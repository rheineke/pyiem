import unittest

import numpy as np
import pandas as pd

from iem.order import PriceTimeLimit


def _test_expiry():
    return pd.Timestamp(year=2016, month=1, day=10, hour=20, minute=1)


class PriceTimeLimitTest(unittest.TestCase):
    def testConstructor(self):
        with self.assertRaises(ValueError):
            PriceTimeLimit(np.nan, _test_expiry())
