"""Iowa Electronic Markets price history"""
import datetime as dt
import itertools

import numpy as np
import pandas as pd
import pytz
import requests

import iem
from iem.contract import Market

NAME = 'daily_price_history'

def full_price_history_frame(mkt_id):
    return pd.concat(full_price_history_frames(mkt_id))


def full_price_history_frames(mkt_id):
    month_year_iter = history_dates(mkt_id=mkt_id)
    dfs = []
    for m, y in month_year_iter:
        # TODO(rheineke): Handle future combinations
        dfs.append(price_history_frame(mkt_id, m, y))
    return dfs


def price_history_frame(mkt_id, year, month):
    """Returns price history as a DataFrame"""
    url = _build_url('pricehistory/PriceHistory_GetData.cfm')
    data = dict(Market_ID=mkt_id, Month='{:02d}'.format(month), Year=year)
    response = requests.post(url=url, data=data)
    index_cols = [iem.DATE, iem.CONTRACT]
    kwargs = dict(header=0, parse_dates=[iem.DATE], index_col=index_cols)
    dfs = pd.read_html(response.text, **kwargs)

    # Expect a singleton list
    assert len(dfs) == 1

    return dfs[0]


def history_dates(mkt_id):
    url = _build_url('pricehistory/pricehistory_selectcontract.cfm')
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
    return ''.join([iem.LEGACY_URL, path])


# TODO: Move to strategy module
def agg_frame(px_hist_df):
    notnull_label = px_hist_df[iem.UNITS] != 0
    c_gb = px_hist_df.loc[notnull_label].groupby(level=iem.CONTRACT)
    agg_arg = {
        iem.LOW_PX: np.min,
        iem.HIGH_PX: np.max,
        iem.UNITS: np.sum,
        iem.DVOL: np.sum,
        iem.LST_PX: lambda s: s.ix[-1],
    }
    df = c_gb.agg(arg=agg_arg)
    df[iem.AVG_PX] = df[iem.DVOL].div(df[iem.UNITS]).round(3)
    return df


def read_quote_frame(mkt_id):
    url = _build_url('quotes/{}.html'.format(mkt_id))
    response = requests.get(url=url)
    dfs = pd.read_html(response.text, index_col=0, header=0, na_values=['---'])

    # Expect a singleton list
    assert len(dfs) == 1

    df = dfs[0]

    # Append timestamp
    df[iem.TIMESTAMP] = _timestamp(response.text)

    return df.reset_index().set_index([iem.TIMESTAMP, iem.SYMBOL])


def _timestamp(text):
    # Assume first bold entry is the datetime string
    start_idx = text.find('<B>') + len('<B>')
    end_idx = text.find('</B>')
    ts_str = text[start_idx:end_idx]
    # Split into time, timezone, and date strings
    time_str, raw_zone, date_str = ts_str.split(' ', 2)
    dt_str = time_str + ', ' + date_str
    # tz-naive timestamp
    naive_ts = pd.to_datetime(dt_str, format='%H:%M:%S, %A, %B %d, %Y')
    # Replace tz_str with something recognized by pytz
    tz_dict = {'CST': 'US/Central'}
    clean_zone = raw_zone[:-1]
    zone = tz_dict.get(clean_zone, clean_zone)
    tz = pytz.timezone(zone)
    # Return tz-aware timestamp
    return naive_ts.tz_localize(tz)


if __name__ == '__main__':
    mkt_id = Market('FedPolicyB').id
    # year = 2016
    # month = 6
    # px_hist_df = price_history_frame(mkt_id, year, month)
    # px_hist_df = full_price_history_frame(mkt_id)
    # agg_df = agg_frame(px_hist_df)
    quote_df = read_quote_frame(mkt_id)
    print(quote_df)

