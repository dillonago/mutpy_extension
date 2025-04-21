from simple import mul, div, simple_eq, arr_mul, simple_eq2
import unittest

class test_simple(unittest.TestCase):

    def test_mul(self):
        self.assertEqual(mul(2, 2), 4)

    def test_div(self):
        self.assertEqual(div(2, 2), 1)

    def test_simple_eq(self):
        self.assertTrue(simple_eq(1, 0) > 0)

    def test_arr(self):
        self.assertEqual(arr_mul([2, 2, 2]), 12)

    def test_simple_eq2(self):
        self.assertTrue(simple_eq2(4, 2) > 0)

    def test_division(self):
        self.assertEqual(div(10, 3), 3.3333333333333335)
if __name__ == '__main__':
    unittest.main()