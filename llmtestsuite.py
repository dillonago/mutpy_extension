import numpy as np
import pandas as pd
import unittest
from float import floatMul, comMul

class testFloat(unittest.TestCase):

    def test_floatMul(self):
        data = np.random.rand(2, 3).astype(np.float32)
        df = pd.DataFrame(data)
        num = np.float64(np.random.rand())
        df_mul = df * num
        output = df_mul.equals(floatMul(df, num))
        self.assertTrue(output)

    def test_comMul(self):
        data = np.random.rand(2, 3).astype(np.complex64)
        df = pd.DataFrame(data)
        num = np.complex64(np.random.rand())
        df_mul = df * num
        output = df_mul.equals(comMul(df, num))
        self.assertTrue(output)

    def test_floatMul2(self):
        data = np.array([np.inf, -np.inf, np.nan]).reshape(1, 3).astype(np.float32)
        df = pd.DataFrame(data)
        num = np.float64(1)
        df_mul = df * num
        output = df_mul.equals(floatMul(df, num))
        self.assertTrue(output)
if __name__ == '__main__':
    unittest.main()