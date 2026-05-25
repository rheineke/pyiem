import unittest

from src import pyiem


class IowaElectronicMarketsTest(unittest.TestCase):
    def testSide(self):
        # self.assertEqual(repr(pyiem.Side.BUY), 'buy')
        self.assertEqual(str(pyiem.Side.BUY), 'buy')
        # self.assertEqual(repr(pyiem.Side.SELL), 'sell')
        self.assertEqual(str(pyiem.Side.SELL), 'sell')
