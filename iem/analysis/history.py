"""Information that can be retrieved from daily historical data"""

import iem
from iem import config, pricehistory as px_hist, recorder


def contract_dates_frame(daily_price_history_df):
    """
    Returns a dataframe that calculates the open and liquidation date of each
    contract based on the start and end of daily historical data

    :param daily_price_history_df:
    :return:
    """
    df = daily_price_history_df.reset_index()
    gb = df.groupby(iem.CONTRACT)
    agg_args = {
        config.OPEN_DATE: min,
        config.LIQUIDATION_DATE: max,
    }
    dt_df = gb[iem.DATE].aggregate(agg_args)
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
