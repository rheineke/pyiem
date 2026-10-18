"""Information that can be retrieved from daily historical data"""

import pyiem
from pyiem import pricehistory as px_hist
from pyiem import config, recorder


def contract_dates_frame(daily_price_history_df):
    """
    Returns a dataframe that calculates the open and liquidation date of each
    contract based on the start and end of daily historical data

    :param daily_price_history_df:
    :return:
    """
    df = daily_price_history_df.reset_index()
    gb = df.groupby(pyiem.CONTRACT)
    dt_df = gb[pyiem.DATE].agg(
        **{config.OPEN_DATE: 'min', config.LIQUIDATION_DATE: 'max'}
    )
    return dt_df.sort_values(by=config.LIQUIDATION_DATE)


def _table_names(store):
    names = []
    for k in store.keys():
        if px_hist.NAME not in k:
            continue
        names.append(k[1:])
    return names


if __name__ == '__main__':
    mkt_date_dict = {}
    with recorder.open_store('data/hist_iem.hdf') as hdf_store:
        table_names = _table_names(hdf_store)
        for name in table_names:
            df = hdf_store[name]
            mkt = name.split('_')[0]
            mkt_date_dict[mkt] = contract_dates_frame(df)
