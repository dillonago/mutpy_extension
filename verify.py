import numpy as np

def check_any(arr):
    return np.any(arr)
def check_all(arr):
    return np.all(arr)
def get_zeros(shape):
    return np.zeros(shape)
def get_ones(shape):
    return np.ones(shape)
def get_average(arr):
    weights = np.zeros_like(arr)
    weights[0] = 1
    return np.average(arr, weights=weights)
def get_zeroslike(arr):
    return np.zeros_like(arr)
def get_oneslike(arr):
    return np.ones_like(arr)
