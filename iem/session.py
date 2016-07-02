from urllib.parse import urlencode

import numpy as np
import pandas as pd
import requests

import iem
from iem.order import Bundle, Single


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
        data = urlencode(dict(logout=''))
        return self._session.get(url=_build_url('TraderLogin.action?' + data))

    def market_orderbook(self, market):
        url = _build_url('MarketTrader.action')
        data = {'market': market.value}
        ob_df = self._post_frame(url, data, **dict(index_col=iem.CONTRACT))
        return clean_orderbook_frame(ob_df)

    def asset_holdings(self, contract):
        url = _build_url('TraderActivity.action')
        data = {
            'market': contract.market,
            'asset': contract.asset_id,
            'activityType': 'holdings',
            'viewAssetHoldings': 25,  # Number of transactions? Required?
        }
        return self._post_frame(url, data, **dict(parse_dates=['Date']))

    def asset_outstanding_orders(self, contract, side):
        url = _build_url('TraderActivity.action')
        data = {
            'market': contract.market,
            'asset': contract.asset_id,
            'activityType': side,
            'viewAssetHoldings': 1,  # Required?
        }
        date_cols = [iem.ORDER_DATE, iem.EXPIRATION]
        return self._post_frame(url, data, **dict(parse_dates=date_cols))

    def place_order(self, order):
        if type(order) == Single and order.price_time_limit is not None:
            return self.place_limit_order(order)
        elif type(order) == Bundle:
            return self.place_bundle_order(order)
        elif type(order) == Single and order.price_time_limit is None:
            pass
            # return self.place_market_order(order)

    def place_limit_order(self, order):
        url = _build_url('order/LimitOrder.action')
        data = {
            'limitOrderAssetToMarket': order.contract.asset_to_market,
            'orderType': limit_order_type(order.side),
            'expirationDate': order.price_time_limit.expiration,
            'price': '{:.2f}'.format(order.price_time_limit.price),
            'limitOrderQuantity': order.quantity,
            'placeLimitOrder': 'Place Limit Order',
            'market': order.contract.market,
        }
        return self._post_frame(url, data)

    def place_bundle_order(self, order):
        url = _build_url('order/BundleOrder.action')
        data = {
            'bundle': order.contract_bundle.bundle_id,
            'orderType': bundle_order_type(order.side, order.counterparty),
            'bundleOrderQuantity': order.quantity,
            'placeBundleOrder': 'Place Bundle Order',
            'market': order.contract_bundle.market,
        }
        return self._post_frame(url=url, data=data)

    def place_market_order(self, order):
        url = _build_url('order/MarketOrder.action')
        data = {
            'marketOrderAssetToMarket': order.contract.asset_to_market,
            'orderType': market_order_type(order.side),
            'marketOrderQuantity': order.quantity,
            'placeMarketOrder': 'Place Market Order',
            'market': order.contract.market,
        }
        response = self._session.post(url=url, data=data)
        return response

    def cancel_order(self, order):
        data = {
            'cancelBidOrder': '',
            'market': order.contract.market,
            'bidOrder': order.id,
            'asset': order.contract.asset_id,
            'activityType': limit_order_type(order.side),
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


def market_order_type(side):
    return 'buy' if side == iem.Side.BUY else 'sell'


def limit_order_type(side):
    return 'bid' if side == iem.Side.BUY else 'ask'


def bundle_order_type(side, counterparty):
    if side == iem.Side.SELL:
        return ''
    else:
        return 'buyAtFixed' if counterparty.Exchange else 'buyAtMarketAskPrice'


def clean_orderbook_frame(df):
    cols = df.columns.tolist()[2:]
    own = 'Own '
    for best in [iem.BEST_ASK, iem.BEST_BID]:  # Ordered for prepend
        best_cols = [best, own + best]
        best_columns = dict((i, v) for i, v in enumerate(best_cols))
        best_df = best_price_frame(df[best]).rename(columns=best_columns)
        df[best_cols] = best_df
        cols = best_cols + cols  # Prepend
    return df[cols]


def best_price_frame(srs):
    df = srs.str.split(pat=' ', n=1, expand=True)
    if len(df.columns) == 1:  # Handle no own best order
        df[1] = None
    to_replace = {0: {'--': np.nan}, 1: {None: False, '*': True}}
    df.replace(to_replace=to_replace, inplace=True)
    df[0] = df[0].astype(float)
    return df
