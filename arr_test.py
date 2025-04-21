import numpy as np
from arr import arr_mul
import unittest

class TestAxis(unittest.TestCase):
    def test_arr(self):
        self.assertEqual(arr_mul([2, 2, 2]), 12)

if __name__=="__main__":
    unittest.main()