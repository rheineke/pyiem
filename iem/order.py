from builtins import super

from enum import Enum, unique

import numpy as np
import pandas as pd


def _is_ioc(price, expiration):
    if np.isnan(price) and pd.isnull(expiration):
        return True
    elif not np.isnan(price):
        return False
    else:
        fmt = 'Price {} and expiration {} are not valid combination'
        raise ValueError(fmt.format(price, expiration))


def to_string(expiration):
    if pd.isnull(expiration):
        return 'No expiration'
    return '{:%Y-%m-%d %I:%M %p}'.format(expiration)


class PriceTimeLimit:
    def __init__(self, price=np.nan, expiration=pd.NaT):
        self.price = price
        self.expiration = expiration
        self.ioc = _is_ioc(price, expiration)

    def __repr__(self):
        fmt = '{price:.3f} {expiry}'
        return fmt.format(price=self.price, expiry=to_string(self.expiration))


@unique
class Counterparty(Enum):
    Exchange = 0
    Participant = 1


class Order:
    def __init__(self, side, quantity, price_time_limit, counterparty):
        self.side = side
        self.quantity = quantity
        self.price_time_limit = price_time_limit
        self.counterparty = counterparty


class Single(Order):
    def __init__(self, contract, side, quantity, price_time_limit):
        super().__init__(side, quantity, price_time_limit,
                         Counterparty.Participant)
        self.contract = contract
        self.id = None

    def __repr__(self):
        fmt = 'Single {contract}: {side} {qty}@{pricetimelimit} ({cp})'
        kwargs = dict(contract=self.contract,
                      side=self.side,
                      qty=self.quantity,
                      pricetimelimit=self.price_time_limit,
                      cp=self.counterparty)
        return fmt.format(**kwargs)


# TODO: Can combine if contract can hold same info as contract_bundle
class Bundle(Order):
    def __init__(self, contract_bundle, side, quantity, counterparty):
        super().__init__(side, quantity, None, counterparty)
        self.contract_bundle = contract_bundle

    def __repr__(self):
        fmt = 'Bundle {contract}: {side} {qty} ({cp})'
        kwargs = dict(contract=self.contract_bundle, side=self.side,
                      qty=self.quantity, cp=self.counterparty)
        return fmt.format(**kwargs)
