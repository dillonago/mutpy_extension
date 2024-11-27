import unittest
import numpy as np
from example.num import check_sum_diff, check_sum_same, check_prod_diff, check_prod_same

class checkNumpy(unittest.TestCase):
    def test_sum_same(self): 
        arr = np.array([[2,4,6], [9,5,4]])
        result = check_sum_same(arr, axis=1)
        self.assertEqual(result.ndim, 2)

    def test_sum_diff(self): 
        arr = np.array([[2,4,6], [9,5,4]])
        result = check_sum_diff(arr, axis=1)
        self.assertEqual(result.ndim, 1)

    def test_prod_same(self): 
        arr = np.array([[2,4,6], [9,5,4]])
        result = check_prod_same(arr, axis=1)
        self.assertEqual(result.ndim, 2)

    def test_prod_diff(self): 
        arr = np.array([[2,4,6], [9,5,4]])
        result = check_prod_diff(arr, axis=1)
        self.assertEqual(result.ndim, 1)

if __name__ == '__main__':
    unittest.main()