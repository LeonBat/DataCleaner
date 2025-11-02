import pytest

# Provide DataCleaner class as a fixture for all tests
try:
    from dctoolkit.cleaner import DataCleaner as _DataCleaner
except Exception:
    import dctoolkit as dc

    _DataCleaner = getattr(dc, "DataCleaner", getattr(dc, "read_csv", None))


@pytest.fixture
def DataCleaner():
    return _DataCleaner
