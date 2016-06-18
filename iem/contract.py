import iem


class Market:
    # Lookup tables
    _market_dict = iem.read_markets_json()

    def __init__(self, name):
        self.name = name
        self.value = self._market_dict[name]['id']

    def __repr__(self):
        return self.name


class Contract:
    # Lookup tables
    _market_asset_dict = iem.read_markets_json()
    _asset_dict = iem.asset_dict(_market_asset_dict)

    def __init__(self, name):
        self.name = name
        asset = Contract._asset_dict[name]
        self.asset_id = asset['id']
        self.asset_to_market = asset['order']
        self.market = asset['mkt_id']

    def __repr__(self):
        return self.name


class ContractBundle:
    # Lookup tables
    _market_asset_dict = iem.read_markets_json()

    def __init__(self, mkt_name, expiration):
        self.market_name = mkt_name
        self.expiration = expiration
        mkt = ContractBundle._market_asset_dict[mkt_name]
        self.bundle_id = mkt['bundles'][expiration]
        self.market = mkt['id']

    def __repr__(self):
        return self.market_name + ' ' + self.expiration
