import unittest

import pandas as pd
import pytz

from iem import pricehistory as px_hist


class PriceHistoryTest(unittest.TestCase):
    def test_market_name(self):
        table_headers = px_hist._table_headers(HTML_STR)
        names = [px_hist._market_name(s) for s in table_headers]
        exp_names = ['Congress18', 'House18', 'Senate18']
        self.assertEqual(names, exp_names)

    def test_timestamp(self):
        table_headers = px_hist._table_headers(HTML_STR)
        tss = [px_hist._timestamp(s) for s in table_headers]
        ts_kwds = dict(year=2016, month=12, day=31, hour=7, minute=45, second=1)
        naive_ts = pd.Timestamp(**ts_kwds)
        exp_ts = naive_ts.tz_localize(pytz.timezone('US/Central'))
        for ts in tss:
            self.assertEqual(ts, exp_ts)


HTML_STR = """
<HTML>
<HEAD>
<!--  -------------------------------------------------------------  -->
<!--     WebExchange 1.0                                             -->
<!--         Copyright 1998-2010, Joyce E. Berg and Forrest D. Nelson  -->
<!--         All rights reserved.                                    -->
<!--                                                                 -->
<!--         for information contact:                                -->
<!--             joyce-berg@uiowa.edu                                -->
<!--             forrest-nelson@uiowa.edu                            -->
<!--                                                                 -->
<!--  -------------------------------------------------------------  -->

<TITLE>2018 Congressional Election Markets Quotes</TITLE>
</HEAD>

<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000FF" VLINK="#663399" ALINK="#FFFFFF">




<!-- crumb trail -->
<font face="Arial,Helvetica,sans-serif" color="#000000" size=2>
<a href="http://tippie.uiowa.edu/iem/markets/">Current Markets</a>
&nbsp;
<img src="../images/arrow2.gif" width="7" height="9" alt="" border="0">
&nbsp;
<a href="http://tippie.uiowa.edu/iem/markets/Congress18.html"><b>2018 Congress</b></a>
&nbsp;
<img src="../images/arrow2.gif" width="7" height="9" alt="" border="0">
&nbsp;
<a href="http://tippie.uiowa.edu/iem/markets/data_Congress18.html">2018 Congress Data</a>
&nbsp;
<img src="../images/arrow2.gif" width="7" height="9" alt="" border="0">
&nbsp;
<B>2018 Congress Quotes</b>
</font>
<HR size=1 NOSHADE>
<p></p>
<!-- end of crumb trail -->


<CENTER>
<H2>
Market Quotes:  Congress18\r
<BR>2018 Congressional Control Market.
</H2>

<FONT SIZE="-1">

Quotes current as of <B>07:45:01 CST, Saturday, December 31, 2016</B>.
</FONT>
<P>

<TABLE BORDER=1>
	<TR>
	<TD><B>Symbol</B></TD>
	<TD ALIGN="LEFT"><B>Bid</B></TD>
	<TD ALIGN="LEFT"><B>Ask</B></TD>
	<TD ALIGN="LEFT"><B>Last</B></TD>
	<TD ALIGN="LEFT"><B>Low</B></TD>
	<TD ALIGN="LEFT"><B>High</B></TD>
	<TD ALIGN="LEFT"><B>Average</B></TD>
	</TR>

<TR>
	<TD>DH_DS18</TD>
	<TD ALIGN="RIGHT">0.021</TD>
	<TD ALIGN="RIGHT">0.027</TD>
	<TD ALIGN="RIGHT">0.025</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>DH_RS18</TD>
	<TD ALIGN="RIGHT">0.026</TD>
	<TD ALIGN="RIGHT">0.038</TD>
	<TD ALIGN="RIGHT">0.039</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>RH_DS18</TD>
	<TD ALIGN="RIGHT">0.200</TD>
	<TD ALIGN="RIGHT">0.215</TD>
	<TD ALIGN="RIGHT">0.220</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>RH_RS18</TD>
	<TD ALIGN="RIGHT">0.650</TD>
	<TD ALIGN="RIGHT">0.694</TD>
	<TD ALIGN="RIGHT">0.698</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>OTHER18</TD>
	<TD ALIGN="RIGHT">0.023</TD>
	<TD ALIGN="RIGHT">0.049</TD>
	<TD ALIGN="RIGHT">0.030</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

</TABLE>



<BR>
| <A HREF="http://tippie.biz.uiowa.edu/iem/markets/pr_Congress18.html">Prospectus</A>
| <A HREF="../pricehistory/pricehistory_selectcontract.cfm?market_ID=369">Price History</A>
| <A HREF="../graphs/graph_Congress18.cfm">Graph</A>
|

<BR>

<HR>
<H2>
Market Quotes:  House18\r
<BR>2018 House Control Market.
</H2>

<FONT SIZE="-1">

Quotes current as of <B>07:45:01 CST, Saturday, December 31, 2016</B>.
</FONT>
<P>

<TABLE BORDER=1>
	<TR>
	<TD><B>Symbol</B></TD>
	<TD ALIGN="LEFT"><B>Bid</B></TD>
	<TD ALIGN="LEFT"><B>Ask</B></TD>
	<TD ALIGN="LEFT"><B>Last</B></TD>
	<TD ALIGN="LEFT"><B>Low</B></TD>
	<TD ALIGN="LEFT"><B>High</B></TD>
	<TD ALIGN="LEFT"><B>Average</B></TD>
	</TR>

<TR>
	<TD>RH.gain18</TD>
	<TD ALIGN="RIGHT">0.090</TD>
	<TD ALIGN="RIGHT">0.645</TD>
	<TD ALIGN="RIGHT">0.998</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>RH.hold18</TD>
	<TD ALIGN="RIGHT">0.115</TD>
	<TD ALIGN="RIGHT">0.645</TD>
	<TD ALIGN="RIGHT">0.096</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>RH.lose18</TD>
	<TD ALIGN="RIGHT">0.105</TD>
	<TD ALIGN="RIGHT">0.645</TD>
	<TD ALIGN="RIGHT">0.105</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

</TABLE>



<BR>
| <A HREF="http://tippie.biz.uiowa.edu/iem/markets/pr_House18.html">Prospectus</A>
| <A HREF="../pricehistory/pricehistory_selectcontract.cfm?market_ID=368">Price History</A>
| <A HREF="../graphs/graph_House18.cfm">Graph</A>
|



<BR>

<HR>
<H2>
Market Quotes:  Senate18\r
<BR>2018 Senate Control Market.
</H2>

<FONT SIZE="-1">

Quotes current as of <B>07:45:01 CST, Saturday, December 31, 2016</B>.
</FONT>
<P>

<TABLE BORDER=1>
	<TR>
	<TD><B>Symbol</B></TD>
	<TD ALIGN="LEFT"><B>Bid</B></TD>
	<TD ALIGN="LEFT"><B>Ask</B></TD>
	<TD ALIGN="LEFT"><B>Last</B></TD>
	<TD ALIGN="LEFT"><B>Low</B></TD>
	<TD ALIGN="LEFT"><B>High</B></TD>
	<TD ALIGN="LEFT"><B>Average</B></TD>
	</TR>

<TR>
	<TD>RS.gain18</TD>
	<TD ALIGN="RIGHT">0.410</TD>
	<TD ALIGN="RIGHT">0.650</TD>
	<TD ALIGN="RIGHT">0.161</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>RS.hold18</TD>
	<TD ALIGN="RIGHT">0.125</TD>
	<TD ALIGN="RIGHT">0.645</TD>
	<TD ALIGN="RIGHT">0.121</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

<TR>
	<TD>RS.lose18</TD>
	<TD ALIGN="RIGHT">0.071</TD>
	<TD ALIGN="RIGHT">0.645</TD>
	<TD ALIGN="RIGHT">0.071</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	<TD ALIGN="RIGHT">---</TD>
	</TR>

</TABLE>



<BR>
| <A HREF="http://tippie.biz.uiowa.edu/iem/markets/pr_Senate18.html">Prospectus</A>
| <A HREF="../pricehistory/pricehistory_selectcontract.cfm?market_ID=367">Price History</A>
| <A HREF="../graphs/graph_Senate18.cfm">Graph</A>
|

<BR>
<HR>
The source of these quotes is updated every 15 minutes.
To refresh your screen, use the refresh button on your browser.

<HR>
<CENTER>
| <A HREF="https://iemweb.biz.uiowa.edu/trader-login.html">Login and Trade</A> | <A HREF="https://iemweb.biz.uiowa.edu">WebEx Manual</A> | <A HREF="http://tippie.uiowa.edu/iem">IEM Home Page</A> |
</CENTER>
<HR>
Site maintained by <A HREF="mailto:iem@uiowa.edu">Iowa Electronic Markets</A>





</CENTER>

</BODY>
</HTML>
"""