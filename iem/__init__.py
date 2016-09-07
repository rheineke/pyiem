"""Core functions and constants for the Iowa Electronic Market"""

import json
from enum import Enum, unique

# Exchange information
ASK = 'ask'
BID = 'bid'
AVG_PX = 'AvgPrice'
BEST_ASK = 'Best Ask'
BEST_BID = 'Best Bid'
CONTRACT = 'Contract'
DATE = 'Date'
DVOL = '$Volume'
EXPIRATION = 'Expiration'
HIGH_PX = 'HighPrice'
LOW_PX = 'LowPrice'
LST_PX = 'LastPrice'
MAX_CONTRACTS = 'Max Contracts Held'
NET_POS = 'Net Position'
ORDER_DATE = 'Order Date'
OWN = 'Own '
OWN_BEST_ASK = OWN + BEST_ASK
OWN_BEST_BID = OWN + BEST_BID
PROFIT = 'Profit'
SGN_ACTION = 'Signed Action'
SGN_QTY = 'Signed Quantity'
TRADE_ID = 'Trade ID'
TRADE_TYPE = 'Trade Type'
UNIT_PX = 'Unit Price'
UNITS = 'Units'
VOL = 'Units'

# URLs
URL = 'https://iem.uiowa.edu/iem/'
LEGACY_URL = 'https://iemweb.biz.uiowa.edu/'

# Price values
TICK = .001
MAX_PRICE = 1
MIN_PRICE = 0


def read_markets_json(market_fp=None, **load_kwargs):
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        mkts = json.load(fp, **load_kwargs)
    return mkts


class Market:
    # Lookup tables
    _market_asset_dict = read_markets_json()

    def __init__(self, name):
        self.name = name
        self.value = self._market_asset_dict[name]['id']

    def __repr__(self):
        return self.name


@unique
class Side(Enum):
    BUY = 0
    SELL = 1

    def opposite(self):
        return Side.SELL if self.value is 0 else Side.BUY


def asset_dict(markets):
    asset_data_dict = dict()
    for mkt in markets.values():
        mkt_dict = {'mkt_id': mkt['id']}
        pairs = [(k, dict(v, **mkt_dict)) for k, v in mkt['assets'].items()]
        asset_data_dict.update(pairs)
    return asset_data_dict


def best_price_name(side):
    return side_value(side, BEST_BID, BEST_ASK)


def price_name(side):
    return side_value(side, BID, ASK)


def most_outside_price(side):
    return side_value(side, MIN_PRICE, MAX_PRICE)


def side_value(side, buy_value, sell_value):
    return buy_value if side is Side.BUY else sell_value
