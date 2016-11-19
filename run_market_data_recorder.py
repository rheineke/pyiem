from iem import config
from iem.contract import Market
from iem.session import Session
from iem.analysis.hdf_store import retrieve_and_store_public_data

if __name__ == '__main__':
    # Publicly available daily data
    retrieve_and_store_public_data()

    # Configuration
    login_kwargs = config.read_login()
    mkt_conf = config.read_markets()
    mkts = [Market(nm) for nm in mkt_conf.keys()]

    # Initiate session
    sess = Session(**login_kwargs)
    login_response = sess.authenticate()
    # Request each market orderbook dataframe
    for mkt in mkts:
        ob_df = sess.market_orderbook(mkt)
        # Timestamp either from request object or created here
        # Request own outstanding orders from each market
        for asset in mkt_conf[mkt.name]['assets']:
            oo_df = sess.asset_outstanding_orders()
    # Request own trades from each market (or is it one list for all markets?)
    # Request position from each market

    # Record orderbooks after all session I/O to minimize time difference
    # between market snapshotes

