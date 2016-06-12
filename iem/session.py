import json
from urllib.parse import urlencode

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
        # Lookup tables
        self._market_asset_dict = _read_markets_json()
        self._asset_market_dict = _asset_market_dict(self._market_asset_dict)

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
        data = urlencode(dict(logout=''))
        return self._session.get(url=_build_url('TraderLogin.action?' + data))

    def market_orderbook(self, market):
        url = _build_url('MarketTrader.action')
        data = {'market': market.value}
        return self._post_frame(url, data, **dict(index_col=iem.CONTRACT))

    def asset_holdings(self, asset):
        url = _build_url('TraderActivity.action')
        data = {
            'market': self._asset_market_dict[asset.value],
            'asset': asset.value,
            'activityType': 'holdings',
            'viewAssetHoldings': 25,  # Number of transactions? Required?
        }
        return self._post_frame(url, data, **dict(parse_dates=['Date']))

    def asset_outstanding_orders(self, asset, side):
        url = _build_url('TraderActivity.action')
        data = {
            'market': self._asset_market_dict[asset.value],
            'asset': asset.value,
            'activityType': side,
            'viewAssetHoldings': 1,  # Required?
        }
        date_cols = [iem.ORDER_DATE, iem.EXPIRATION]
        return self._post_frame(url, data, **dict(parse_dates=date_cols))

    def place_order(self, order):
        # 'MarketOrder.action'
        url = _build_url('order/LimitOrder.action')
        data = {
            'limitOrderAssetToMarket': 285,
            'orderType': 'bid',
            'expirationDate': '2016/11/02 11:59 PM',  # '%Y/%m/%d %H:%M %p'
            'price': '0.251',  # '{:1.2f}'
            'limitOrderQuantity': '1',
            'placeLimitOrder': 'Place Limit Order',
            'market': '364'
        }
        return self._post_frame(url, data)

    def place_market_order(self, order):
        url = _build_url('order/MarketOrder.action')
        data = {
            'marketOrderAssetToMarket': 285,
            'orderType': 'buy',
            'marketOrderQuantity': '1',
            'placeMarketOrder': 'Place Market Order',
            'market': 364,
        }
        response = self._session.post(url=url, data=data)
        return response

    def cancel_order(self, order):
        data = {
            'cancelBidOrder': '',
            'market': '364',
            'bidOrder': '4602237',
            'asset': '3037',
            'activityType': 'bid',
        }
        url = _build_url('TraderActivity.action?' + urlencode(data))
        response = self._session.get(url)
        return response

    def _post_frame(self, url, data, **kwargs):
        # Use this in all the various function calls
        response = self._session.post(url=url, data=data)
        dfs = pd.read_html(response.text, **kwargs)

        # Expect a singleton list
        assert len(dfs) == 1

        return dfs[0]


def _build_url(path):
    return ''.join([iem.URL, 'trader/', path])


def _read_markets_json(market_fp=None):
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        mkts = json.load(fp)
    return mkts


def _asset_market_dict(markets):
    asset_mkt_dict = dict()
    for mkt in markets.values():
        asset_mkt_dict.update([(a, mkt['id']) for a in mkt['assets'].values()])
    return asset_mkt_dict
