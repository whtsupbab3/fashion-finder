import torch
from PIL import Image
from pinecone import Pinecone
from transformers import CLIPProcessor, CLIPModel
from store_images_pinecone import get_image_embedding, get_image_from_path_or_url

PINECONE_API_KEY = "pcsk_4A88Ck_E1mE5KfTMW77KaN3QAPVZGG4MMLzxxmwKCvsP8ESDMzvaCqpiUZEuGvJatAX66m"
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "hack0125"
index = pc.Index(INDEX_NAME)

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def find_similar_images(query_image_path: str, top_k: int = 5):
    query_image = get_image_from_path_or_url(query_image_path)
    query_embedding = get_image_embedding(query_image)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results

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

if __name__ == "__main__":
    test_image_path = "https://i5.walmartimages.com/asr/45f3f324-d2da-4121-a6d0-d7b253813400.7e8a49af1676fb2c1a36e9d308f792ea.jpeg"

    test_image_url = "https://i5.walmartimages.com/asr/45f3f324-d2da-4121-a6d0-d7b253813400.7e8a49af1676fb2c1a36e9d308f792ea.jpeg"

    try:
        print("\nTesting with local image...")
        results = find_similar_images(test_image_path)
        print_results(results)

        print("\nTesting with URL image...")
        results = find_similar_images(test_image_url)
        print_results(results)

    except Exception as e:
        print(f"Error during testing: {e}")
