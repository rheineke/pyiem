import json
from pprint import pprint

from iem.session import Session
from iem.order import Bundle, PriceTimeLimit, Single, Counterparty
from iem import Side


def arbitrage_orders(direction, quantity=1):
    # TODO: Most efficient action is to determine if single buy is lower price
    # than bundle + 2 sales
    expiration = '2016/06/30 11:59 PM'
    dir_pt_lmt = PriceTimeLimit(.20, expiration)
    direction_contract = 291  # TODO: Lookup
    contract_bundle = 704
    other_contracts = [290, 292]
    other_pt_lmt = PriceTimeLimit(0.90, expiration)
    return [
        # Buy direction asset
        Single(direction_contract, Side.BUY, quantity, dir_pt_lmt),
        # Buy bundle asset
        Bundle(contract_bundle, Side.BUY, quantity, Counterparty.Exchange),
    ] + [  # Sell other two assets
        Single(c, Side.SELL, quantity, other_pt_lmt) for c in other_contracts
    ]


if __name__ == '__main__':
    with open('conf/login.json') as fp:
        login_kwargs = json.load(fp)

    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    os = arbitrage_orders('same', quantity=1)
    pprint(os)
    responses = []
    for o in os:
        responses.append(sess.place_order(o))
    sess.logout()
