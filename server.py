from pinecone import Pinecone, ServerlessSpec
import os
import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import torch
from PIL import Image
from io import BytesIO
import requests
from transformers import CLIPProcessor, CLIPModel
import csv
import base64
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tomlkit.api import key

client = openai.OpenAI(api_key=os.getenv(OPENAI_API_KEY))
pc = Pinecone(api_key=os.getenv(PINECONE_API_KEY))

index = pc.Index(os.getenv(INDEX))

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
device = torch.device("cpu")
model.to(device)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add after CORS middleware setup
app.mount("/images", StaticFiles(directory="images"), name="images")

class SearchRequest(BaseModel):
    image_url: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    brand: Optional[str] = None
    top_k: Optional[int] = 5

class ErrorResponse(BaseModel):
    error: str

def get_image_embedding(image_data):
    if isinstance(image_data, bytes):
        image = Image.open(BytesIO(image_data)).convert("RGB")
    else:
        image = image_data.convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    return outputs[0].cpu().numpy().tolist()

def get_image_from_url(image_url: str):
    response = requests.get(image_url)
    return Image.open(BytesIO(response.content))

def find_similar_images(image_url: str, top_k: int = 5):
    query_image = get_image_from_url(image_url)
    query_embedding = get_image_embedding(query_image)

    return index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

def print_results(results):
    print("\nSimilar images found:")
    print("-" * 50)

    for match in results['matches']:
        score = match['score']
        metadata = match['metadata']
        print(f"Similarity Score: {score:.4f}")
        print(f"Brand: {metadata.get('Brandname', 'N/A')}")
        print(f"Price: {metadata.get('price', 'N/A')}")
        print(f"Image URL: {metadata.get('imageUrl', 'N/A')}")
        print(f"Product URL: {metadata.get('productUrl', 'N/A')}")
        print("-" * 50)

@app.post("/search")
async def search_similar_products(request: SearchRequest):
    try:
        results = find_similar_images(request.image_url, top_k=10)

        filtered_matches = []
        for match in results['matches']:
            metadata = match['metadata']

            try:
                price = float(metadata.get('price', '0').replace('$', '').replace(',', ''))
            except ValueError:
                continue

            price_in_range = True
            if request.min_price is not None:
                price_in_range = price_in_range and price >= request.min_price
            if request.max_price is not None:
                price_in_range = price_in_range and price <= request.max_price

            brand_match = True
            if request.brand:
                brand_match = metadata.get('Brandname', '').lower() == request.brand.lower()

            if price_in_range and brand_match:
                filtered_matches.append({
                    'score': match['score'],
                    'product': {
                        'brand': metadata.get('Brandname'),
                        'price': price,
                        'image_url': metadata.get('imageUrl'),
                        'product_url': metadata.get('productUrl'),
                        'review': metadata.get('review')
                    }
                })

        return {
            'results': filtered_matches[:request.top_k],
            'total_found': len(filtered_matches)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
