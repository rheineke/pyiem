import json


def read_markets_json(market_fp=None):
    if market_fp is None:
        market_fp = 'conf/markets.json'
    with open(market_fp) as fp:
        mkts = json.load(fp)
    return mkts