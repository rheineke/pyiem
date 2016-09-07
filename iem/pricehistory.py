"""Iowa Electronic Exchange Daily price history"""

import datetime as dt
import itertools

import numpy as np
import pandas as pd
import requests

import iem


def full_price_history_frame(mkt_id):
    return pd.concat(_full_price_history_frames(mkt_id))


def _full_price_history_frames(mkt_id):
    month_year_iter = history_dates(mkt_id=mkt_id)
    dfs = []
    for m, y in month_year_iter:
        # TODO: Handle future combinations
        dfs.append(price_history_frame(mkt_id, m, y))
    return dfs


def price_history_frame(mkt_id, year, month):
    """Returns price history as a DataFrame"""
    url = _build_url('PriceHistory_GetData.cfm')
    data = dict(Market_ID=mkt_id, Month='{:02d}'.format(month), Year=year)
    response = requests.post(url=url, data=data)
    index_cols = [iem.DATE, iem.CONTRACT]
    kwargs = dict(header=0, parse_dates=[iem.DATE], index_col=index_cols)
    try:
        dfs = pd.read_html(response.text, **kwargs)
    except ValueError:
        dfs = [pd.DataFrame()]

    # Expect a MultiIndex with datetime and string levels
    # Expect a singleton list
    assert len(dfs) == 1

    return dfs[0]


def history_dates(mkt_id):
    url = _build_url('pricehistory_selectcontract.cfm')
    response = requests.get(url=url, params={'Market_ID': mkt_id})
    dfs = pd.read_html(response.text, index_col=0)

    # Expect a singleton list
    assert len(dfs) == 1

    df = dfs[0]

    mon_str = df.ix['Month:'][1]
    months = [dt.datetime.strptime(s[:3], '%b').month for s in mon_str.split()]
    year_str = df.ix['Year'][1]
    years = [int(s) for s in year_str.split()]

    return itertools.product(years, months)


def _build_url(path):
    return ''.join([iem.LEGACY_URL, 'pricehistory/', path])


# TODO: Move to strategy module
def agg_frame(df):
    notnull_label = px_hist_df[iem.UNITS] != 0
    c_gb = px_hist_df.loc[notnull_label].groupby(level=iem.CONTRACT)
    agg_arg = {
        iem.LOW_PX: np.min,
        iem.HIGH_PX: np.max,
        iem.UNITS: np.sum,
        iem.DVOL: np.sum,
        iem.LST_PX: lambda s: s.ix[-1],
    }
    agg_df = c_gb.agg(arg=agg_arg)
    agg_df[iem.AVG_PX] = agg_df[iem.DVOL].div(agg_df[iem.UNITS]).round(3)
    return agg_df


if __name__ == '__main__':
    mkt = iem.Market('Congress16')
    mkt_id = mkt.value
    # year = 2016
    # month = 6
    # px_hist_df = price_history_frame(mkt_id, year, month)
    px_hist_df = full_price_history_frame(mkt_id)

    agg_df = agg_frame(px_hist_df)

