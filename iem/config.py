"""Convenience functions that perform I/O to read local configuration files"""
import json

import pandas as pd

_LIQUIDATION_DATE = 'liquidation_date'


def read_markets(market_fp=None):
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        mkts = json.load(fp)
    return mkts


def active_markets(market_dict, active_date):
    # TODO(rheineke): Create bundle iterator?
    active_market_dict = {}
    for mkt_nm, mkt_dict in market_dict.items():
        bundles_dict = mkt_dict['bundle']
        if _LIQUIDATION_DATE in bundles_dict:
            if _active_bundle(bundles_dict, active_date):
                active_market_dict[mkt_nm] = mkt_dict
        else:  # Market contains multiple bundles
            active_bundles_dict = {}
            for bundle_nm, bundle_dict in bundles_dict.items():
                if _active_bundle(bundle_dict, active_date):
                    active_bundles_dict[bundle_nm] = bundle_dict
            if len(active_bundles_dict):
                active_market_dict[mkt_nm] = active_bundles_dict
    return active_market_dict


def _active_bundle(bundle_dict, date):
    liq_dt = pd.to_datetime(bundle_dict[_LIQUIDATION_DATE])
    return pd.isnull(liq_dt) or liq_dt >= date


def read_login():
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)
    return login_kwargs
