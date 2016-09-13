from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from analysis import hdf_store
import iem

EXPIRY = 'expiry'
EXPIRY_DATE = 'expiry_date'
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
    return expiry_date_json.get(expiry_str, pd.NaT)


if __name__ == '__main__':
    mkt_name = 'FedPolicyB'
    with hdf_store.open_store(mode='r') as hdf_store:
        px_hist_df = hdf_store[mkt_name]

    mkts_json = iem.read_markets_json()

    # Clean dataframe
    df = px_hist_df.copy().reset_index()
    # Expiry
    df[EXPIRY] = df[iem.CONTRACT].apply(expiry)
    # Expiry date
    kwargs = {'expiry_date_json': mkts_json[mkt_name]['expiry_date']}
    expiry_dt_srs = df[EXPIRY].apply(expiry_date_series, **kwargs)
    df[EXPIRY_DATE] = expiry_dt_srs
    # Days to expiration
    df[DAYS_TO_EXPIRY_DATE] = df[EXPIRY_DATE] - df[iem.DATE]
    # sept16_lbl = df[iem.CONTRACT].str.contains('0916')
    gb = df.groupby([EXPIRY, iem.DATE])
    agg_dict = {
        iem.UNITS: np.sum,
        iem.DVOL: np.sum,
        iem.LOW_PX: np.sum,
        iem.HIGH_PX: np.sum,
        iem.AVG_PX: np.sum,
        iem.LST_PX: np.sum,
        EXPIRY_DATE: 'first',
        DAYS_TO_EXPIRY_DATE: 'first',
    }
    agg_df = gb.agg(agg_dict)
    # Clean aggregate
    agg_df[EXPIRY_DATE] = pd.to_datetime(agg_df[EXPIRY_DATE])
    agg_df[DAYS_TO_EXPIRY_DATE] = pd.to_timedelta(agg_df[DAYS_TO_EXPIRY_DATE])
    sept16_df = agg_df.loc['0916']
    # plt.figure(get_new_fignum())
    # TODO: Match price history graphs on website
    # TODO: Construct days to expiration. Useful feature?
    # TODO: Arbitrage analysis
    # cols = [iem.LOW_PX, iem.HIGH_PX, iem.AVG_PX, iem.LST_PX]
    # kwargs = dict(c='blue', marker='o', label='Training data')
    # plt.plot(sept16_df[cols], **kwargs)
