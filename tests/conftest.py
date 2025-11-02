import importlib.util
import pathlib
import pytest

# Try to import DataCleaner from the package, fall back to loading the module file
try:
    from dctoolkit.cleaner import DataCleaner as _DataCleaner
except Exception:
    try:
        import dctoolkit as _dc

        _DataCleaner = getattr(_dc, "DataCleaner", None)
    except Exception:
        _DataCleaner = None

    if _DataCleaner is None:
        # last-resort: load the module by path
        repo_root = pathlib.Path(__file__).parents[1]
        mod_path = repo_root / "dctoolkit" / "cleaner.py"
        spec = importlib.util.spec_from_file_location(
            "dctoolkit.cleaner", str(mod_path)
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _DataCleaner = getattr(mod, "DataCleaner")


@pytest.fixture
def DataCleaner():
    """Fixture returning the DataCleaner class."""
    return _DataCleaner
