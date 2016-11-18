"""Convenience functions that perform I/O to read local configuration files"""

import json


def read_markets(market_fp=None):
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        mkts = json.load(fp)
    return mkts


def read_login():
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)
    return login_kwargs
