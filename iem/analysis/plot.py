import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import iem
from iem import config, pricehistory as px_hist, recorder
from iem import contract

EXPIRY = 'expiry'
DAYS_TO_EXPIRY_DATE = 'days_to_expiry_date'


def get_new_fignum():
    fignums = plt.get_fignums()
    if fignums:
        return max(fignums) + 1
    else:
        return 1


def expiry(contract_name):
    return contract_name[-4:]


def expiry_date_series(expiry_str, *, expiry_date_json):
    bundle = expiry_date_json.get(expiry_str, {})
    return bundle.get(config.EXPIRY_DATE, pd.NaT)


def cumulative_units_frame(bundle_history_df):
    return cumsum_frame(bundle_history_df[iem.UNITS])


def cumsum_frame(bundle_history_srs):
    return bundle_history_srs.unstack().cumsum()


def bundle_slice(json_obj, market_name, expiry_date_str):
    bundle_dict = config.find_bundle(json_obj, market_name, expiry_date_str)
    bundle_assets = list(bundle_dict[config.ASSETS].keys())
    return pd.IndexSlice[:, bundle_assets]


def plot_cumsum(bundle_history_srs):
    cumsum_df = cumsum_frame(bundle_history_srs)
    # First trade index
    fst_trade_idx = (cumsum_df.sum(axis=1) > 0).idxmax()
    nonzero_cum_units_df = cumsum_df.loc[fst_trade_idx:]
    plt.figure(get_new_fignum())
    plt.plot(nonzero_cum_units_df)
    plt.show()

if __name__ == '__main__':
    mkt_name = 'FedPolicyB'
    mkt = contract.Market(mkt_name)
    with recorder.open_store(mode='r') as hdf_store:
        px_hist_df = hdf_store[recorder.history_key(market=mkt)]

    mkts_json = config.read_markets()
    mkt_conf = mkts_json[mkt_name]

    # Clean dataframe
    df = px_hist_df.copy().reset_index()
    # Expiry
    df[EXPIRY] = df[iem.CONTRACT].apply(expiry)
    # Expiry date
    expiry_date_json = mkt_conf[config.BUNDLE]
    kwargs = {'expiry_date_json': expiry_date_json}
    df[config.EXPIRY_DATE] = df[EXPIRY].apply(expiry_date_series, **kwargs)
    # Days to expiration
    df[DAYS_TO_EXPIRY_DATE] = df[config.EXPIRY_DATE] - df[iem.DATE]

    # Bundle frame
    bundle = '1116'
    bundle_assets = list(mkt_conf[config.BUNDLE][bundle][config.ASSETS].keys())
    bundle_lbl = df[iem.CONTRACT].str.contains(bundle)
    bundle_df = df.loc[bundle_lbl]

    bundle_df = px_hist_df.loc[bundle_slice(mkts_json, mkt_name, bundle), :]
    # plot_cumsum(bundle_df[iem.UNITS])
    plot_cumsum(bundle_df[iem.DOLLAR_VOLUME])

    # plot_cumsum(px_hist_df[iem.UNITS])
    plot_cumsum(px_hist_df[iem.DOLLAR_VOLUME])

    # gb = df.groupby([EXPIRY, iem.DATE])
    # agg_dict = {
    #     iem.UNITS: np.sum,
    #     iem.DVOL: np.sum,
    #     iem.LOW_PX: np.sum,
    #     iem.HIGH_PX: np.sum,
    #     iem.AVG_PX: np.sum,
    #     iem.LST_PX: np.sum,
    #     config.EXPIRY_DATE: 'first',
    #     DAYS_TO_EXPIRY_DATE: 'first',
    # }
    # agg_df = gb.agg(agg_dict)
    # # Clean aggregate
    # agg_df[config.EXPIRY_DATE] = pd.to_datetime(agg_df[config.EXPIRY_DATE])
    # agg_df[DAYS_TO_EXPIRY_DATE] = pd.to_timedelta(agg_df[DAYS_TO_EXPIRY_DATE])
    # bundle_df = agg_df.loc[bundle]
    # plt.figure(get_new_fignum())
    # TODO: Match price history graphs on website
    # TODO: Construct days to expiration. Useful feature?
    # TODO: Arbitrage analysis
    # cols = [iem.LOW_PX, iem.HIGH_PX, iem.AVG_PX, iem.LST_PX]
    # kwargs = dict(c='blue', marker='o', label='Training data')
    # plt.plot(sept16_df[cols], **kwargs)
