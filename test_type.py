from type import div, random
import unittest

class test_type(unittest.TestCase): 
    def test_div(self):
       self.assertEqual(type(div(2, 2)), float)
    
    def test_random(self):
        self.assertTrue(random(1,0) > 0)





if __name__=="__main__":
    unittest.main()