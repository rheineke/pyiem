import iem
from iem.config import read_login
from iem.contract import Contract, Market
from iem.session import Session

if __name__ == '__main__':
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
    oo_df = sess.outstanding_orders(asset, iem.BID)

    # Get trade messages
    msg_df = sess.messages(mkt)

    # Send order
    # contract = 3037  # RCONV16.TRUMP_NOM
    # price_time_limit = PriceTimeLimit(.25, '20161102')
    # o = Single(contract, Side.BUY, 1, price_time_limit)
    # latest_ob_df = sess.place_order(o)

    logout_response = sess.logout()
