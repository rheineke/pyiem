import unittest

import pandas as pd

from iem import config


class ConfigTest(unittest.TestCase):
    def testActiveMarkets(self):
        ts = pd.Timestamp(year=2016, month=11, day=18)
        self._active_markets(ts, 1, 2)

    def testActiveMarketsEndOfYear(self):
        ts = pd.Timestamp(year=2016, month=12, day=30)
        self._active_markets(ts, 4, 3)

    def _active_markets(self, ts, exp_num_active_markets, exp_num_fed_bundles):
        mkt_conf = config.read_markets()
        active_mkt_conf = config.active_markets(mkt_conf, ts)
        fed = 'FedPolicyB'
        self.assertEqual(len(active_mkt_conf), exp_num_active_markets)
        self.assertTrue(fed in active_mkt_conf)
        num_active_bundles = len(active_mkt_conf[fed][config.BUNDLE])
        self.assertEqual(num_active_bundles, exp_num_fed_bundles)

    def testFindBundle(self):
        mkt_conf = config.read_markets()
        for mkt_name, mkt_dict in mkt_conf.items():
            bundles = mkt_dict[config.BUNDLE]
            if config.BUNDLE_ID in bundles:  # bundles is expected bundle
                bundle = config.find_bundle(mkt_conf, mkt_name, '')
                self.assertEqual(bundles, bundle)
            else:
                for bundle_exp, exp_bundle in bundles.items():
                    bundle = config.find_bundle(mkt_conf, mkt_name, bundle_exp)
                    self.assertEqual(exp_bundle, bundle)

    def testFindAsset(self):
        pass
