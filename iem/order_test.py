import unittest

import numpy as np
import pandas as pd

from iem import Side
from iem import config
from iem.order import Market
from iem.order import PriceTimeLimit, Single, to_string


class MarketTest(unittest.TestCase):
    def testMarketConstructor(self):
        conf = config.read_markets_json()
        for mkt_name in conf.keys():
            m = Market(mkt_name)
            self.assertEqual(m.name, mkt_name)
            self.assertEqual(m.id, conf[mkt_name]['id'])


def _test_expiry():
    return pd.Timestamp(year=2016, month=1, day=10, hour=20, minute=1)


class PriceTimeLimitTest(unittest.TestCase):
    def testConstructor(self):
        ptl = PriceTimeLimit(np.nan, pd.NaT)  # IOC PriceTimeLimit
        px = .999
        ptl = PriceTimeLimit(px, pd.NaT)  # GTC PriceTimeLimit
        ptl = PriceTimeLimit(px, _test_expiry())  # Limit PriceTimeLimit
        with self.assertRaises(ValueError):
            PriceTimeLimit(np.nan, _test_expiry())

    def testIOC(self):
        ptl = PriceTimeLimit(np.nan, pd.NaT)
        self.assertTrue(ptl.ioc)
        px = .999
        ptl = PriceTimeLimit(px, pd.NaT)
        self.assertFalse(ptl.ioc)
        ptl = PriceTimeLimit(px, _test_expiry())
        self.assertFalse(ptl.ioc)

    def testSessionStringFormat(self):
        self.assertEqual(to_string(_test_expiry()), '2016-01-10 08:01 PM')
        self.assertEqual(to_string(pd.NaT), 'No expiration')

    def testExpiryDate(self):
        pass

    def testRepr(self):
        ptl = PriceTimeLimit(.999, _test_expiry())
        self.assertEqual(str(ptl), '0.999 2016-01-10 08:01 PM')


class OrderTest(unittest.TestCase):
    def testConstructor(self):
        s = Single("FRup116", Side.BUY, 1, PriceTimeLimit(np.nan, pd.NaT))
