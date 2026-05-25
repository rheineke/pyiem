"""Convenience functions that perform I/O to read local configuration files"""
import json

import collections
import pandas as pd
import sqlalchemy as sa

# Variables defined in configuration file but not explicitly on website
ID = 'id'
ASSET_ID = 'asset_id'
ASSETS = 'assets'
BUNDLE = 'bundle'
BUNDLE_ID = 'bundle_id'
BUNDLES = 'bundles'
EXPIRY_DATE = 'expiry_date'
MARKET_ID = 'market_id'
MARKETS = 'markets'
NAME = 'name'
OPEN_DATE = 'open_date'
ORDER_ID = 'order_id'
LIQUIDATION_DATE = 'liquidation_date'
QUOTES_URL = 'quotes_url'


def read_markets(market_fp=None):
    if market_fp is None:
        market_fp = 'conf/markets.json'

    with open(market_fp) as fp:
        mkts = json.load(fp, object_hook=collections.OrderedDict)

    return mkts


def find_bundle(json_obj, market_name, expiry_date_str):
    bundle_value = json_obj[market_name][BUNDLE]

    if BUNDLE_ID in bundle_value:
        return bundle_value

    return bundle_value[expiry_date_str]


def find_asset(json_obj, market_name, asset_name):
    expiry_str = asset_name[-4:]
    bundle_value = find_bundle(json_obj, market_name, expiry_str)
    return bundle_value[ASSETS][asset_name]


def active_markets(market_dict, active_date):
    # TODO(rheineke): Create bundle iterator?
    active_market_dict = {}
    for mkt_nm, mkt_dict in market_dict.items():
        bundles_dict = mkt_dict[BUNDLE]
        if LIQUIDATION_DATE in bundles_dict:
            if _active_bundle(bundles_dict, active_date):
                active_market_dict[mkt_nm] = mkt_dict
        else:  # Market contains multiple bundles
            active_bundles_dict = {}
            for bundle_nm, bundle_dict in bundles_dict.items():
                if _active_bundle(bundle_dict, active_date):
                    active_bundles_dict[bundle_nm] = bundle_dict
            if len(active_bundles_dict):
                active_market_dict[mkt_nm] = {
                    ID: mkt_dict[ID],
                    BUNDLE: active_bundles_dict
                }
    return active_market_dict


def _active_bundle(bundle_dict, date):
    # Date is after open date
    if OPEN_DATE in bundle_dict:
        open_dt = pd.to_datetime(bundle_dict[OPEN_DATE])
    else:
        open_dt = pd.NaT
    opened_after = pd.isnull(open_dt) or open_dt <= date

    # Date is before liquidation date
    liq_dt = pd.to_datetime(bundle_dict[LIQUIDATION_DATE])
    liquidated_after = pd.isnull(liq_dt) or liq_dt >= date
    return opened_after and liquidated_after


def read_login():
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)
    return login_kwargs


def markets_table(metadata):
    return sa.Table(
        MARKETS,
        metadata,
        sa.Column(ID, sa.INTEGER, primary_key=True, nullable=False),
        sa.Column(NAME, sa.NCHAR(10), nullable=False),
    )


def bundles_table(metadata):
    mkt_id_fk = sa.ForeignKey(MARKETS + '.' + ID)
    return sa.Table(
        BUNDLES,
        metadata,
        sa.Column(ID, sa.INTEGER, primary_key=True, nullable=False),
        sa.Column(MARKET_ID, sa.INTEGER, mkt_id_fk, nullable=False),
        sa.Column(OPEN_DATE, sa.DATE, nullable=False),
        sa.Column(EXPIRY_DATE, sa.DATE, nullable=False),
        sa.Column(LIQUIDATION_DATE, sa.DATE, nullable=True),
    )


def assets_table(metadata):
    bundle_id_fk = sa.ForeignKey(BUNDLES + '.' + ID)
    return sa.Table(
        ASSETS,
        metadata,
        sa.Column(ID, sa.INTEGER, primary_key=True, nullable=False),
        sa.Column(BUNDLE_ID, sa.INTEGER, bundle_id_fk, nullable=False),
        sa.Column(NAME, sa.NCHAR(10), nullable=False),
        sa.Column(ORDER_ID, sa.INTEGER, nullable=False),
    )
