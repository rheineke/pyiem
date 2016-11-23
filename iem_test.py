import unittest

import iem


class IowaElectronicMarketsTest(unittest.TestCase):
    def testSide(self):
        # self.assertEqual(repr(iem.Side.BUY), 'buy')
        self.assertEqual(str(iem.Side.BUY), 'buy')
        # self.assertEqual(repr(iem.Side.SELL), 'sell')
        self.assertEqual(str(iem.Side.SELL), 'sell')
