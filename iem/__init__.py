"""Core classes and constants for the Iowa Electronic Market

Public attributes:
- Market
- contract
"""

from enum import Enum, unique

__author__ = 'rheineke'

CONTRACT = 'Contract'
DVOL = '$Volume'
HIGH_PX = 'HighPrice'
LOW_PX = 'LowPrice'
LST_PX = 'LastPrice'
MAX_CONTRACTS = 'Max Contracts Held'
NET_POS = 'Net Position'
PROFIT = 'Profit'
SGN_ACTION = 'Signed Action'
SGN_QTY = 'Signed Quantity'
TRADE_ID = 'Trade ID'
TRADE_TYPE = 'Trade Type'
UNIT_PX = 'Unit Price'
VOL = 'Units'

OLD_URL = 'iemweb.biz.uiowa.edu'
URL = 'iem.uiowa.edu/iem'


@unique
class Market(Enum):
    """
    IEM numeric designation for each market. A market contains a set of
    arbitrageable contracts
    """
    Congress16 = 360
    PRES16_VS = 361
    PRES16_WTA = 362
    RCONV16 = 364
    # DCONV16 = 365


@unique
class Congress16(Enum):
    DH_DS16 = 3014
    RH_DS16 = 3015
    DH_RS16 = 3016
    RH_RS16 = 3017
    OTHER16 = 3018


@unique
class RConv16(Enum):
    CARS_NOM = 0
    CRUZ_NOM = 1
    RROF_NOM = 2
    RUBI_NOM = 3
    TRUM_NOM = 3037


def market_contract_assets(market):
    if type(market) == str:
        mkt_assets = {
            Market.Congress16.name: Congress16,
        }
    else:
        mkt_assets = {
            Market.Congress16: Congress16,
        }
    return mkt_assets[market]