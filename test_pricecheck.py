import unittest
class TestVerifyPrice(unittest.TestCase):
    def test_verify(self,system,stype,price):
        try:
            self.assertEqual(system.pricedict[stype],price)
            print("The entered price is correct.")
        except KeyError:
            raise ValueError("The entered service type is not valid!")