"""Core classes and constants for the Iowa Electronic Market

Public attributes:
- Market
- contract
"""
import json
from collections import OrderedDict
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


@unique
class Side(Enum):
    BUY = 0
    SELL = 1

    def opposite(self):
        return Side.SELL if self.value is 0 else Side.BUY


def read_markets_json(market_fp=None, **load_kwargs):
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        # Use OrderedDict to maintain ordering
        mkts = json.load(fp, **load_kwargs)
    return mkts


def asset_dict(markets):
    asset_data_dict = dict()
    for mkt in markets.values():
        mkt_dict = {'mkt_id': mkt['id']}
        pairs = [(k, dict(v, **mkt_dict)) for k, v in mkt['assets'].items()]
        asset_data_dict.update(pairs)
    return asset_data_dict


def best_price_name(side):
    return BEST_BID if side is Side.BUY else BEST_ASK


def price_name(side):
    return BID if side is Side.BUY else ASK


def move_inside(side, px_srs, increment):
    return px_srs + increment if side is Side.BUY else px_srs - increment


def most_outside_price(side):
    return MIN_PRICE if side is Side.BUY else MAX_PRICE


def is_outside(side, srs, other):
    return srs < other if side is Side.BUY else srs > other
