import asyncio

import pandas as pd

from iem import recorder


def read_and_write_quotes(now, loop):
    recorder.read_and_write_quotes(now)
    delay = 15 * 60  # HTML is updated once every 15 minutes
    loop.call_later(delay, read_and_write_quotes, pd.Timestamp.now(), loop)

if __name__ == '__main__':
    # Publicly available data
    # Daily summary data
    # hdf_store.retrieve_and_store_daily_data()

    # Quotes data
    loop = asyncio.get_event_loop()

    # Schedule a call to retrieve quotes and store them
    loop.call_soon(read_and_write_quotes, pd.Timestamp.now(), loop)

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    loop.close()

    # store = recorder.open_store(mode='r')
    # quotes_hist_df = store['FedPolicyB_quotes']

    # Configuration
    # login_kwargs = config.read_login()
    # mkt_conf = config.read_markets()
    # mkts = [Market(nm) for nm in mkt_conf.keys()]
    #
    # # Initiate session
    # sess = Session(**login_kwargs)
    # login_response = sess.authenticate()
    # # Request each market orderbook dataframe
    # for mkt in mkts:
    #     ob_df = sess.market_orderbook(mkt)
    #     # Timestamp either from request object or created here
    #     # Request own outstanding orders from each market
    #     for asset in mkt_conf[mkt.name]['assets']:
    #         oo_df = sess.asset_outstanding_orders()
    # Request own trades from each market (or is it one list for all markets?)
    # Request position from each market

    # Record orderbooks after all session I/O to minimize time difference
    # between market snapshotes

