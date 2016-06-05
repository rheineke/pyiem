import json

import pandas as pd

from iem.session import Session

if __name__ == '__main__':
    with open('../conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Get Orderbook
    mkt_url = sess.build_url('MarketTrader.action')
    mkt_data = {
        'market': 364,
        # 'selectMarket': 'Start trading',
        # 'sourcePage': '',
    }
    market_response = sess._session.post(url=mkt_url, data=mkt_data)
    ob_df = pd.read_html(market_response.text, index_col=iem.CONTRACT)[0]
    # Get order activity
    activity_url = sess.build_url('TraderActivity.action')
    activity_data = {
        'market': 364,
        'asset': 3037,
        'activityType': 'holdings',
        'viewAssetHoldings': 25,  # Number of transactions?
        # 'sourcePage': '',
    }
    activity_response = sess._session.post(url=activity_url, data=activity_data)
    activity_dfs = pd.read_html(activity_response.text, parse_dates=['Date'])
    # Get outstanding orders
    oo_data = {
        'market': 360,
        'asset': 3017,
        'activityType': 'bid',
        'viewAssetHoldings': 1,
    }
    oo_response = sess._session.post(url=activity_url, data=oo_data)
    oo_dfs = pd.read_html(oo_response.text, parse_dates=['Order Date', 'Expiration'])
    logout_response = sess.logout()