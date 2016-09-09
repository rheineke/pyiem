from matplotlib import pyplot as plt

from analysis import hdf_store

import iem


def get_new_fignum():
    fignums = plt.get_fignums()
    if fignums:
        return max(fignums) + 1
    else:
        return 1

if __name__ == '__main__':
    mkt_name = 'FedPolicyB'
    with hdf_store.open_store(mode='r') as hdf_store:
        px_hist_df = hdf_store[mkt_name]

    df = px_hist_df.copy()
    df = df.reset_index(level=iem.CONTRACT)
    sept16_lbl = df[iem.CONTRACT].str.contains('0916')
    sept16_df = df.loc[sept16_lbl]

    plt.figure(get_new_fignum())
    # TODO: Match price history graphs on website
    # TODO: Construct days to expiration. Useful feature?
    # TODO:
    cols = [iem.LOW_PX, iem.HIGH_PX, iem.AVG_PX, iem.LST_PX]
    kwargs = dict(c='blue', marker='o', label='Training data')
    plt.plot(sept16_df[cols], **kwargs)
