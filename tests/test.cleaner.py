# File for testing the cleaner module

import pandas as pd
import numpy as np
from dctoolkit import DataCleaner


# Test functionality of function fill_missing

def test_fill_missing():

    #create a test sample
    data = pd.DataFrame({
        'A': [1, 2, np.nan, 4],
        'B': [np.nan, 2, 3, 4],
        'C': ['a', np.nan, 'c', 'd']
    })

    #save to csv
    data.to_csv('fill_missing.csv', index=False)
    



