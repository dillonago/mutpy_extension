import pandas as pd
from example.axis import axis_0, axis_1
import unittest

class TestAxis(unittest.TestCase):
    def test_axis_0(self):
        df = pd.DataFrame([[1,3],[2,4],[3,5],[4,6]])
        result = axis_0(df)
        self.assertEqual(result.shape[0], 2)
        

    def test_axis_1(self):
        df = pd.DataFrame([[1,3],[2,4],[3,5],[4,6]])
        result = axis_1(df)
        self.assertEqual(result.shape[0], 4)

if __name__=="__main__":
    unittest.main()

