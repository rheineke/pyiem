"""Iowa Electronic Markets session. All queries requiring login credentials are
handled by the session object"""
# Python 2 and 3:
from __future__ import print_function

from collections import defaultdict

from lxml import etree
from urllib.parse import urlencode, parse_qs

import pandas as pd
import requests

import iem
from iem.config import read_markets
from iem.order import Single, Bundle, to_string


class Session:
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self._logger = None
        # Start session
        self._session = requests.Session()
        # Lookup tables
        self._market_asset_dict = read_markets()
        self._asset_market_dict = _asset_market_dict(self._market_asset_dict)
        self._order_market_dict = _order_market_dict(self._market_asset_dict)

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

    def orderbook(self, market):
        url = _build_url('MarketTrader.action')
        data = {'market': market.id}
        response = self._session.post(url=url, data=data)

        df = _frame(response, **dict(index_col=iem.CONTRACT))
        alt_df = _orderbook_tag_frame(response.text)
        return df.combine_first(alt_df)

    def holdings(self, contract):
        url = _build_url('TraderActivity.action')
        data = {
            'market': contract.market.id,  # 51
            'asset': contract.asset_id,  # 3054
            'activityType': 'holdings',
            # 'viewAssetHoldings': 25,  # Net position. Required?
            # '_sourcePage': '',
            # '_fp': '',
        }
        kwargs = dict(index_col=iem.DATE, parse_dates=[iem.DATE])
        return self._post_frame(url=url, data=data, read_html_kwargs=kwargs)

    def outstanding_orders(self, contract, side):
        url = _build_url('TraderActivity.action')
        data = {
            'market': contract.market.id,  # 51
            'asset': contract.asset_id,  # 3056
            'activityType': side,
            # 'viewAssetHoldings': 1,  # Number of open orders. Required?
        }
        response = self._session.post(url=url, data=data)

        date_cols = [iem.ORDER_DATE, iem.EXPIRATION]
        kwargs = dict(index_col=iem.ORDER_DATE, parse_dates=date_cols)
        # return self._post_frame(url=url, data=data, read_html_kwargs=kwargs)

        df = _frame(response, **kwargs)
        oid_df = _order_id_tag_frame(response.text)
        cxl_o = iem.CANCEL_ORDER
        df[cxl_o] = df[cxl_o].combine_first(oid_df[cxl_o])
        return df

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
            'limitOrderAssetToMarket': order.contract.asset_to_market_id,  # 285
            'orderType': order_type(order.side),  # 'bid'
            'expirationDate': to_string(order.price_time_limit.expiration),
            'price': '{:.3f}'.format(order.price_time_limit.price),  # '0.251'
            'limitOrderQuantity': order.quantity,  # '1',
            'placeLimitOrder': 'Place Limit Order',
            'market': self._order_market_dict[order.contract],  # '364'
        }
        return self._post_frame(url=url, data=data)

    def place_bundle_order(self, order):
        url = _build_url('order/BundleOrder.action')
        data = {
            'bundle': order.contract_bundle.id,
            'orderType': bundle_order_type(order.side, order.counterparty),
            'bundleOrderQuantity': order.quantity,
            'placeBundleOrder': 'Place Bundle Order',
            'market': order.contract_bundle.market.id,
        }
        return self._post_frame(url=url, data=data)

    def place_market_order(self, order):
        url = _build_url('order/MarketOrder.action')
        data = {
            'marketOrderAssetToMarket': order.contract.asset_to_market_id,
            'orderType': str(order.side),
            'marketOrderQuantity': order.quantity,
            'placeMarketOrder': 'Place Market Order',
            'market': order.contract.market.id,
        }
        response = self._session.post(url=url, data=data)
        return response

    def cancel_order(self, order):
        side_str = order_type(order.side)
        data = {
            'cancel{}Order'.format(side_str.capitalize()): '',
            'market': order.contract.market.id,
            (side_str + 'Order'): order.id,
            'asset': order.contract.asset_id,
            'activityType': side_str,
        }
        url = _build_url('TraderActivity.action?' + urlencode(data))
        response = self._session.get(url)  # Almost certainly wrong
        return response

    def messages(self, market):
        data = {
            'home': '',
            'market': market.id,
        }
        url = _build_url('TraderMessages.action?' + urlencode(data))
        date_cols = [iem.DATE, iem.EXPIRATION_DATE]
        kwargs = dict(index_col=iem.DATE, parse_dates=date_cols)
        return self._get_frame(url=url, read_html_kwargs=kwargs)

    def _post_frame(self, url, data, read_html_kwargs=None):
        if read_html_kwargs is None:
            read_html_kwargs = {}
        # Use this in all the various function calls
        response = self._session.post(url=url, data=data)
        return _frame(response, **read_html_kwargs)

    def _get_frame(self, url, read_html_kwargs):
        # Use this in all the various function calls
        response = self._session.get(url=url)
        return _frame(response, **read_html_kwargs)


