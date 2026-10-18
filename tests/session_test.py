import pandas as pd

import pyiem

table_text = """
<table id="data-table" class="table table-striped form-table jumbotronTable" aria-describedby="Trader activity table">
<h2>Outstanding Bid: FRup1216</h2>
<thead>
    <tr>
        <th><label for="order.date">Order Date</label></th>
        <th><label for="market">Market</label></th>
        <th><label for="contract">Contract</label></th>
        <th><label for="order.type">Order Type</label></th>
        <th><label for="quantity">Quantity</label></th>
        <th><label for="price">Price</label></th>
        <th><label for="expiration">Expiration</label></th>
        <th><label for="order.cancelOrder">Cancel Order</label></th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>2016-11-02 20:30:54.257</td>
        <td>FedPolicyB</td>
        <td>FRup1216</td>
        <td>bid</td>
        <td>1.000000</td>
        <td>0.001000</td>
        <td></td>
        <td>
        <a data-confirm-button="Yes, cancel this order" ata-cancel-button="No, take me back" data-text="Are you sure you wish to cancel this order?" href="/pyiem/trader/TraderActivity.action?cancelBidOrder=&amp;market=51&amp;bidOrder=4600000&amp;asset=3054&amp;activityType=bid" title="Cancel this order" class="submitBtn confirm"><img class="cancelOrderBtn" src="/pyiem/images/x_icon_red.png" alt="Cancel this bid order"/>
        </a>
        </td>
    </tr>
</tbody>
</table>
"""


def main():
    date_cols = [pyiem.ORDER_DATE, pyiem.EXPIRATION]
    kwargs = dict(index_col=pyiem.ORDER_DATE, parse_dates=date_cols)
    dfs = pd.read_html(table_text, **kwargs)
    df = dfs[0]

    oid_df = pd.DataFrame()
    cxl_o = pyiem.CANCEL_ORDER
    df[cxl_o] = df[cxl_o].combine_first(oid_df[cxl_o])
