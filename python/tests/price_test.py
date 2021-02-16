from data_source.lib.price import Price, PriceTwoDecimal
import unittest
from unittest import TestCase
class PriceTwoDecimalTest(TestCase):

    def test_zero_parsing(self):
        price = PriceTwoDecimal(0.0)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 0)
        self.assertEqual(price.int_num, 0)
        self.assertEqual(str(price), "0.00")

    def test_non_zero_parsing_simple(self):
        price = PriceTwoDecimal(34.56)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 56)
        self.assertEqual(price.int_num, 34)
        self.assertEqual(str(price), "34.56")

    def test_non_zero_parsing_zero_int(self):
        price = PriceTwoDecimal(0.56)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 56)
        self.assertEqual(price.int_num, 0)
        self.assertEqual(str(price), "0.56")
    
    def test_non_zero_parsing_zero_float(self):
        price = PriceTwoDecimal(34.0)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 0)
        self.assertEqual(price.int_num, 34)
        self.assertEqual(str(price), "34.00")
    
    def test_non_zero_parsing_one_float(self):
        price = PriceTwoDecimal(34.30)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 30)
        self.assertEqual(price.int_num, 34)
        self.assertEqual(str(price), "34.30")

    def test_non_zero_parsing_one_float2(self):
        price = PriceTwoDecimal(34.03)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 3)
        self.assertEqual(price.int_num, 34)
        self.assertEqual(str(price), "34.03")

    def test_non_zero_parsing_truncate(self):
        price = PriceTwoDecimal(34.033)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 3)
        self.assertEqual(price.int_num, 34)
        self.assertEqual(str(price), "34.03")

        price = PriceTwoDecimal(34.038)
        self.assertEqual(price.precision, 100)
        self.assertEqual(price.float_num, 4)
        self.assertEqual(price.int_num, 34)
        self.assertEqual(str(price), "34.04")
    
    def test_eq_op(self):
        p1 = PriceTwoDecimal(23.33)
        p11 = PriceTwoDecimal(23.332)

        p2 = PriceTwoDecimal(23.30)
        p3 = PriceTwoDecimal(3.33)

        self.assertTrue(p1 == p11)
        self.assertTrue(p1 != p2)
        self.assertTrue(p1 != p3)
        self.assertTrue(p2 != p3)

    def test_comp_op(self):
        small = PriceTwoDecimal(34.30)
        large = PriceTwoDecimal(36.15)
        self.assertEqual(small.float_num, 30)
        self.assertEqual(small.int_num, 34)
        self.assertEqual(large.float_num, 15)
        self.assertEqual(large.int_num, 36)
        self.assertTrue(small < large)
        self.assertTrue(small <= large)
        self.assertTrue(small != large)

        self.assertTrue(large > small)
        self.assertTrue(large >= small)
        self.assertTrue(large != small)
    
if __name__ == "__main__":
    unittest.main()
