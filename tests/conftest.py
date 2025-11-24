import importlib.util
import pathlib
import pytest
import sys

# ensure src/ is discoverable so `import dctoolkit` works without installing the package
repo_root = pathlib.Path(__file__).parents[1]
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# try normal import first
try:
    from dctoolkit.cleaner import DataCleaner as _DataCleaner
except Exception:
    # fallback: load module directly from src/dctoolkit/cleaner.py
    mod_path = src_dir / "dctoolkit" / "cleaner.py"
    if not mod_path.exists():
        raise FileNotFoundError(f"Expected module at {mod_path!s}")
    spec = importlib.util.spec_from_file_location("dctoolkit.cleaner", str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _DataCleaner = getattr(mod, "DataCleaner")


@pytest.fixture
def DataCleaner():
    """Fixture returning the DataCleaner class."""
    return _DataCleaner
