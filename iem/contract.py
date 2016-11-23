from iem import config


class Market:
    def __init__(self, market_name, market_fp=None):
        self.name = market_name
        self.id = config.read_markets(market_fp)[market_name]['id']

    def __repr__(self):
        return '{}: {}'.format(self.name, self.id)


class ContractBundle:
    def __init__(self, market_name, expiration):
        self.market = Market(market_name)
        self.expiration = expiration
        b = config.find_bundle(config.read_markets(), market_name, expiration)
        self.id = int(b['bundle_id'])


class Contract:
    def __init__(self, market_name, contract_name):
        self.contract_name = contract_name
        self.market = Market(market_name)
        a = config.find_asset(config.read_markets(), market_name, contract_name)
        self.asset_id = int(a['id'])
        self.asset_to_market_id = int(a['order'])

    def __repr__(self):
        return self.contract_name
