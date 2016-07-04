import json

import pandas as pd

import iem
from iem.contract import Contract, Market
from iem.session import Session

TICK = .001
MAX_PRICE = 1
MIN_PRICE = 0
MOST_INSIDE_BUNDLE_PRICE = (0.9, 1.005)


def rest_best_price_frame(orderbook_df, most_inside_bundle_prices=None):
    # Filter out prices using resting limit order prices
    order_df = next_best_rest_price_frame(orderbook_df)
    # Filter out own best orders
    bb_srs = order_df[iem.BID].where(~orderbook_df[iem.OWN_BEST_BID])
    order_df[iem.BID] = bb_srs
    ba_srs = order_df[iem.ASK].where(~orderbook_df[iem.OWN_BEST_ASK])
    order_df[iem.ASK] = ba_srs
    # Filter out bundle arbitrages
    df = orderbook_df.join(order_df)
    bundle_gb = df.groupby(bundle)
    if most_inside_bundle_prices is None:
        most_inside_bundle_prices = MOST_INSIDE_BUNDLE_PRICE
        kwargs = {'most_inside_bundle_prices': most_inside_bundle_prices}
    order_df = bundle_gb.apply(nonarbitrage_group, **kwargs)
    return order_df


def nonarbitrage_group(group, most_inside_bundle_prices):
    bundle_bid, bundle_ask = bundle_sums(group)
    nonarb_group = group.copy()
    mi_bid, mi_ask = most_inside_bundle_prices
    bid_cond = pd.Series(data=bundle_bid <= mi_bid, index=group.index)
    nonarb_group[iem.BID] = nonarb_group[iem.BID].where(bid_cond)
    ask_cond = pd.Series(data=bundle_ask >= mi_ask, index=group.index)
    nonarb_group[iem.ASK] = nonarb_group[iem.ASK].where(ask_cond)
    return nonarb_group


def bundle_sum_series(group):
    bid_px, ask_px = bundle_sums(group)
    return pd.Series(data=[bid_px, ask_px], index=[iem.BID, iem.ASK])


def bundle_sums(group):
    bundle_bid_px = group[[iem.BEST_BID, iem.BID]].max(axis=1).sum()
    bundle_ask_px = group[[iem.BEST_ASK, iem.ASK]].min(axis=1).sum()
    return bundle_bid_px, bundle_ask_px


def bundle(contract_name):
    if contract_name.startswith('FR'):
        return contract_name[-4:]
    else:
        return contract_name


def next_best_rest_price_frame(orderbook_df):
    order_df = pd.DataFrame(index=orderbook_df.index)
    order_df[iem.BID] = _next_best_rest_series(iem.Side.BUY, orderbook_df)
    order_df[iem.ASK] = _next_best_rest_series(iem.Side.SELL, orderbook_df)
    return order_df


def _next_best_rest_series(side, orderbook_df):
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
