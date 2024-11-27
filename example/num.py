import numpy as np

def check_sum_same(arr, axis):
    return np.sum(arr, axis, keepdims=True)

def check_sum_diff(arr, axis):
    return np.sum(arr, axis, keepdims=False)

def check_prod_same(arr, axis):
    return np.prod(arr, axis, keepdims=True)

def check_prod_diff(arr, axis):
    return np.prod(arr, axis, keepdims=False)
