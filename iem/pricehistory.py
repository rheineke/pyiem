import datetime as dt
import itertools

import pandas as pd
import requests

import iem


def full_price_history_frame(mkt_id):
    month_year_iter = history_dates(mkt_id=mkt_id)
    dfs = []
    for m, y in month_year_iter:
        # TODO: Handle future combinations
        dfs.append(price_history_frame(mkt_id, m, y))
    return pd.concat(dfs)


def price_history_frame(mkt_id, year, month):
    """Returns price history as a DataFrame"""
    url = iem.LEGACY_URL + 'pricehistory/PriceHistory_GetData.cfm'
    data = dict(Market_ID=mkt_id, Month='{:02d}'.format(month), Year=year)
    response = requests.post(url=url, data=data)
    index_cols = [iem.DATE, iem.CONTRACT]
    kwargs = dict(header=0, parse_dates=[iem.DATE], index_col=index_cols)
    dfs = pd.read_html(response.text, **kwargs)

    # Expect a singleton list
    assert len(dfs) == 1

    return dfs[0]


def history_dates(mkt_id):
    url = iem.LEGACY_URL + 'pricehistory/pricehistory_selectcontract.cfm'
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

if __name__ == '__main__':
    mkt_id = iem.Market.RCONV16.value
    # year = 2016
    # month = 6
    # px_hist_df = price_history_frame(mkt_id, year, month)
    px_hist_dfs = full_price_history_frame(mkt_id)


