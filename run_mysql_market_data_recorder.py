import json

import pandas as pd
import sqlalchemy as sa

from iem import config, contract, recorder


def create_all(metadata, mkt_conf):
    config.markets_table(metadata)
    config.bundles_table(metadata)
    config.assets_table(metadata)

    # Daily market quotes
    mkts = [contract.Market(mkt_nm) for mkt_nm in mkt_conf.keys()]
    for mkt in mkts:
        recorder.daily_market_table(metadata, mkt)
        recorder.quotes_table(metadata, mkt)


def insert_config_data(engine):
    # Market table data
    mkt_names = list(mkt_conf.keys())
    idx_data = [mkt_conf[nm][config.ID] for nm in mkt_names]
    mkt_idx = pd.Index(data=idx_data, name=config.ID)
    mkt_df = pd.DataFrame(data=mkt_names, columns=[config.NAME], index=mkt_idx)
    mkt_df = mkt_df.sort_index()
    sql_kwargs = dict(con=engine, if_exists='append')
    # mkt_df.to_sql(config.MARKETS, **sql_kwargs)

    # Bundles and assets table data
    bundle_data = pd.compat.OrderedDefaultdict(list)
    asset_data = pd.compat.OrderedDefaultdict(list)

    for mkt_name, mkt_dict in mkt_conf.items():
        mkt_id = mkt_dict[config.ID]

        if config.BUNDLE_ID in mkt_dict[config.BUNDLE]:
            bundle_dict = mkt_dict[config.BUNDLE]
            append_bundle(bundle_data, mkt_id, bundle_dict)

            bundle_id = bundle_dict[config.BUNDLE_ID]
            append_assets(asset_data, bundle_id, bundle_dict[config.ASSETS])
        else:
            for bundle_name, bundle_dict in mkt_dict[config.BUNDLE].items():
                append_bundle(bundle_data, mkt_id, bundle_dict)

                bundle_id = bundle_dict[config.BUNDLE_ID]
                append_assets(asset_data, bundle_id, bundle_dict[config.ASSETS])

    bundle_df = pd.DataFrame(data=bundle_data).set_index(config.ID)
    bundle_df = bundle_df.sort_index()
    # bundle_df.to_sql(config.BUNDLES, **sql_kwargs)

    asset_df = pd.DataFrame(data=asset_data).set_index(config.ID)
    asset_df = asset_df.sort_index()
    # asset_df.to_sql(config.ASSETS, **sql_kwargs)


def append_bundle(bundle_data, mkt_id, bundle_dict):
    bundle_data[config.ID].append(bundle_dict[config.BUNDLE_ID])

    bundle_data[config.MARKET_ID].append(mkt_id)

    for c in [config.OPEN_DATE, config.EXPIRY_DATE, config.LIQUIDATION_DATE]:
        val_str = bundle_dict[c]
        bundle_data[c].append(val_str if len(val_str) else None)


def append_assets(asset_data, bundle_id, asset_dict):
    for asset_name, asset_id_dict in asset_dict.items():
        asset_data[config.ID].append(asset_id_dict[config.ID])
        asset_data[config.BUNDLE_ID].append(bundle_id)
        asset_data[config.NAME].append(asset_name)
        asset_data[config.ORDER_ID].append(asset_id_dict['order'])

if __name__ == '__main__':
    with open('conf/db.json', 'r') as fp:
        db_conf = json.load(fp)

    # Engine connect to MySQL
    sa_url = 'sqlalchemy.url'
    mysql_url, dbname = db_conf[sa_url].rsplit(sep='/', maxsplit=1)
    mysql_engine = sa.engine_from_config({sa_url: mysql_url})

    create_fmt = 'CREATE DATABASE IF NOT EXISTS {dbname}'
    mysql_engine.execute(create_fmt.format(dbname=dbname))

    # Engine connecting to MySQL database
    engine = sa.engine_from_config(db_conf)

    metadata = sa.MetaData()
    mkt_conf = config.read_markets()
    create_all(metadata, mkt_conf)
    metadata.create_all(engine)

    insert_config_data(engine)

    # Query market table. Does metadata drop and create the table?
    db_mkt_df = pd.read_sql_table(config.MARKETS, engine, index_col=config.ID)
    db_bundle_df = pd.read_sql_table(config.BUNDLES, engine, index_col=config.ID)
    db_asset_df = pd.read_sql_table(config.ASSETS, engine, index_col=config.ID)

    # TODO: Populate data
    markets = [contract.Market(mkt_nm) for mkt_nm in mkt_conf.keys()]
    with recorder.open_store('data/hist_iem.hdf') as hdf_store:
        for market in markets:
            mkt_hist_key = recorder.history_key(market)
            mkt_hist_df = hdf_store[mkt_hist_key]
