"""Iowa Electronic Markets price history"""
import datetime as dt
import itertools
from collections import OrderedDict

import numpy as np
import pandas as pd
import pytz
import requests

import iem
from iem import config
from iem.contract import Market

NAME = 'daily_price_history'


def full_price_history_frame(mkt_id):
    return pd.concat(full_price_history_frames(mkt_id))


def full_price_history_frames(mkt_id):
    month_year_iter = history_dates(mkt_id=mkt_id)
    dfs = []
    for y, m in month_year_iter:
        dfs.append(price_history_frame(mkt_id, y, m))
    return dfs


def price_history_frame(mkt_id, year, month):
    """Returns price history as a DataFrame"""
    url = _build_url('pricehistory/PriceHistory_GetData.cfm')
    data = dict(Market_ID=mkt_id, Month='{:02d}'.format(month), Year=year)
    response = requests.post(url=url, data=data)
    index_cols = [iem.DATE, iem.CONTRACT]
    kwargs = dict(header=0, parse_dates=[iem.DATE], index_col=index_cols)
    try:
        dfs = pd.read_html(response.text, **kwargs)
    except ValueError:
        dfs = [pd.DataFrame()]

    # Expect a singleton list
    assert len(dfs) == 1

    # Remove duplicates, if any
    df = dfs[0]
    if len(df.index.unique()) != len(df.index):
        df = df.groupby(level=df.index.names).first()

    return df


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
        iem.DOLLAR_VOLUME: np.sum,
        iem.LST_PX: lambda s: s.ix[-1],
    }
    df = c_gb.agg(arg=agg_arg)
    df[iem.AVG_PX] = df[iem.DOLLAR_VOLUME].div(df[iem.UNITS]).round(3)
    return df


def read_quote_frame(mkt_conf):
    dfs = read_quote_frames(mkt_conf)

    # Expect a singleton list
    assert len(dfs) == 1

    return dfs[0]


def read_quote_frames(mkt_conf):
    url = _market_quote_url(mkt_conf)
    response = requests.get(url=url)
    dfs = pd.read_html(response.text, index_col=0, header=0, na_values=['---'])

    # Data outside of the HTML tables
    table_headers = _table_headers(response.text)
    market_names = [_market_name(s) for s in table_headers]
    timestamps = [_timestamp(s) for s in table_headers]

    # Modify data frames
    mod_dfs = [_modify_frame(df, ts) for df, ts in zip(dfs, timestamps)]

    return OrderedDict((nm, df) for nm, df in zip(market_names, mod_dfs))


def _market_quote_url(mkt_conf):
    rel_path = mkt_conf.get(config.QUOTES_URL, mkt_conf['id'])
    return _build_url('quotes/{}.html'.format(rel_path))


def _modify_frame(df, timestamp):
    # Append timestamp
    df[iem.TIMESTAMP] = timestamp

    return df.reset_index().set_index([iem.TIMESTAMP, iem.SYMBOL])


def _timestamp(text):
    # Assume first bold entry is the datetime string
    start_sub = 'Quotes current as of <B>'
    start_idx = text.find(start_sub) + len(start_sub)
    end_idx = text.find('</B>', start_idx)
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


def _market_name(text):
    # Assume word following 'Market Quotes:  ' is the market name
    start_sub = 'Market Quotes:  '
    start_idx = text.find(start_sub) + len(start_sub)
    end_idx = text.find('\r\n<BR>', start_idx)
    return text[start_idx:end_idx].split('.html')[0]


def _table_headers(text):
    return text.split('<TABLE')[:-1]


if __name__ == '__main__':
    snapshot_dt = pd.Timestamp(year=2016, month=12, day=30)
    mkt_id = Market('FedPolicyB').id
    # year = 2016
    # month = 6
    # px_hist_df = price_history_frame(mkt_id, year, month)
    # px_hist_df = full_price_history_frame(mkt_id)
    # agg_df = agg_frame(px_hist_df)
    mkt_conf = config.read_markets()
    active_mkt_conf = config.active_markets(mkt_conf, snapshot_dt)
    quote_dfs = read_quote_frames(active_mkt_conf['Congress18'])
    print(quote_dfs)

