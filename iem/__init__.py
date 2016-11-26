"""Core classes and constants for the Iowa Electronic Market

Public attributes:
- Market
- contract
"""

from enum import Enum, unique

# Iowa Electronic Market URLs
URL = 'https://iem.uiowa.edu/iem/'
LEGACY_URL = 'https://iemweb.biz.uiowa.edu/'

# Iowa Electronic Market defined names
AVG_PX = 'AvgPrice'
CANCEL_ORDER = 'Cancel Order'
CONTRACT = 'Contract'
DATE = 'Date'
DOLLAR_VOLUME = '$Volume'
EXPIRATION = 'Expiration'
EXPIRATION_DATE = 'Expiration Date'
HIGH_PX = 'HighPrice'
LOW_PX = 'LowPrice'
LST_PX = 'LastPrice'
MAX_CONTRACTS = 'Max Contracts Held'
NET_POS = 'Net Position'
ORDER_DATE = 'Order Date'
PROFIT = 'Profit'
QUANTITY_HELD = 'Quantity Held'
SGN_ACTION = 'Signed Action'
SGN_QTY = 'Signed Quantity'
SYMBOL = 'Symbol'
TRADE_ID = 'Trade ID'
TRADE_TYPE = 'Trade Type'
UNIT_PX = 'Unit Price'
UNITS = 'Units'
VOL = 'Units'
YOUR_ASKS = 'Your Asks'
YOUR_BIDS = 'Your Bids'

# Locally defined names
TIMESTAMP = 'Timestamp'

ASK = 'ask'
BID = 'bid'


@unique
class Side(Enum):
    BUY = 0
    SELL = 1

    # def __repr__(self):
    #     return 'buy' if self == self.BUY else 'sell'

    def __str__(self):
        return 'buy' if self is self.BUY else 'sell'
