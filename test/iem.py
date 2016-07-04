import unittest

import iem
import iem.operator


class TestIEM(unittest.TestCase):
    def test_opposite(self):
        self.assertEqual(iem.Side.BUY.opposite(), iem.Side.SELL)
        self.assertEqual(iem.Side.SELL.opposite(), iem.Side.BUY)

    def test_most_outside_price(self):
        self.assertEqual(iem.most_outside_price(iem.Side.BUY), iem.MIN_PRICE)
        self.assertEqual(iem.most_outside_price(iem.Side.SELL), iem.MAX_PRICE)
