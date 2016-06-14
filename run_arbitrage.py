import json
from pprint import pprint

from iem.contract import Contract, ContractBundle
from iem.session import Session
from iem.order import Bundle, PriceTimeLimit, Single, Counterparty
from iem import Side


def arbitrage_orders(direction, quantity=1):
    # TODO: Most efficient action is to determine if single buy is lower price
    # than bundle + 2 sales
    expiration = '2016/06/30 11:59 PM'
    dir_pt_lmt = PriceTimeLimit(.20, expiration)
    dir_contract = Contract('FRsame0616')
    contract_bundle = ContractBundle('FedPolicyB', '0616')
    other_contracts = [Contract('FRup0616'), Contract('FRdown0616')]
    other_pt_lmt = PriceTimeLimit(0.90, expiration)
    return [
        # Buy direction asset
        Single(dir_contract, Side.BUY, quantity, dir_pt_lmt),
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
    # for o in os:
    #     responses.append(sess.place_order(o))
    sess.logout()
