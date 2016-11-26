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


def history_key(market):
    return market.name + '_' + px_hist.NAME


def quote_key(market):
    return market.name + '_quotes'


def retrieve_and_store_daily_data():
    for mkt_name in config.read_markets().keys():
        print(mkt_name)
        mkt = contract.Market(mkt_name)
        mkt_id = mkt.id
        if mkt_name == 'FedPolicyB':
            px_hist_dfs = px_hist.full_price_history_frames(mkt_id)

            # FedPolicyB data cleaning
            # 2001/10 data has a warning about the contract type
            oct_2001_idx = 9
            df = px_hist_dfs[oct_2001_idx]
            tail_df = df.iloc[1:].reset_index()
            tail_df[iem.DATE] = pd.to_datetime(tail_df[iem.DATE])
            clean_df = tail_df.set_index([iem.DATE, iem.CONTRACT])
            px_hist_dfs[oct_2001_idx] = clean_df

            px_hist_df = pd.concat(px_hist_dfs)
        else:
            px_hist_df = px_hist.full_price_history_frame(mkt_id)
        # Fully lexsort dataframe for easier manipulation later
        px_hist_df = px_hist_df.sort_index()
        with open_store() as hdf_store:
            hdf_store[history_key(market=mkt)] = px_hist_df


def read_and_write_quotes(snapshot_date):
    mkt_conf = config.read_markets()
    active_mkt_conf = config.active_markets(mkt_conf, snapshot_date)
    for mkt_name in active_mkt_conf.keys():
        print('{}: retrieving {}. . . '.format(snapshot_date, mkt_name), end='')
        mkt = contract.Market(mkt_name)
        quotes_df = px_hist.read_quote_frame(mkt.id)
        with open_store() as hdf_store:
            key = quote_key(market=mkt)
            # TODO(rheineke): Do not assume table exists
            if key in hdf_store:
                prev_df = hdf_store[key]
                dedupe_idx = quotes_df.index.difference(prev_df.index)
                iter_df = quotes_df.reindex(dedupe_idx)
            else:
                iter_df = quotes_df
            hdf_store.put(key=key, value=iter_df, format='t', append=True)
        print('{}: completed {}'.format(pd.Timestamp.now(), mkt_name))
