import unittest
import numpy as np
from verify import check_any


class test_Any(unittest.TestCase):
    def test_Any(self):
        arr = np.full((3, 2), True, dtype=np.bool)
        arr[0, 0] = False
        self.assertEqual(check_any(arr), True)


if __name__ == "__main__":
    unittest.main()
