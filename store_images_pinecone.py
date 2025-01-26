import os
import csv
import base64
import requests
import torch
import pandas as pd
from PIL import Image
from io import BytesIO
from pinecone import Pinecone
from transformers import CLIPProcessor, CLIPModel

PINECONE_API_KEY = "pcsk_4A88Ck_E1mE5KfTMW77KaN3QAPVZGG4MMLzxxmwKCvsP8ESDMzvaCqpiUZEuGvJatAX66m"
pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "hack0125"

index = pc.Index(INDEX_NAME)

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def get_image_embedding(image_data):
    if isinstance(image_data, bytes):
        image = Image.open(BytesIO(image_data)).convert("RGB")
    else:
        image = image_data.convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    embeddings = outputs[0].cpu().numpy().tolist()
    return embeddings

def get_image_from_path_or_url(image_source: str):
    if image_source.startswith(('http://', 'https://')):
        response = requests.get(image_source)
        return Image.open(BytesIO(response.content))
    else:
        return Image.open(image_source)

def upsert_to_pinecone(vector_id: str, embedding, metadata: dict):
    index.upsert(vectors=[
        (vector_id, embedding, metadata)
    ])

def main(csv_file_path):
    df = pd.read_csv(csv_file_path, sep=';')
    total_rows = len(df)

    for idx, row in df.iterrows():
        try:
            nid = str(row['Nid'])
            seller_id = str(row['SellerId'])
            brandname = str(row['Brandname'])
            review = str(row['review'])
            price = str(row['price'])
            image_source = str(row['imageUrl'])
            product_url = str(row['productUrl'])

            try:
                image = get_image_from_path_or_url(image_source)
                embedding = get_image_embedding(image)
            except Exception as e:
                print(f"Warning: Failed to process image for Nid={nid}: {e}")
                continue

            metadata = {
                "Nid": nid,
                "SellerId": seller_id,
                "Brandname": brandname,
                "review": review,
                "price": price,
                "productUrl": product_url,
                "imageUrl": image_source
            }

            upsert_to_pinecone(image_source, embedding, metadata)

            print(f"Upserted image_source={image_source} to Pinecone.")

            print(f"Progress: {idx+1}/{total_rows}", end='\r')

        except Exception as e:
            print(f"\nError processing row {idx}: {e}")
            continue

    print("\nProcessing complete!")

if __name__ == "__main__":
    CSV_FILE_PATH = "./data.csv"
    main(CSV_FILE_PATH)
