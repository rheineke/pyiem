import pandas as pd

import iem
from iem import pricehistory as px_hist


def open_store(mode=None):
    kwargs = dict(path='data/iem.hdf', mode=None)
    return pd.HDFStore(**kwargs)

if __name__ == '__main__':
    mkt_name = 'FedPolicyB'
    print(mkt_name)
    mkt = iem.Market(mkt_name)
    mkt_id = mkt.value
    px_hist_dfs = px_hist._full_price_history_frames(mkt_id)

    # with open_store() as hdf_store:
    #     hdf_store[mkt_name] = px_hist_df
