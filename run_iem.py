import json

import iem
from iem.session import Session

if __name__ == '__main__':
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Get Orderbook dataframe
    ob_df = sess.market_orderbook(iem.Market.RCONV16)
    # Get order activity
    asset = iem.RConv16.TRUM_NOM
    oa_df = sess.asset_holdings(asset)
    # Get outstanding orders
    oo_df = sess.asset_outstanding_orders(asset, iem.BID)
    logout_response = sess.logout()
