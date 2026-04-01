import numpy as np

#Compares 2 vectors and returns a float representing the Chebyshev distance between them.
#Takes 2 numpy arrays.
#Returns a float representing the largest absolute difference across any single dimension. 0.0 means identical vectors.
#Throws ValueError if the arrays have different shapes.
def chebyshev_distance(a, b):
    if a.shape != b.shape:
        raise ValueError(f"Vector shapes do not match: {a.shape} vs {b.shape}")
    return float(np.max(np.abs(a - b)))
