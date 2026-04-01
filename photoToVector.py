import numpy as np
from deepface import DeepFace
import os

#Analizes a photo and returns a vector of emotions using DeepFace.
#Takes a string representing a file path or a numpy array representing an image.
#Returns a vector of emotions detected in the image.
#Throws FileNotFoundError if the file path is wrong.
#Throws ValueError if there is no face detected in the image.
def photo_to_vector(image):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
    try:
        results = DeepFace.analyze(img_path=image, actions=["emotion"], enforce_detection=True)
    except ValueError as e:
        raise ValueError(f"No face detected in the image: {e}") from e
    if isinstance(results, list):
        emotions = results[0]["emotion"] if len(results) == 1 else results[0]["emotion"]
    else:
        emotions = results["emotion"]
    return np.array(list(emotions.values()), dtype=np.float64)