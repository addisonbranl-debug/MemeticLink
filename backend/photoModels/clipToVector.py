import numpy as np
import os
import clip
import torch
from PIL import Image

#Analizes a photo and returns a semantic embedding vector using OpenAI's CLIP model.
#Takes a string representing a file path or a numpy array representing an image.
#Returns a vector of L2-normalised floats representing the CLIP embedding of the image.
#Throws FileNotFoundError if the file path is wrong.
def clip_to_vector(image, model_name="ViT-B/32"):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
        pil_image = Image.open(image).convert("RGB")
    else:
        pil_image = Image.fromarray(
            image[..., ::-1] if image.shape[-1] == 3 else image
        ).convert("RGB")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load(model_name, device=device)
    tensor = preprocess(pil_image).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(tensor)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding.cpu().numpy().squeeze()