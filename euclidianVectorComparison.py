import numpy as np

#Compares 2 vectors and returns a float representing the Euclidean distance between them.
#Takes 2 numpy arrays.
#Returns a float representing the Euclidean distance between the two vectors. 0.0 means identical vectors.
#Throws ValueError if the arrays have different shapes.
def euclidean_distance(a, b):
    if a.shape != b.shape:
        raise ValueError(f"Vector shapes do not match: {a.shape} vs {b.shape}")
    return float(np.sqrt(np.sum((a - b) ** 2)))
