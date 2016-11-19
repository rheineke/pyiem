import unittest

import pandas as pd

from iem import config


class ConfigTest(unittest.TestCase):
    def testActiveMarkets(self):
        mkt_conf = config.read_markets()
        ts = pd.Timestamp(year=2016, month=11, day=18)
        active_mkt_conf = config.active_markets(mkt_conf, ts)
        fed = 'FedPolicyB'
        self.assertEqual(len(active_mkt_conf), 1)
        self.assertTrue(fed in active_mkt_conf)
        self.assertEqual(len(active_mkt_conf[fed]), 2)
