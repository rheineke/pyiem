import iem


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
