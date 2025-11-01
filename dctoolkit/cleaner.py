####################################
# DataCleaner Toolkit               #
####################################

# This module provides data cleaning functionalities for dataframes.
# Features include:
# -Handling missing values
# -Removing duplicates
# -Normalizing data
# -Removing outliers



# Libraries
from typing import Literal, Optional
import pandas as pd
import numpy as np


# class DataCleaner

class DataCleaner:
    #constructor
    #class can read from CSV path or accept DataFrame directly

    def __init__(self, path_or_df: str | pd.DataFrame, *, copy: bool = True):
        '''
        This class can read from a CSV file or accept a DataFrame directly.

        Parameters:
        - path_or_df: The path to the CSV file or a pandas DataFrame.
        - copy: Whether to create a copy of the DataFrame when initialized with a DataFrame. Default is True.

        Returns: None
        >>> cleaner = DataCleaner("data.csv", copy=False)
        Returns: None
        >>> cleaner = DataCleaner(df)
        Returns: None
        '''
        if isinstance(path_or_df, pd.DataFrame):
            self.df = path_or_df.copy() if copy else path_or_df
        else:
            self.df = pd.read_csv(path_or_df)

    
    ### Methods ###

    #filling missing values
    def fill_missing(self, strategy: Literal["mean", "median", "mode", "drop"] = "mean", *, inplace: bool = True) -> Optional[pd.DataFrame]:
        '''
        This function fills missing values in the provided data by 
        the specified strategy: "mean", "median", "mode", or "drop".

        Parameters:
        - strategy: The strategy to use for filling missing values. Options are
            "mean"
            "median"
            "mode"
            "drop"
        -Default is "mean".

        Returns:
        - None: The function modifies the dataframe in place.
        - pd.DataFrame: If inplace is False, returns a new DataFrame with missing values filled.

        >>> cleaner.fill_missing("mean")

        >>> cleaner.fill_missing("replace")
        Traceback (most recent call last):
            ...
        ValueError: Unknown strategy: replace. Please choose from 'mean', 'median', 'mode', or 'drop'.    
        '''
        target = self.df if inplace else self.df.copy() #determines if inplace modification or copy
        if strategy == "mean":
            target.fillna(target.mean(numeric_only=True), inplace=True)

        elif strategy == "median":
            target.fillna(target.median(numeric_only=True), inplace=True)

        elif strategy == "mode":
            for column in target.columns:
                modes = target[column].mode()
                if not modes.empty:
                    target[column].fillna(modes.iloc[0], inplace=True)
                # if no mode (all NaN) leave values as NaN

        elif strategy == "drop":
            target.dropna(inplace=True)

        else:
            raise ValueError(f"Unknown strategy: {strategy}. Please choose from 'mean', 'median', 'mode', or 'drop'.")
        
        if inplace:
            self.df = target
            return None
        return target



    #removing duplicates
    def remove_duplicates(self, *, inplace: bool = True) -> Optional[pd.DataFrame]:
        '''
        This function removes duplicate rows from the dataframe.

        Parameters: None

        Returns: 
        - None: The function modifies the dataframe in place.
        - pd.DataFrame: If inplace is False, returns a new DataFrame with duplicates removed.

        >>> cleaner.remove_duplicates()
        '''
        if inplace:
            self.df.drop_duplicates(inplace=True)
            return None
        return self.df.drop_duplicates()



    #removing outliers
    def remove_outliers(self, method: Literal["zscore", "iqr"] = "zscore", threshold: Optional[float] = 3.0, *, inplace: bool = True) -> Optional[pd.DataFrame]:
        '''
        This function removes outliers from the dataframe using the specified method:
        "zscore" or "iqr".

        Parameters:
        - method: The method to use for outlier detection. Options are
            -"zscore"
            -"iqr"
        - threshold: The threshold value for outlier detection. Default is 3.0
        - Default method is "zscore".

        Returns: 
        - None: The function modifies the dataframe in place.
        - pd.DataFrame: If inplace is False, returns a new DataFrame with outliers removed.

        >>> cleaner.remove_outliers("zscore", 2.0)
        >>> cleaner.remove_outliers("iqr")
        >>> cleaner.remove_outliers("remove_outlier")
        Traceback (most recent call last):
            ...
        ValueError: Unknown method: remove_outlier. Please choose from 'zscore' or 'iqr'.

        '''
        target = self.df if inplace else self.df.copy()
        if method == "zscore":
            numeric = target.select_dtypes(include=[np.number])
            # avoid zero-division: replace zero std with 1 (no scaling)
            std = numeric.std(ddof=0).replace(0, 1)
            z_scores = np.abs((numeric - numeric.mean()) / std)
            mask = (z_scores < threshold).all(axis=1)
            target = target.loc[mask]

        elif method == "iqr":
            numeric = target.select_dtypes(include=[np.number])
            Q1 = numeric.quantile(0.25)
            Q3 = numeric.quantile(0.75)
            IQR = Q3 - Q1
            mask = ~((numeric < (Q1 - 1.5 * IQR)) | (numeric > (Q3 + 1.5 * IQR))).any(axis=1)
            target = target.loc[mask]

        else:
            raise ValueError(f"Unknown method: {method}. Please choose from 'zscore' or 'iqr'.")

        if inplace:
            self.df = target
            return None
        return target

        
    #normalizing data
    def normalize_data(self, method: Literal["minmax", "zscore", "mean"] = "minmax", *, inplace: bool = True) -> Optional[pd.DataFrame]:
        '''
        This function normalizes the data in the dataframe using the specified methods.

        Parameters:
         - method: The method to use for normalization. Options are
            -"minmax"
            -"zscore"
            -"mean"
        -Default: "minmax" normalization is applied.
            
        Returns: None: The function modifies the dataframe in place.

        >>> cleaner.normalize_data("minmax")
        >>> cleaner.normalize_data("average")
        Traceback(most recent calls):
            ...
        ValueError(f"Unknown method: {method}. Please choose from 'minmax', 'zscore', or 'mean'.")
        '''

        target = self.df if inplace else self.df.copy()
        numeric = target.select_dtypes(include=[np.number])
        if method == "minmax":
            denom = (numeric.max() - numeric.min()).replace(0, 1)
            target[numeric.columns] = (numeric - numeric.min()) / denom

        elif method == "zscore":
            std = numeric.std(ddof=0).replace(0, 1)
            target[numeric.columns] = (numeric - numeric.mean()) / std

        elif method == "mean":
            denom = (numeric.max() - numeric.min()).replace(0, 1)
            target[numeric.columns] = (numeric - numeric.mean()) / denom

        else:
            raise ValueError(f"Unknown method: {method}. Please choose from 'minmax', 'zscore', or 'mean'.")

        if inplace:
            self.df = target
            return None
        return target


    #save cleaned data

    def save_cleaned_data(self, output_path: str) -> None:
        '''
        This function saves the cleaned dataframe to the specified output path.

        Parameters:
            - output_path: The path where the cleaned dataframe will be saved.

        Returns: None

        >>> cleaner.save_cleaned_data("cleaned_data.csv")
        '''
        self.df.to_csv(output_path, index=False)