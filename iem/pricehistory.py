import pandas as pd
import requests

import iem


def price_history_frame(mkt_id, year, month):
    """Returns price history as a DataFrame"""
    url = iem.LEGACY_URL + '/pricehistory/PriceHistory_GetData.cfm'
    data = dict(Market_ID=mkt_id, Month='{:02d}'.format(month), Year=year)
    response = requests.post(url=url, data=data)
    index_cols = [iem.DATE, iem.CONTRACT]
    kwargs = dict(header=0, parse_dates=[iem.DATE], index_col=index_cols)
    dfs = pd.read_html(response.text, **kwargs)

    # Expect a singleton list
    assert len(dfs) == 1

    return dfs[0]

if __name__ == '__main__':
    mkt_id = iem.Market.RCONV16.value
    year = 2016
    month = 6
    px_hist_df = price_history_frame(mkt_id, year, month)

