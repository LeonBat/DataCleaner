import pandas as pd
import pytest
from dctoolkit.cleaner import DataCleaner


def test_normalize_minmax_and_zscore(DataCleaner):
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})
    cleaner = DataCleaner(df.copy())
    assert cleaner.normalize_data(method="minmax") is None
    assert pytest.approx(cleaner.df.loc[0, "A"], rel=1e-6) == 0.0
    assert pytest.approx(cleaner.df.loc[4, "B"], rel=1e-6) == 1.0

    cleaner2 = DataCleaner(df.copy())
    assert cleaner2.normalize_data(method="zscore") is None
    assert abs(cleaner2.df["A"].mean()) < 1e-8


def test_normalize_invalid_method_raises(DataCleaner):
    df = pd.DataFrame({"x": [1, 2, 3]})
    cleaner = DataCleaner(df)
    with pytest.raises(ValueError):
        cleaner.normalize_data("unknown_method")


def test_functional_normalize_preserves_original(DataCleaner):
    df = pd.DataFrame({"const": [1, 1, 1], "x": [1, 2, 3]})
    cleaner = DataCleaner(df.copy())
    out = cleaner.normalize_data(method="minmax", inplace=False)
    assert isinstance(out, pd.DataFrame)
    assert (cleaner.df["const"] == 1).all()
