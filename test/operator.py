import unittest

from iem import Side
from iem import operator


class TestOperator(unittest.TestCase):
    def test_outside(self):
        self.assertTrue(operator.inside(Side.BUY)(6, 5))
        self.assertFalse(operator.inside(Side.BUY)(5, 6))
        self.assertTrue(operator.inside(Side.SELL)(5, 6))
        self.assertTrue(operator.inside(Side.BUY)(6, 5))

    def test_outside(self):
        self.assertTrue(operator.outside(Side.BUY)(5, 6))
        self.assertFalse(operator.outside(Side.BUY)(6, 5))
        self.assertTrue(operator.outside(Side.SELL)(6, 5))
        self.assertTrue(operator.outside(Side.BUY)(5, 6))

    def test_move_inside(self):
        self.assertEqual(operator.move_inside(Side.BUY)(5, 1), 6)
        self.assertEqual(operator.move_inside(Side.SELL)(5, 1), 4)
        self.assertEqual(operator.move_outside(Side.BUY)(5, 1), 4)
        self.assertEqual(operator.move_outside(Side.SELL)(5, 1), 6)
