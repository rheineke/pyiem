import json

import iem
from iem.contract import Contract, Market
from iem.session import Session

if __name__ == '__main__':
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Get Orderbook dataframe
    mkt = Market('RCONV16')
    ob_df = sess.market_orderbook(mkt)
    # Get order activity
    contract = Contract('TRUM_NOM')
    oa_df = sess.asset_holdings(contract)
    # Get outstanding orders
    oo_df = sess.asset_outstanding_orders(contract, iem.BID)
    # Log out
    logout_response = sess.logout()
