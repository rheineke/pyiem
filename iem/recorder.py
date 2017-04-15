"""
Record daily historical data and 15 minute market snapshots in an HDF store
"""
# Python 2 and 3:
from __future__ import print_function

import os
from pathlib import Path

import pandas as pd
import sqlalchemy as sa

import iem
from iem import config, contract, pricehistory as px_hist


def daily_market_table(metadata):
    # Index columns
    date_col = sa.Column('Date', sa.DATETIME, nullable=False)
    asset_col = sa.Column(
        config.ASSET_ID,
        sa.INTEGER,
        sa.ForeignKey('assets.id'),
        nullable=False
    )

    return sa.Table(
        'daily_market',
        metadata,
        date_col,
        asset_col,
        sa.Column('Units', sa.INTEGER, nullable=False),
        sa.Column('$Volume', sa.INTEGER, nullable=False),
        sa.Column('LowPrice', sa.INTEGER, nullable=False),
        sa.Column('HighPrice', sa.INTEGER, nullable=False),
        sa.Column('AvgPrice', sa.DECIMAL, nullable=False),
        sa.Column('LastPrice', sa.INTEGER, nullable=True),  # Null == NaN?
        sa.Index('idx', (date_col, asset_col), unique=True),
    )


def quotes_table(metadata):
    # Index columns
    ts_col = sa.Column('Timestamp', sa.TIMESTAMP, nullable=False)
    asset_col = sa.Column(
        config.ASSET_ID,
        sa.INTEGER,
        sa.ForeignKey('assets.id'),
        nullable=False
    )

    return sa.Table(
        'quotes',
        metadata,
        ts_col,
        asset_col,
        sa.Column('Bid', sa.INTEGER, nullable=False),  # No example of nullable
        sa.Column('Ask', sa.INTEGER, nullable=False),
        sa.Column('Last', sa.INTEGER, nullable=False),
        sa.Column('Low', sa.INTEGER, nullable=True),
        sa.Column('High', sa.INTEGER, nullable=True),
        sa.Column('Average', sa.DECIMAL, nullable=True),
        sa.Index('idx', (ts_col, asset_col), unique=True),
    )


def store_path(path=None):
    if path is None:
        path = 'data/iem.hdf'
    return Path(path)


def open_store(path=None, mode=None):
    store_p = store_path(path)
    parent_path = store_p.parent
    # Since Python 3.5, we can request nested existing directories directly from
    # path-like object without exception
    # parent_path.mkdir(parents=False, exist_ok=True)
    try:
        os.makedirs(parent_path.as_posix())
    except OSError:
        pass
    # Add to HDFStore arguments if size becomes an issue
    # , complevel=9, complib='zlib'
    return pd.HDFStore(path=store_p.as_posix(), mode=mode)


def history_key(market):
    return market.name + '_' + px_hist.NAME


def quote_key(market):
    return market.name + '_quotes'


def retrieve_and_store_daily_data():
    """
    For each market in the markets config file, retrieve the daily snapshots
    from the IEM site. Previous daily snapshot data for that market is
    overwritten in the process

    :return: None
    """
    for mkt_name in config.read_markets().keys():
        mkt = contract.Market(mkt_name)
        px_hist_df = read_daily_market_data(mkt_name)

        with open_store(mode='a') as hdf_store:
            key = history_key(market=mkt)
            hdf_store.put(key=key, value=px_hist_df, format='t')


def read_daily_market_data(market):
    """
    Read the daily snapshots from the IEM website.

    :param market: 
    :return: 
    """
    print(market.name)
    if market.name == 'FedPolicyB':
        px_hist_dfs = px_hist.full_price_history_frames(market.id)

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
        px_hist_df = px_hist.full_price_history_frame(market.id)

    # Fully lexsort dataframe for easier manipulation later
    px_hist_df = px_hist_df.sort_index()

    return px_hist_df


def read_and_write_quotes(snapshot_date):
    mkt_conf = config.read_markets()
    active_mkt_conf = config.active_markets(mkt_conf, snapshot_date)
    retrieved_markets = {}
    for mkt_name, mkt_conf in active_mkt_conf.items():
        print('{}: retrieving {}. . . '.format(snapshot_date, mkt_name), end='')
        mkt = contract.Market(mkt_name)

        # Market snapshot may have been retrieved already
        if mkt_name not in retrieved_markets:
            quotes_dfs = px_hist.read_quote_frames(mkt_conf)
            retrieved_markets.update(quotes_dfs)

        quotes_df = retrieved_markets[mkt_name]

        with open_store(mode='a') as hdf_store:
            key = quote_key(market=mkt)
            if key in hdf_store:
                prev_df = hdf_store[key]
                dedupe_idx = quotes_df.index.difference(prev_df.index)
                iter_df = quotes_df.reindex(dedupe_idx)
            else:
                iter_df = quotes_df
            hdf_store.put(key=key, value=iter_df, format='t', append=True)
        print('{}: completed {}'.format(pd.Timestamp.now(), mkt_name))
