import json

import iem
from iem.session import Session
from iem.config import read_login
from iem.order import PriceTimeLimit, Single
from iem import Side

if __name__ == '__main__':
    login_kwargs = read_login()
    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Get Orderbook dataframe
    ob_df = sess.market_orderbook(iem.Market.RCONV16)
    # Get order activity
    asset = iem.RConv16.TRUM_NOM
    # oa_df = sess.asset_holdings(asset)
    # Get outstanding orders
    oo_df = sess.asset_outstanding_orders(asset, iem.BID)
    # Send order
    # contract = 3037  # RCONV16.TRUMP_NOM
    # price_time_limit = PriceTimeLimit(.25, '20161102')
    # o = Single(contract, Side.BUY, 1, price_time_limit)
    # latest_ob_df = sess.place_order(o)
    logout_response = sess.logout()
