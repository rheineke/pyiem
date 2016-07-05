import pandas as pd

import iem
from iem import operator

MOST_INSIDE_BUNDLE_PRICE = (0.9, 1.005)


def best_price_frame(orderbook_df, most_inside_bundle_prices=None):
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
    return order_df.reset_index(level=0, drop=True)


def nonarbitrage_group(group, most_inside_bundle_prices):
    bundle_bid, bundle_ask = bundle_sums(group)
    nonarb_group = group.copy()
    mi_bid, mi_ask = most_inside_bundle_prices
    bid_cond = pd.Series(data=bundle_bid <= mi_bid, index=group.index)
    nonarb_group[iem.BID] = nonarb_group[iem.BID].where(bid_cond)
    ask_cond = pd.Series(data=bundle_ask >= mi_ask, index=group.index)
    nonarb_group[iem.ASK] = nonarb_group[iem.ASK].where(ask_cond)
    return nonarb_group


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
    px_col = iem.best_price_name(side)
    best_px_srs = operator.move_inside(side)(orderbook_df[px_col], iem.TICK)
    best_px_srs.fillna(iem.most_outside_price(side), inplace=True)
    opp_px_col = iem.best_price_name(side.opposite())
    opp_mo_px = iem.most_outside_price(opp_px_col)
    curr_opp_px_srs = orderbook_df[opp_px_col].fillna(opp_mo_px)
    outside_label = operator.outside(side)(best_px_srs, curr_opp_px_srs)
    return best_px_srs.where(outside_label)
