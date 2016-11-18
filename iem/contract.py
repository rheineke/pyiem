from iem import config


class Market:
    def __init__(self, market_name, market_fp=None):
        self.name = market_name
        self.id = config.read_markets(market_fp)[market_name]['id']