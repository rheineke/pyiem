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
