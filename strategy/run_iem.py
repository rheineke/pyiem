import datetime as dt
import json
from collections import OrderedDict

import numpy as np
import pandas as pd

import iem
from iem import operator, Market
from iem.contract import Contract
from iem.session import Session
from iem.order import PriceTimeLimit, Single
from strategy import make


def strategy_price_limit_frame(market):
    json_fp = 'conf/strategy_{}.json'.format(market.name)
    return pd.read_json(json_fp, orient='index')


def strategy_best_price_frame(best_px_df, strategy_best_px_df):
    order_df = best_px_df.copy()
    # Best bid
    strat_bb_srs = strategy_best_px_df[iem.BID]
    bb_srs = best_px_df[iem.BID]
    bid_cond = operator.outside(iem.Side.BUY)(bb_srs, strat_bb_srs)
    order_df[iem.BID] = bb_srs.where(bid_cond)
    # Best ask
    strat_ba_srs = strategy_best_px_df[iem.ASK]
    ba_srs = best_px_df[iem.ASK]
    ask_cond = operator.outside(iem.Side.SELL)(ba_srs, strat_ba_srs)
    order_df[iem.ASK] = ba_srs.where(ask_cond)
    return order_df


def generate_orders(price_df, qty):
    os = []
    os += _side_orders(iem.Side.BUY, price_df)
    os += _side_orders(iem.Side.SELL, price_df)
    return os


def _side_orders(side, price_df):
    qty = 1
    px_col = iem.price_name(side)
    os = []
    for contract_name, px in price_df[px_col].items():
        if pd.isnull(px):
            continue
        c = Contract(contract_name)
        ptl = PriceTimeLimit(price=px, expiration=expiry(c))
        o = Single(contract=c, side=side, quantity=qty, price_time_limit=ptl)
        os.append(o)
    return os


def expiry(contract):
    # TODO: Optimize
    return '2016/07/26 23:59 PM'
    # return dt.date(2016, 7, 26)


if __name__ == '__main__':
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    print(login_response.request)
    # Get Orderbook dataframe
    mkt = Market('FedPolicyB')
    ob_df = sess.market_orderbook(mkt)
    # Get order activity
    # contract = Contract('FRsame0616')
    # oa_df = sess.asset_holdings(contract)
    # Get outstanding orders
    # oo_df = sess.asset_outstanding_orders(contract, iem.BID)
    # Send resting limit orders
    # rest_best_px_df = make.best_price_frame(ob_df)
    # TODO: Use dynamic traded prices to adjust limit orders
    # TODO: Use fixed prices until dynamic prices can be determined
    # strat_df = strategy_price_limit_frame(mkt)
    # strat_best_px_df = strategy_best_price_frame(rest_best_px_df, strat_df)
    # orders = generate_orders(strat_best_px_df, qty=1)
    # print(orders)
    # order_responses = []
    # for order in orders:
    #     order_responses.append(sess.place_limit_order(order))
    # Log out
    logout_response = sess.logout()


