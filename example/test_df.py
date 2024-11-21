import pandas as pd
from df import (
    drop_column_inplace,
    drop_column_copy,
    fillna_inplace,
    fillna_copy,
    sort_values_copy,
    sort_values_inplace,
)
import unittest


class TestPandas(unittest.TestCase):
    def test_drop_column_inplace(self):
        data = {"A": [1, 2, 3], "B": [4, 5, 6]}
        df = pd.DataFrame(data)

        drop_column_inplace(df, "B")

        self.assertNotIn("B", df.columns, "Column 'B' was dropped using inplace=True")

    def test_drop_column_copy(self):
        data = {"A": [1, 2, 3], "B": [4, 5, 6]}
        df = pd.DataFrame(data)

        df_new = drop_column_copy(df, "B")

        self.assertNotIn(
            "B", df_new.columns, "Column 'B' was dropped in the new DataFrame"
        )
        self.assertIn(
            "B",
            df.columns,
            "Original DataFrame was not modified despite using inplace=False",
        )

    def test_fillna_inplace(self):
        df = pd.DataFrame({"A": [1, None], "B": [None, 4]})
        fillna_inplace(df, 0)
        self.assertEqual(
            df.isnull().sum().sum(), 0, "All NaN values should be replaced inplace"
        )

    def test_fillna_copy(self):
        df = pd.DataFrame({"A": [1, None], "B": [None, 4]})
        new_df = fillna_copy(df, 0)
        self.assertGreater(
            df.isnull().sum().sum(), 0, "Original DataFrame should have NaN values"
        )
        self.assertEqual(
            new_df.isnull().sum().sum(), 0, "New DataFrame should have no NaN values"
        )

    def test_sort_values_inplace(self):
        df = pd.DataFrame({"A": [3, 1, 2]})
        sort_values_inplace(df, by="A")
        self.assertEqual(
            df["A"].tolist(), [1, 2, 3], "DataFrame should be sorted inplace"
        )

    def test_sort_values_copy(self):
        df = pd.DataFrame({"A": [3, 1, 2]})
        new_df = sort_values_copy(df, by="A")
        self.assertEqual(
            df["A"].tolist(), [3, 1, 2], "Original DataFrame should remain unsorted"
        )
        self.assertEqual(
            new_df["A"].tolist(), [1, 2, 3], "New DataFrame should be sorted"
        )


if __name__ == "__main__":
    unittest.main()
