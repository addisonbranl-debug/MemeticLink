import numpy as np
import os
import cv2
from skimage.feature import hog

#Analizes a photo and returns a Histogram of Oriented Gradients (HOG) vector using scikit-image.
#Takes a string representing a file path or a numpy array representing an image.
#Takes optional parameters for target size, orientations, pixels per cell, and cells per block that default to (128, 128), 9, (8, 8), and (2, 2) respectively.
#Returns a vector of HOG features detected in the image.
#Throws FileNotFoundError if the file path is wrong.
def hog_to_vector(image, target_size=(128, 128), orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2)):
    if isinstance(image, str):
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image file not found: {image}")
        img = cv2.imread(image)
    else:
        img = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, target_size)
    features = hog(resized, orientations=orientations, pixels_per_cell=pixels_per_cell, cells_per_block=cells_per_block, feature_vector=True)
    return features.astype(np.float32)