import pandas as pd
from dctoolkit.cleaner import DataCleaner


def test_remove_duplicates_inplace_and_functional(DataCleaner):
    df = pd.DataFrame({"A": [1, 2, 2, 3], "B": ["a", "b", "b", "c"]})
    cleaner = DataCleaner(df.copy())
    assert cleaner.remove_duplicates() is None
    assert len(cleaner.df) == 3

    cleaner2 = DataCleaner(df.copy())
    out = cleaner2.remove_duplicates(inplace=False)
    assert isinstance(out, pd.DataFrame)
    assert len(out) == 3
    assert len(cleaner2.df) == 4
