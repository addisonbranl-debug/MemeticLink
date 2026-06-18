import numpy as np

# KL divergence and Jensen-Shannon divergence functions below:

#Compares 2 vectors and returns a float representing the KL divergence from a to b.
#Takes 2 numpy arrays.
#Takes an optional epsilon to avoid log(0) errors.
#Returns a float representing the KL divergence from a to b. 0.0 means identical distributions.
#Throws ValueError if the arrays have different shapes.
def kl_divergence(a, b, epsilon=1e-10):
    if a.shape != b.shape:
        raise ValueError(f"Vector shapes do not match: {a.shape} vs {b.shape}")
    p = (a / (a.sum() or 1.0)) + epsilon
    q = (b / (b.sum() or 1.0)) + epsilon
    return float(np.sum(p * np.log(p / q)))

#Compares 2 vectors and returns a float representing the Jensen-Shannon divergence between them.
#Takes 2 numpy arrays.
#Takes an optional epsilon to avoid log(0) errors.
#Returns a float representing the Jensen-Shannon divergence between the two vectors. 0.0 means identical distributions.
#Throws ValueError if the arrays have different shapes.
def jensen_shannon_divergence(a, b, epsilon=1e-10):
    if a.shape != b.shape:
        raise ValueError(f"Vector shapes do not match: {a.shape} vs {b.shape}")
    p = (a / (a.sum() or 1.0)) + epsilon
    q = (b / (b.sum() or 1.0)) + epsilon
    m = (p + q) / 2
    kl_pm = np.sum(p * np.log(p / m))
    kl_qm = np.sum(q * np.log(q / m))
    return float((kl_pm + kl_qm) / 2)