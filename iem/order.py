from enum import Enum, unique

import numpy as np


@unique
class Side(Enum):
    BUY = 0
    SELL = 1


def _is_ioc(price, expiration):
    if np.isnan(price) and expiration is None:
        return True
    elif not np.isnan(price) and expiration is not None:
        return False
    else:
        fmt = 'Price {} and expiration {} are not valid combination'
        raise ValueError(fmt.format(price, expiration))


class PriceTimeLimit:
    def __init__(self, price=np.nan, expiration=None):
        self.price = price
        self.expiration = expiration
        self.ioc = _is_ioc(price, expiration)


@unique
class CounterParty(Enum):
    Exchange = 0
    Participant = 1


class Order:
    def __init__(self, side, quantity, price_time_limit, counterparty,
                 request_code):
        self.side = side
        self.quantity = quantity
        self.price_time_limit = price_time_limit
        self.counterparty = counterparty
        self.request_code = request_code

    def calc_request_code(self, side, price_time_limit):
        if type(self) == Single:
            if side == Side.SELL:
                return 'S' if price_time_limit.ioc else 'A'
            else:
                return 'P' if price_time_limit.ioc else 'B'
        else:
            raise NotImplementedError('Bundle order not implemented yet')


class Single(Order):
    def __init__(self, contract, side, quantity, price_time_limit):
        super().__init__(side, quantity, price_time_limit,
                         CounterParty.Participant,
                         single_request_code(side, price_time_limit))
        self.contract = contract

