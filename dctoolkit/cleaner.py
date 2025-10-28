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