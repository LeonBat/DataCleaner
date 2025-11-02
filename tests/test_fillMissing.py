import pandas as pd
import pytest
from dctoolkit.cleaner import DataCleaner


def test_fill_missing_invalid_strategy_raises(DataCleaner):
    df = pd.DataFrame({"n": [1, None, 3], "s": ["x", None, "z"]})
    cleaner = DataCleaner(df)
    with pytest.raises(ValueError):
        cleaner.fill_missing("not_a_strategy")


def test_fill_missing_mean_median_mode_and_drop(DataCleaner):
    df = pd.DataFrame({"num": [1, None, 3], "cat": ["a", None, "a"]})
    cleaner = DataCleaner(df.copy())
    assert cleaner.fill_missing("mean") is None
    assert cleaner.df["num"].isnull().sum() == 0
    assert cleaner.df["cat"].isnull().sum() == 1

    assert cleaner.fill_missing("mode") is None
    assert cleaner.df["cat"].isnull().sum() == 0

    cleaner2 = DataCleaner(df.copy())
    assert cleaner2.fill_missing("median") is None
    assert cleaner2.df.loc[1, "num"] == pytest.approx(2.0)

    cleaner3 = DataCleaner(df.copy())
    assert cleaner3.fill_missing("drop") is None
    assert len(cleaner3.df) == 2


def test_fill_missing_mode_on_all_na_does_not_raise(DataCleaner):
    df = pd.DataFrame({"A": [None, None]})
    cleaner = DataCleaner(df.copy())
    cleaner.fill_missing("mode")  # should not raise
    assert cleaner.df["A"].isnull().all()