import pandas as pd

import iem
from iem import pricehistory as px_hist


def open_store(mode=None):
    kwargs = dict(path='data/iem.hdf', mode=None)
    return pd.HDFStore(**kwargs)


def retrieve_and_store():
    mkt_dict = iem.read_markets_json()
    for mkt_name, _ in mkt_dict.items():
        print(mkt_name)
        mkt = iem.Market(mkt_name)
        mkt_id = mkt.value
        if mkt_name == 'FedPolicyB':
            px_hist_dfs = px_hist._full_price_history_frames(mkt_id)
            # FedPolicyB data cleaning
            # 2001/10 data has a warning about the contract type
            df = px_hist_dfs[9]
            tail_df = df.iloc[1:]
            dt_lvl = tail_df.index.get_level_values(level=iem.DATE)
            dt_idx = pd.to_datetime(dt_lvl)
            contract_idx = tail_df.index.get_level_values(level=iem.CONTRACT)
            levels = [dt_idx, contract_idx]
            labels = tail_df.index.labels
            multi_idx = pd.MultiIndex(levels=levels, labels=labels)
            clean_df = tail_df.set_index(multi_idx)
            px_hist_dfs[9] = clean_df
            px_hist_df = pd.concat(px_hist_dfs)
        else:
            px_hist_df = px_hist.full_price_history_frame(mkt_id)
        with open_store() as hdf_store:
            hdf_store[mkt_name] = px_hist_df

if __name__ == '__main__':
    pass
    # retrieve_and_store()
