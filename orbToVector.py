import numpy as np
import os
import cv2

#Analizes a photo and returns a vector of descriptors using Oriented FAST and Rotated BRIEF.
#Takes a string representing a file path or a numpy array representing an image.
#Takes an optional number for the maximum number of keypoints to detect that defaults to 500.
#Takes an optional number for the ORB patch size parameter that defaults to 128.
#Returns numpy array of shape (32,) representing the mean-pooled ORB descriptors. 
#Throws ValueError if no keypoints are detected in the image.
#Throws FileNotFoundError if the file path is wrong.
def orb_to_vector(image, n_keypoints=500, patch_size=128):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
        img = cv2.imread(image)
    else:
        img = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=n_keypoints, patchSize=patch_size)
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    if descriptors is None:
        raise ValueError("No keypoints detected in the image")
    return descriptors.mean(axis=0).astype(np.float32)
