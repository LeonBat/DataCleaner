# DataCleaner

The DataCleaner is a small utility that provides functionality for preprocessing dataframes. 
It is based on the pandas package and it provides basic data cleaning functionalities like:

- filling missing values
- removing duplicate values
- removing outliers
- normalizing data


This README covers quick install, usage examples, testing and notes about the API.


## Installation and Import

You can install the package using pip

````bash
python -m pip install datacleaner
````

Before starting you need to set up an environment. 

### environment.yml
name: toolkit
channels:
  - defaults
  - conda-forge
dependencies:
  - python = 3.11
  - pandas
  - numpy
  - typing
  - pytest
  - pytest-mock
  - black


## Quick Start

Import Datacleaner
````python
import pandas as pd
from dctoolkit.cleaner import DataCleaner
````

````python
# from DataFrame (default copy=True -> original is not mutated)
df = pd.DataFrame({"A":[1, None, 3], "B":[10, 20, 200]})
cleaner = DataCleaner(df)
````

using datacleaner

````python
# inplace (default): modifies cleaner.df and returns None
cleaner.fill_missing("mean")              # fill numeric columns with mean
cleaner.remove_duplicates()               # drop duplicate rows
cleaner.remove_outliers(method="iqr")     # remove rows outside 1.5*IQR for numeric cols
cleaner.normalize_data(method="minmax")   # scale numeric cols to [0,1]
cleaner.save_cleaned_data("out.csv")      # write to CSV
````


````python
# functional usage: return a cleaned DataFrame without mutating cleaner.df
new_df = cleaner.fill_missing("mode", inplace=False)
filtered = cleaner.remove_outliers(method="zscore", threshold=1.9, inplace=False)
scaled = cleaner.normalize_data(method="zscore", inplace=False)
````

reading in from csv path
````python
# construct from CSV path
cleaner2 = DataCleaner("data.csv")
````

## API Summary

**Constructor**

DataCleaner(path_or_df: str | pandas.DataFrame, *, copy: bool = True)
If a DataFrame is passed and copy=True (default), the constructor copies it to avoid mutating the caller's DataFrame.
If copy=False, inplace operations will affect the original DataFrame.

**Core methods (mutating by default)**

fill_missing(strategy: "mean"|"median"|"mode"|"drop", *, inplace: bool = True) -> Optional[pd.DataFrame]

- mean/median: numeric-only filling
- mode: per-column mode (safe when all-NaN -> left unchanged)
- drop: drop rows with any NaN
- returns None when inplace=True else returns a new DataFrame
- remove_duplicates(*, inplace: bool = True) -> Optional[pd.DataFrame]

remove_duplicates(*, inplace: bool = True) -> Optional[pd.DataFrame]
- drop duplicate rows

remove_outliers(method: "zscore"|"iqr" = "zscore", threshold: float = 3.0, *, - inplace: bool = True) -> Optional[pd.DataFrame]

operates on numeric columns only; preserves non-numeric columns
- zscore: removes rows whose numeric columns exceed the z-score threshold (per-column)
- iqr: removes rows outside 1.5 * IQR per numeric column

normalize_data(method: "minmax"|"zscore"|"mean" = "minmax", *, inplace: bool = True) -> Optional[pd.DataFrame]

- numeric-only normalization, constant columns handled to avoid division-by-zero
- minmax: normalizes data with minmax method
- score: normalizes data with zscore method
- mean: normalizes data with mean method

save_cleaned_data(output_path: str) -> None
- writes self.df to CSV (index=False)


**Notes**
- Methods accept inplace=False to return a new DataFrame instead of modifying self.df.
- Non-numeric columns are preserved by outlier removal and normalization operations.
- Mode-filling will not raise for all-NaN columns; NaNs are left intact if no mode exists.


## Contributing
- Fork, create a PR with a clear description and tests for new behavior.
- Follow code style (Black) and add/update tests for bug fixes and new features.

## License

MIT License

Copyright (c) 2025 Leon Otto Gasteiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

Open an issue or PR on the repository for questions or contributions.


