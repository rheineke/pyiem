import pyiem
from pyiem.config import read_login
from pyiem.contract import Contract, Market
from pyiem.session import Session

def main():
    login_kwargs = read_login()
    sess = Session(**login_kwargs)
    login_response = sess.authenticate()

    # Get Orderbook dataframe
    mkt = Market('FedPolicyB')
    ob_df = sess.orderbook(mkt)

    # Get order activity
    asset = Contract(mkt.name, 'FRup1216')
    print(asset)
    oa_df = sess.holdings(asset)

    # Get outstanding orders
    oo_df = sess.outstanding_orders(asset, pyiem.BID)

    # Get trade messages
    msg_df = sess.messages(mkt)

    # Send order
    # contract = 3037  # RCONV16.TRUMP_NOM
    # price_time_limit = PriceTimeLimit(.25, '20161102')
    # o = Single(contract, Side.BUY, 1, price_time_limit)
    # latest_ob_df = sess.place_order(o)

    logout_response = sess.logout()

if __name__ == '__main__':
    main()
