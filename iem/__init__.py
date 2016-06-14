"""Core classes and constants for the Iowa Electronic Market

Public attributes:
- Market
- contract
"""
import json
from enum import Enum, unique

AVG_PX = 'AvgPrice'
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
PROFIT = 'Profit'
SGN_ACTION = 'Signed Action'
SGN_QTY = 'Signed Quantity'
TRADE_ID = 'Trade ID'
TRADE_TYPE = 'Trade Type'
UNIT_PX = 'Unit Price'
UNITS = 'Units'
VOL = 'Units'

URL = 'https://iem.uiowa.edu/iem/'
LEGACY_URL = 'https://iemweb.biz.uiowa.edu/'


ASK = 'ask'
BID = 'bid'


@unique
class Side(Enum):
    BUY = 0
    SELL = 1


def read_markets_json(market_fp=None):
    print('Read')
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        mkts = json.load(fp)
    return mkts


def asset_dict(markets):
    asset_data_dict = dict()
    for mkt in markets.values():
        mkt_dict = {'mkt_id': mkt['id']}
        pairs = [(k, dict(v, **mkt_dict)) for k, v in mkt['assets'].items()]
        asset_data_dict.update(pairs)
    return asset_data_dict
