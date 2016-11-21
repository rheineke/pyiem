from pathlib import Path

import pandas as pd

import iem
from iem import config, contract, pricehistory as px_hist


def open_store(path=None, mode=None):
    if path is None:
        path = 'data/iem.hdf'
    parent_path = Path(path).parent
    parent_path.mkdir(parents=False, exist_ok=True)
    return pd.HDFStore(path=path, mode=mode)


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


def read_and_write_quotes(snapshot_date):
    mkt_conf = config.read_markets()
    active_mkt_conf = config.active_markets(mkt_conf, snapshot_date)
    for mkt_name in active_mkt_conf.keys():
        print('{}: retrieving {}'.format(snapshot_date, mkt_name))
        mkt = contract.Market(mkt_name)
        quotes_df = px_hist.read_quote_frame(mkt.id)
        with open_store() as hdf_store:
            key = mkt_name + '_' + 'quotes'
            # TODO(rheineke): Do not assume table exists
            if key in hdf_store:
                prev_df = hdf_store[key]
                dedupe_idx = quotes_df.index.difference(prev_df.index)
                iter_df = quotes_df.reindex(dedupe_idx)
            else:
                iter_df = quotes_df
            hdf_store.put(key=key, value=iter_df, format='t', append=True)
        print('{}: completed {}'.format(pd.Timestamp.now(), mkt_name))
