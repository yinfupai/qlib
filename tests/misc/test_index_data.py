import numpy as np
import pandas as pd

import qlib.utils.index_data as idd

import unittest


class IndexDataTest(unittest.TestCase):
    def test_index_single_data(self):
        # Auto broadcast for scalar
        sd = idd.SingleData(0, index=["foo", "bar"])
        print(sd)

        # Support empty value
        sd = idd.SingleData()
        print(sd)

        # Bad case: the input is not aligned
        with self.assertRaises(ValueError):
            idd.SingleData(range(10), index=["foo", "bar"])

        # test indexing
        sd = idd.SingleData([1, 2, 3, 4], index=["foo", "bar", "f", "g"])
        print(sd)
        print(sd.iloc[1])  # get second row

        # Bad case: it is not in the index
        with self.assertRaises(KeyError):
            print(sd.loc[1])

        print(sd.loc["foo"])

        # Test slicing
        print(sd.loc[:"bar"])

        print(sd.iloc[:3])

    def test_index_multi_data(self):
        # Auto broadcast for scalar
        sd = idd.MultiData(0, index=["foo", "bar"], columns=["f", "g"])
        print(sd)

        # Bad case: the input is not aligned
        with self.assertRaises(ValueError):
            idd.MultiData(range(10), index=["foo", "bar"], columns=["f", "g"])

        # test indexing
        sd = idd.MultiData(np.arange(4).reshape(2, 2), index=["foo", "bar"], columns=["f", "g"])
        print(sd)
        print(sd.iloc[1])  # get second row

        # Bad case: it is not in the index
        with self.assertRaises(KeyError):
            print(sd.loc[1])

        print(sd.loc["foo"])

        # Test slicing

        print(sd.loc[:"foo"])

        print(sd.loc[:, "g":])

    def test_sorting(self):
        sd = idd.MultiData(np.arange(4).reshape(2, 2), index=["foo", "bar"], columns=["f", "g"])
        print(sd)
        sd.sort_index()

        print(sd)
        print(sd.loc[:"c"])

    def test_corner_cases(self):
        sd = idd.MultiData([[1, 2], [3, np.NaN]], index=["foo", "bar"], columns=["f", "g"])
        print(sd)

        self.assertTrue(np.isnan(sd.loc["bar", "g"]))

        # support slicing
        print(sd.loc[~sd.loc[:, "g"].isna().data.astype(np.bool)])

        print(self.assertTrue(idd.SingleData().index == idd.SingleData().index))

        # empty dict
        print(idd.SingleData({}))
        print(idd.SingleData(pd.Series()))

        sd = idd.SingleData()
        with self.assertRaises(KeyError):
            sd.loc["foo"]

        # replace
        sd = idd.SingleData([1, 2, 3, 4], index=["foo", "bar", "f", "g"])
        sd = sd.replace(dict(zip(range(1, 5), range(2, 6))))
        print(sd)
        self.assertTrue(sd.iloc[0] == 2)

    def test_ops(self):
        sd1 = idd.SingleData([1, 2, 3, 4], index=["foo", "bar", "f", "g"])
        sd2 = idd.SingleData([1, 2, 3, 4], index=["foo", "bar", "f", "g"])
        print(sd1 + sd2)
        new_sd = sd2 * 2
        self.assertTrue(new_sd.index == sd2.index)

        sd1 = idd.SingleData([1, 2, None, 4], index=["foo", "bar", "f", "g"])
        sd2 = idd.SingleData([1, 2, 3, None], index=["foo", "bar", "f", "g"])
        self.assertTrue(np.isnan((sd1 + sd2).iloc[3]))
        self.assertTrue(sd1.add(sd2).sum() == 13)

    def test_todo(self):
        pass
        # here are some examples which do not affect the current system, but it is weird not to support it
        # sd2 = idd.SingleData([1, 2, 3, 4], index=["foo", "bar", "f", "g"])
        # 2 * sd2


if __name__ == "__main__":
    unittest.main()