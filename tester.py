from unittest import TestCase
from testFunctions import mul, div

class CalculatorTest(TestCase):
    def test_mul(self):
        self.assertEqual(mul(2, 2), 4)

    def test_div(self):
        self.assertEqual(div(2, 2), 1)
