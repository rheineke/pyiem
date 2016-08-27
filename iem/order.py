import datetime as dt
from enum import Enum, unique
from functools import wraps

import numpy as np


def _is_ioc(price, expiration):
    if np.isnan(price) and expiration is None:
        return True
    elif not np.isnan(price) and expiration is not None:
        return False
    else:
        fmt = 'Price {} and expiration {} are not valid combination'
        raise ValueError(fmt.format(price, expiration))


def strftime_expiration(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        # Find expiration argument
        if len(args) == 2:
            expiry_obj = args[1]
        else:
            expiry_obj = kwds.get('expiration', None)
        if type(expiry_obj) == dt.date:
            expiration_str = expiry_obj.strftime('%Y/%m/%d 23:59PM')
        elif type(expiry_obj) == dt.datetime:
            expiration_str = expiry_obj.strftime('%Y/%m/%d %H:%M%p')
        elif type(expiry_obj) == str:
            expiration_str = expiry_obj
        return func(*args[:-1], expiration=expiration_str)
    return wrapper


# @strftime_expiration
class PriceTimeLimit:
    def __init__(self, price=np.nan, expiration=None):
        self.price = price
        self.expiration = expiration
        self.ioc = _is_ioc(price, expiration)


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

    def __repr__(self):
        fmt = 'Single {contract}: {side} {qty}@{price} {expiry} ({cp})'
        kwargs = dict(contract=self.contract,
                      side=self.side,
                      qty=self.quantity,
                      price=self.price_time_limit.price,
                      expiry=self.price_time_limit.expiration,
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
