from unittest import TestCase
from calculator import mul, div, square

class CalculatorTest(TestCase):

    def test_mul(self):
        self.assertEqual(mul(2, 0), 0)

    def test_div(self):
        self.assertEqual(div(2, 2), 1)

    def test_square(self):
        self.assertEqual(square(2, 2), 4)

# import pytest
# from calculator import mul, div

# def test_mul():
#     assert mul(2, 0) == 0

# def test_div():
#     assert div(2, 2) == 1