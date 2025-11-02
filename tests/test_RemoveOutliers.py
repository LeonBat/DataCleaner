import pandas as pd
from dctoolkit.cleaner import DataCleaner

def test_remove_outliers_iqr_and_zscore_behavior(DataCleaner):
    df = pd.DataFrame({"A": [1, 2, 3, 4, 100], "B": [10, 20, 30, 40, 200]})

    cleaner = DataCleaner(df.copy())
    assert cleaner.remove_outliers(method="iqr") is None
    assert len(cleaner.df) < len(df)

    cleaner2 = DataCleaner(df.copy())
    # slightly tighter threshold helps detect the extreme value reliably in tests
    assert cleaner2.remove_outliers(method="zscore", threshold=1.9) is None
    assert len(cleaner2.df) < len(df)

    cleaner3 = DataCleaner(df.copy())
    assert cleaner3.remove_outliers(method="zscore", threshold=1000.0) is None
    assert len(cleaner3.df) == len(df)