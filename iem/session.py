import pandas as pd
import requests

import iem


class Session:
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self._logger = None
        # Start session
        self._session = requests.Session()

    def authenticate(self):
        # Send login request to IEM
        data = {
            'forceLogin': False,  # Required
            'username': self._username,
            'password': self._password,
            'loginSubmit': 'Sign in',  # Required
            '_sourcePage': '',  # Required
        }

        url = _build_url('TraderLogin.action')
        return self._session.post(url=url, data=data)

    def _log(self, message):
        if self._logger:
            self._logger.write(message)

    def logout(self):
        return self._session.get(url=_build_url('TraderLogin.action?logout='))

    def market_orderbook(self, market):
        url = _build_url('MarketTrader.action')
        data = {'market': market.value}
        response = self._session.post(url=url, data=data)
        dfs = pd.read_html(response.text, index_col=iem.CONTRACT)
        return dfs[0]

    # TODO: Asset uniquely defines market, remove market
    def asset_holdings(self, market, asset):
        url = _build_url('TraderActivity.action')
        data = {
            'market': market.value,
            'asset': asset.value,
            'activityType': 'holdings',
            'viewAssetHoldings': 25,  # Number of transactions?
        }
        response = self._session.post(url=url, data=data)
        dfs = pd.read_html(response.text, parse_dates=['Date'])
        return dfs[0]

    def asset_outstanding_orders(self, market, asset, side):
        url = _build_url('TraderActivity.action')
        oo_data = {
            'market': market.value,
            'asset': asset.value,
            'activityType': side,
            'viewAssetHoldings': 1,
        }
        response = self._session.post(url=url, data=oo_data)
        date_cols = [iem.ORDER_DATE, iem.EXPIRATION]
        dfs = pd.read_html(response.text, parse_dates=date_cols)
        return dfs[0]


def _build_url(path):
    return '{}{}'.format(iem.URL + 'trader/', path)
