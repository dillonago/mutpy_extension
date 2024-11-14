import pandas as pd
from df import drop_column_inplace, drop_column_copy
import unittest

class TestPandas(unittest.TestCase):
    def test_drop_column_inplace(self):
        data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
        df = pd.DataFrame(data)
        
        drop_column_inplace(df, 'B')
        
        self.assertNotIn('B', df.columns, "Column 'B' was dropped using inplace=True")
        
    def test_drop_column_copy(self):
        data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
        df = pd.DataFrame(data)
        
        df_new = drop_column_copy(df, 'B')

        self.assertNotIn('B', df_new.columns, "Column 'B' was dropped in the new DataFrame")
        self.assertIn('B', df.columns, "Original DataFrame was not modified despite using inplace=False")

if __name__ == "__main__":
    unittest.main()