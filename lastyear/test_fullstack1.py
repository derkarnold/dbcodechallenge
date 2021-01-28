import unittest
from .fullstack1 import sumMultiplesBelow

class TestStage1(unittest.TestCase):
    def test_base_case(self):
        result = sumMultiplesBelow(20, 5, 7)
        self.assertEqual(result, 51)
        
    def test_answer_case(self):
        result = sumMultiplesBelow(1000, 5, 7)
        self.assertEqual(result, 156361)
