import numpy as np
import os
import cv2
import mediapipe as mp

MODEL_PATH = os.path.join(os.path.dirname(__file__), "face_landmarker.task")

#Analizes a photo and returns a vector of facial landmarks using MediaPipe.
#Takes a string representing a file path or a numpy array representing an image.
#Takes an optional boolean for whether to normalise the landmarks relative to the face bounding box, defaulting to True.
#Returns a numpy array of shape (1434,) representing the flattened x, y, z coordinates of 478 landmarks.
#Throws FileNotFoundError if the file path is wrong.
#Throws ValueError if there is no face detected in the image.
def mediapipe_to_vector(image, normalise=True):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
        img = cv2.imread(image)
    else:
        img = image.copy()
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_faces=1,
    )
    with mp.tasks.vision.FaceLandmarker.create_from_options(options) as landmarker:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_image)
    if not result.face_landmarks:
        raise ValueError("No face detected in the image.")
    landmarks = result.face_landmarks[0]
    coords = np.array([[lm.x, lm.y, lm.z] for lm in landmarks], dtype=np.float32)
    if normalise:
        centroid = coords.mean(axis=0)
        coords -= centroid
        scale = coords[:, :2].max() - coords[:, :2].min()
        if scale > 0:
            coords /= scale
    return coords.flatten()
