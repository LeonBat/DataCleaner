import pandas as pd
from dctoolkit.cleaner import DataCleaner


def test_init_with_dataframe_and_path(DataCleaner, tmp_path):
    df = pd.DataFrame({"x": [1, 2, None], "y": ["a", "b", "c"]})
    cleaner = DataCleaner(df)
    assert isinstance(cleaner.df, pd.DataFrame)
    # modifying original should not change cleaner.df (default copy=True)
    df.loc[0, "x"] = 999
    assert cleaner.df.loc[0, "x"] != 999

    # init from CSV path
    out = tmp_path / "tmp_init.csv"
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(out, index=False)
    cleaner2 = DataCleaner(str(out))
    assert isinstance(cleaner2.df, pd.DataFrame)
    assert list(cleaner2.df.columns) == ["a"]


def test_save_cleaned_data_writes_file(DataCleaner, tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    cleaner = DataCleaner(df)
    out = tmp_path / "out.csv"
    ret = cleaner.save_cleaned_data(str(out))
    assert ret is None
    assert out.exists()
    loaded = pd.read_csv(out)
    pd.testing.assert_frame_equal(loaded, cleaner.df)
