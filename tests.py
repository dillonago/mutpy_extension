import unittest
import numpy as np
import math
from verify import *


class test_Any(unittest.TestCase):
    def test_any(self):
        arr = np.full((3, 2), True, dtype=np.bool)
        arr[0, 0] = False
        self.assertEqual(check_any(arr), True)

    def test_all(self):
        arr = np.full((3, 2), True, dtype=np.bool)
        arr[0, 0] = False
        self.assertEqual(check_all(arr), False)

    def test_zeros(self):
        shape = (2, 3)
        self.assertEqual(get_zeros(shape).sum() == 0, True)

    def test_ones(self):
        shape = (2, 3)
        self.assertEqual(get_ones(shape).sum() == math.prod(shape), True)

    def test_average(self):
        matrix = np.array([1, 2, 3, 4])
        avg = get_average(matrix)
        self.assertEqual(avg, 1)

    def test_zeros_like(self):
        arr = np.array([[1, 2, 3, 4], [2, 3, 4, 5]])
        stuff = get_zeroslike(arr)
        result = stuff.shape[0] == 2 and stuff.shape[1] == 4 and stuff.sum() == 0
        self.assertEqual(result, True)

    def test_ones_like(self):
        arr = np.array([[1, 2, 3, 4], [2, 3, 4, 5]])
        stuff = get_oneslike(arr)
        result = stuff.shape[0] == 2 and stuff.shape[1] == 4 and stuff.sum() == 8
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()
