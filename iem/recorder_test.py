import unittest
from io import StringIO
from pathlib import Path

import pandas as pd

import iem


class HFDStoreTest(unittest.TestCase):
    def testMkdir(self):
        parent_path = Path('data/')
        with self.assertRaises(FileExistsError):
            parent_path.mkdir()

    def testDuplicateData(self):
        s = """Timestamp,Symbol,Bid,Ask,Last,Low,High,Average
        2016-11-19 06:45:00-06:00,FRup1216,0.9,0.95,0.95,,,
        2016-11-19 06:45:00-06:00,FRsame1216,0.07,0.125,0.061,,,
        2016-11-19 06:45:00-06:00,FRdown1216,0.0,0.001,0.002,,,
        2016-11-19 06:45:00-06:00,FRup0117,0.14,0.49,0.145,,,
        2016-11-19 06:45:00-06:00,FRsame0117,0.525,0.895,0.519,,,
        2016-11-19 06:45:00-06:00,FRdown0117,0.002,0.003,0.002,,,
        """
        df = pd.read_csv(StringIO(s), index_col=[iem.TIMESTAMP, iem.SYMBOL])
        dedupe_idx = df.index.difference(df.index)
        iter_df = df.reindex(dedupe_idx)
        self.assertEqual(len(iter_df), 0)


