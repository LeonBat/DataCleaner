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
    def __init__(self, path: str):
        self.df = pd.read_csv(path)

    
    ### Methods ###

    #filling missing values
    def fill_missing(self, strategy: Literal["mean", "median", "mode", "drop"] = "mean") -> None:
        '''
        This function fills missing values in the provided data by 
        the specified strategy: "mean", "median", "mode", or "drop".

        Parameters:
        - strategy: The strategy to use for filling missing values. Options are
            "mean"
            "median"
            "mode"
            "drop"

        Returns:
        - None: The function modifies the dataframe in place.

        >>> DataCleaner.fill_missing("mean")

        >>> DataCleaner.fill_missing("replace")
        Traceback (most recent call last):
            ...
        ValueError: Unknown strategy: replace. Please choose from 'mean', 'median', 'mode', or 'drop'.    
        '''
        if strategy == "mean":
            self.df.fillna(self.df.mean(numeric_only=True), inplace=True)
        
        elif strategy == "median":
            self.df.fillna(self.df.median(numeric_only=True), inplace=True)

        elif strategy == "mode":
            for column in self.df.columns:
                self.df[column].fillna(self.df[column].mode()[0], inplace=True)
        
        elif strategy == "drop":
            self.df.dropna(inplace=True)
        
        else:
            raise ValueError(f"Unknown strategy: {strategy}. Please choose from 'mean', 'median', 'mode', or 'drop'.")



    #removing duplicates
    def remove_duplicates(self) ->None:
        '''
        This function removes duplicate rows from the dataframe.

        Parameters: None

        Returns: None: The function modifies the dataframe in place.

        >>> DataCleaner.remove_duplicates()
        '''
        self.df.drop_duplicates(inplace=True)



    #revmoving outliers
    def remove_outliers(self, method: Literal["zscore", "iqr"] = "zscore", threshold: Optional[float] = 3.0) -> None:
        '''
        This function removes outliers from the dataframe using the specified method:
        "zscore" or "iqr".

        Parameters:
        - method: The method to use for outlier detection. Options are
            -"zscore"
            -"iqr"
        - threshold: The threshold value for outlier detection. Default is 3.0 for z-score method.

        Returns: None: The function modifies the dataframe in place.

        >>> DataCleaner.remove_outliers("zscore", 3.0)
        >>> DataCleaner.remove_outliers("iqr")
        >>> DataCleaner.remove_outliers("remove_outlier")
        Traceback (most recent call last):
            ...
        ValueError: Unknown method: remove_outlier. Please choose from 'zscore' or 'iqr'.

        '''
        if method == "zscore":
            z_scores = np.abs((self.df - self.df.mean(numeric_only=True)) / self.df.std(numeric_only=True))
            self.df = self.df[(z_scores < threshold).all(axis=1)]
        
        elif method == "iqr":
            Q1 = self.df.quantile(0.25)
            Q3 = self.df.quantile(0.75)
            IQR = Q3 - Q1
            self.df = self.df[~((self.df < (Q1 - 1.5 * IQR)) | (self.df > (Q3 + 1.5 * IQR))).any(axis=1)]
        
        else:
            raise ValueError(f"Unknown method: {method}. Please choose from 'zscore' or 'iqr'.")
        
        #normalizing data
        def normalize_data(self, method: Literal["minmax", "zscore", "mean"] = "minmax") -> None:
            '''
            This function normalizes the data in the dataframe using the specified methods.

            Parameters:
            - method: The method to use for normalization. Options are
                -"minmax"
                -"zscore"
                -"mean"
                For default, "minmax" normalization is applied.
            
            Returns: None: The function modifies the dataframe in place.

            >>> DataCleaner.normalize_data("minmax")
            >>> DataCleaner.normalize_data("average")
            Traceback(most recent calls):
                ...
            ValueError(f"Unknown method: {method}. Please choose from 'minmax', 'zscore', or 'mean'.")
            '''

            if method == "minmax":
                self.df = (self.df - self.df.min(numeric_only=True)) / (self.df.max(numeric_only=True) - self.df.min(numeric_only=True))

            elif method == "zscore":
                self.df = (self.df - self.df.mean(numeric_only=True)) / self.df.std(numeric_only=True)

            elif method == "mean":
                self.df = (self.df - self.df.mean(numeric_only=True)) / (self.df.max(numeric_only=True) - self.df.min(numeric_only=True))
            
            else:
                raise ValueError(f"Unknown method: {method}. Please choose from 'minmax', 'zscore', or 'mean'.")
            


            #save cleaned data

            def save_cleaned_data(self, output_path: str) -> None:
                '''
                This function saves the cleaned dataframe to the specified output path.

                Parameters:
                - output_path: The path where the cleaned dataframe will be saved.

                Returns: None

                >>> DataCleaner.save_cleaned_data("cleaned_data.csv")
                '''
                self.df.to_csv(output_path, index=False)