import unittest

from default_parameters import mul, append_hello, append_world


class TestMulFunction(unittest.TestCase):

    def test_mul_correct_all_default(self):
        self.assertEqual(mul(), 1)

    def test_mul_correct_x_default(self):
        self.assertEqual(mul(y=2), 2)

    def test_mul_correct_no_default(self):
        self.assertEqual(mul(x=3, y=2), 6)


class TestAppendFunctions(unittest.TestCase):

    def test_append_hello_correct_default(self):
        self.assertEqual(append_hello(), "hello")

    def test_append_hello_correct_not_default(self):
        self.assertEqual(append_hello("great"), "greathello")

    def test_append_world_correct_default(self):
        self.assertEqual(append_world(), "helloworld")

    def test_append_world_correct_not_default(self):
        self.assertEqual(append_world(None), "world")
