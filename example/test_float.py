import numpy as np
import pandas as pd
import unittest
from example.float import floatMul, comMul

class testFloat(unittest.TestCase):
    def test_floatMul(self):
        data = np.random.rand(2,3).astype(np.float32)
        df = pd.DataFrame(data)
        num = np.float32(np.random.rand())
        df_mul = df*num
        output = df_mul.equals(floatMul(df, num))
        # print(output)
        self.assertTrue(output)

    def test_comMul(self):
        data = np.random.rand(2,3).astype(np.complex64)
        df = pd.DataFrame(data)
        num = np.complex64(np.random.rand())
        df_mul = df*num
        output = df_mul.equals(comMul(df, num))
        # print(output)
        self.assertTrue(output)
        

if __name__=="__main__":
    unittest.main()