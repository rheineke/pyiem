import pandas as pd

import iem
from iem import config, contract, pricehistory as px_hist


def open_store(mode=None):
    # TODO(rheineke): If data folder doesn't exist, create
    kwargs = dict(path='data/iem.hdf', mode=mode)
    return pd.HDFStore(**kwargs)


def retrieve_and_store_daily_data():
    mkt_conf = config.read_markets()
    for mkt_name in mkt_conf.keys():
        print(mkt_name)
        mkt = contract.Market(mkt_name)
        mkt_id = mkt.id
        if mkt_name == 'FedPolicyB':
            px_hist_dfs = px_hist.full_price_history_frames(mkt_id)
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
            hdf_store[mkt_name + '_' + px_hist.NAME] = px_hist_df


def retrieve_and_store_quote_data(snapshot_date):
    mkt_conf = config.read_markets()
    active_mkt_conf = config.active_markets(mkt_conf, snapshot_date)
    for mkt_name in active_mkt_conf.keys():
        print(mkt_name)
        mkt = contract.Market(mkt_name)
        quotes_df = px_hist.read_quote_frame(mkt.id)
        # TODO(rheineke): Append only if it's a new timestamp
        with open_store() as hdf_store:
            key = mkt_name + '_' + 'quotes'
            hdf_store.put(key=key, value=quotes_df, format='t', append=True)
