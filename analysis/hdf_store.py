import pandas as pd

import iem
from iem import pricehistory as px_hist


def open_store(mode=None):
    kwargs = dict(path='data/iem.hdf', mode=None)
    return pd.HDFStore(**kwargs)

if __name__ == '__main__':
    mkt_name = 'FedPolicyB'
    # print(mkt_name)
    # mkt = iem.Market(mkt_name)
    # mkt_id = mkt.value
    # px_hist_dfs = px_hist._full_price_history_frames(mkt_id)

    # FedPolicyB data cleaning
    # 2001/10 data has a warning about the contract type
    # df = px_hist_dfs[9]
    # tail_df = df.iloc[1:]
    # dt_idx = pd.to_datetime(tail_df.index.get_level_values(level=iem.DATE))
    # contract_idx = tail_df.index.get_level_values(level=iem.CONTRACT)
    # levels = [dt_idx, contract_idx]
    # multi_idx = pd.MultiIndex(levels=levels, labels=tail_df.index.labels)
    # clean_df = tail_df.set_index(multi_idx)
    # px_hist_dfs[9] = clean_df
    # px_hist_df = pd.concat(px_hist_dfs)

    with open_store(mode='r') as hdf_store:
        px_hist_df = hdf_store[mkt_name]
