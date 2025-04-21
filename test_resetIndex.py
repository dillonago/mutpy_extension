import unittest
from resetIndex import no_resetIndex, resetIndex
import pandas as pd
import numpy as np

class test_resetIndex(unittest.TestCase): 
    def test_resetIndex(self):
        df = pd.DataFrame({
            'Group': ['A','B','A','B','A','B'], 
            'SubGroup': ['C','C','D','D','C','D'], 
            'Value': [10,20,5,6,34,13]
        })
        result = resetIndex(df, 'SubGroup')
        self.assertEqual(result.shape[1], 3)


    def test_no_resetIndex(self):
        df = pd.DataFrame({
            'Group': ['A','B','A','B','A','B'], 
            'SubGroup': ['C','C','D','D','C','D'], 
            'Value': [10,20,5,6,34,13]
        })
        result = no_resetIndex(df, 'SubGroup')
        self.assertEqual(result.shape[1], 2)

    

if __name__=="__main__":
    unittest.main()