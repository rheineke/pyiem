import json

import pandas as pd

import iem
from iem.contract import Contract, Market
from iem.session import Session

TICK = .001
MAX_PRICE = 1
MIN_PRICE = 0


def rest_best_price_frame(orderbook_df):
    order_df = next_best_price_frame(orderbook_df)
    bb_srs = order_df[iem.BEST_BID].where(~orderbook_df[iem.OWN_BEST_BID])
    order_df[iem.BEST_BID] = bb_srs
    ba_srs = order_df[iem.BEST_ASK].where(~orderbook_df[iem.OWN_BEST_ASK])
    order_df[iem.BEST_ASK] = ba_srs
    return order_df


def next_best_price_frame(orderbook_df):
    order_df = pd.DataFrame(index=orderbook_df.index)
    order_df[iem.BEST_BID] = _next_best_price_series(iem.Side.BUY, orderbook_df)
    order_df[iem.BEST_ASK] = _next_best_price_series(iem.Side.SELL, orderbook_df)
    return order_df


def _next_best_price_series(side, orderbook_df):
    px_col = price_name(side)
    next_best_px_srs = move_inside(side, orderbook_df[px_col], TICK)
    next_best_px_srs.fillna(most_outside_price(side), inplace=True)
    opp_px_col = price_name(side.opposite())
    opp_mo_px = most_outside_price(opp_px_col)
    curr_opp_px_srs = orderbook_df[opp_px_col].fillna(opp_mo_px)
    outside_label = is_outside(side, next_best_px_srs, curr_opp_px_srs)
    return next_best_px_srs.where(outside_label)


def move_inside(side, px_srs, increment):
    return px_srs + increment if side is iem.Side.BUY else px_srs - increment


def most_outside_price(side):
    return MIN_PRICE if side is iem.Side.BUY else MAX_PRICE


def price_name(side):
    return iem.BEST_BID if side is iem.Side.BUY else iem.BEST_ASK


def is_outside(side, srs, other):
    return srs < other if side is iem.Side.BUY else srs > other

if __name__ == '__main__':
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Get Orderbook dataframe
    mkt = Market('FedPolicyB')
    ob_df = sess.market_orderbook(mkt)
    # Get order activity
    contract = Contract('FRsame0616')
    oa_df = sess.asset_holdings(contract)
    # Get outstanding orders
    oo_df = sess.asset_outstanding_orders(contract, iem.BID)
    # Log out
    logout_response = sess.logout()

    rest_best_px_df = rest_best_price_frame(ob_df)