def _frame(response, **kwargs):
    print(response.text)
    dfs = pd.read_html(response.text, **kwargs)

    # Expect a singleton list
    assert len(dfs) == 1

    return dfs[0]


def _build_url(path):
    return ''.join([iem.URL, 'trader/', path])


def order_type(side):
    return 'bid' if side == iem.Side.BUY else 'ask'


def bundle_order_type(side, counterparty):
    is_exch = counterparty is counterparty.Exchange
    if side == iem.Side.SELL:
        return 'sellAtFixed' if is_exch else 'sellAtMarketBidPrice'
    else:
        return 'buyAtFixed' if is_exch else 'buyAtMarketAskPrice'


def _num_open_orders(tr_elem, klass):
    td = tr_elem.find(path="td[@class='{}']".format(klass))
    form = td.find('form')
    if form is None:
        return pd.to_numeric(td.text)
    else:
        val = form.find(path="input[@name='viewAssetHoldings']").attrib['value']
        return pd.to_numeric(val)


def _table_text(text):
    start_idx = text.index('<table')
    tbl = '</table>'
    end_idx = text.index(tbl) + len(tbl)
    return text[start_idx:end_idx]


def _orderbook_tag_frame(text):
    # This function can be removed if this pandas feature request is implemented
    # https://github.com/pandas-dev/pandas/issues/14608
    table_str = _table_text(text)
    root = etree.fromstring(table_str)
    table_body = root.find('tbody')
    index = []
    data = defaultdict(list)
    # Iterator of tr objects
    qty_path = "td[@class='change-cell quantity']"
    tr_iter = table_body.iter(tag='tr')
    for tr in tr_iter:
        index.append(tr.find(path='td').text.strip())
        # Quantity Held
        pos = pd.to_numeric(tr.find(path=qty_path).attrib['value'])
        data[iem.QUANTITY_HELD].append(pos)
        # Your Bids
        data[iem.YOUR_BIDS].append(_num_open_orders(tr, 'yourBidsCell'))
        # Your Asks
        data[iem.YOUR_ASKS].append(_num_open_orders(tr, 'yourAsksCell'))

    return pd.DataFrame(data=data, index=index)


def _order_id_tag_frame(text):
    root = etree.fromstring(_table_text(text))
    tbody = root.find('tbody')
    index_data = []
    data = defaultdict(list)
    for tr in tbody.iter(tag='tr'):
        index_data.append(pd.to_datetime(tr.find('td').text))
        a = tr.find('td/a')
        href = parse_qs(a.attrib['href'])
        data[iem.CANCEL_ORDER].append(float(href['bidOrder'][0]))
    index_data = pd.DatetimeIndex(data=index_data, name=iem.ORDER_DATE)
    return pd.DataFrame(data=data, index=index_data)


def _asset_market_dict(markets):
    asset_mkt_dict = dict()
    for mkt in markets.values():
        bundles = mkt['bundle']
        if 'assets' in bundles:
            assets = bundles['assets'].values()
            asset_mkt_dict.update([(a['id'], mkt['id']) for a in assets])
        else:
            for bundle in bundles.values():
                assets = bundle['assets'].values()
                asset_mkt_dict.update([(a['id'], mkt['id']) for a in assets])
    return asset_mkt_dict


def _order_market_dict(markets):
    asset_mkt_dict = dict()
    for mkt in markets.values():
        bundles = mkt['bundle']
        if 'assets' in bundles:
            assets = bundles['assets'].values()
            asset_mkt_dict.update([(a['order'], mkt['id']) for a in assets])
        else:
            for bundle in bundles.values():
                assets = bundle['assets'].values()
                asset_mkt_dict.update([(a['order'], mkt['id']) for a in assets])
    return asset_mkt_dict
