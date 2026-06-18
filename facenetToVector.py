import numpy as np
import os
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

#Analizes a photo and returns a FaceNet identity embedding vector.
#Takes a string representing a file path or a numpy array representing an image.
#Returns a vector of L2-normalised float embeddings.
#Throws FileNotFoundError if the file path is wrong.
#Throws ValueError if there is no face detected in the image.
def facenet_to_vector(image):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
        pil_image = Image.open(image).convert("RGB")
    else:
        pil_image = Image.fromarray(
            image[..., ::-1] if image.shape[-1] == 3 else image
        ).convert("RGB")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    mtcnn = MTCNN(image_size=160, device=device)
    resnet = InceptionResnetV1(pretrained="vggface2").eval().to(device)
    face_tensor = mtcnn(pil_image)
    if face_tensor is None:
        raise ValueError("No face detected in the image.")
    with torch.no_grad():
        embedding = resnet(face_tensor.unsqueeze(0).to(device))
    return embedding.cpu().numpy().squeeze()