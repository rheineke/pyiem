import unittest

from iem import config
from iem.contract import Market


class MarketTest(unittest.TestCase):
    def testMarketConstructor(self):
        conf = config.read_markets()
        for mkt_name in conf.keys():
            m = Market(mkt_name)
            self.assertEqual(m.name, mkt_name)
            self.assertEqual(m.id, conf[mkt_name]['id'])

    def testMarketRepr(self):
        m = Market('FedPolicyB')
        self.assertEqual(repr(m), '{}: {}'.format(m.name, m.id))
