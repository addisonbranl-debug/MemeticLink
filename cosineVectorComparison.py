import numpy as np

#Compares 2 vectors and returns a float representing the cosine distance between them.
#Takes 2 numpy arrays.
#Returns a float in [0.0, 2.0] representing the cosine distance. 0.0 means identical direction, 2.0 means opposite.
#Throws ValueError if the arrays have different shapes or either is a zero vector.
def cosine_distance(a, b):
    if a.shape != b.shape:
        raise ValueError(f"Vector shapes do not match: {a.shape} vs {b.shape}")
    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)
    if mag_a == 0 or mag_b == 0:
        raise ValueError("Cannot compute cosine distance for a zero vector.")
    return float(1.0 - (np.dot(a, b) / (mag_a * mag_b)))
