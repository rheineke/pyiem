import json

import iem
from iem.session import Session

if __name__ == '__main__':
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Get Orderbook dataframe
    mkt = iem.Market.RCONV16
    ob_df = sess.market_orderbook(mkt)
    # Get order activity
    asset = iem.RConv16.TRUM_NOM
    oa_df = sess.asset_holdings(mkt, asset)
    # Get outstanding orders
    oo_df = sess.asset_outstanding_orders(mkt, asset, iem.BID)
    logout_response = sess.logout()
