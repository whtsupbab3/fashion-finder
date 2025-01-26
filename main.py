import torch
import clip
from PIL import Image

# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device='cpu')

def get_clip_embedding(img_path):
    image = preprocess(Image.open(img_path)).unsqueeze(0)
    with torch.no_grad():
        embedding = model.encode_image(image)
    return embedding.cpu().numpy().flatten()

# Example usage
embedding = get_clip_embedding('./favicon.png')
print(embedding)  # Typically 512 for CLIP ViT-B/32
