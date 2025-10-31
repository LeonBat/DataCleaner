#######################
# File for testing the cleaner module
#######################

#importing class Cleaner from cleaner module
import dctoolkit as dc

#Libraries
import pandas as pd
import os


#### Testing the DataCleaner methods ####

#Sample dataframe for testing
def test_data(functionstype:str) -> None:
    '''Creates a sample dataframes for testing purposes.
    
    Parameters:
    - functionstype: The type of function to test. Options are
        "fill_missing"
        "remove_duplicates"
        "normalize_data"
        "remove_outliers"
    
    Returns:
    - None: The function creates a CSV file named 'test_data.csv'.
    '''
    # dataframe for testing fill_missing
    if functionstype == "fill_missing":
        data_missing = {
            'A': [1, 2, None, 4, 5, None],
            'B': [None, 2, 3, None, 5, 6],
            'C': [1, None, None, 4, 5, 6]
        }
        df = pd.DataFrame(data_missing)
        df.to_csv('test_data.csv', index=False)

    # dataframe for testing remove_duplicates
    elif functionstype == "remove_duplicates":
        data_duplicates = {
            'A': [1, 2, 2, 4, 5, 5],
            'B': [1, 2, 2, 4, 5, 5],
            'C': [1, 2, 2, 4, 5, 5]
        }
        df = pd.DataFrame(data_duplicates)
        df.to_csv('test_data.csv', index=False)
    
    # dataframe for testing normalize_data
    elif functionstype == "normalize_data":
        data_normalize = {
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': [100, 200, 300, 400, 500]
        }
        df = pd.DataFrame(data_normalize)
        df.to_csv('test_data.csv', index=False)

    # dataframe for testing remove_outliers
    elif functionstype == "remove_outliers":
        data_outliers = {
            'A': [1, 2, 3, 4, 100],
            'B': [10, 20, 30, 40, 200],
            'C': [100, 200, 300, 400, 3000]
        }
        df = pd.DataFrame(data_outliers)
        df.to_csv('test_data.csv', index=False)

    elif functionstype == "clean":
        data_clean = {
            "A": [1, 2, 3, 4, 5],
            "B": [6, 7, 8, 9, 10],
            "C": [11, 12, 13, 14, 15]
        }
        df = pd.DataFrame(data_clean)
        df.to_csv('test_data.csv', index=False)
    
    else:
        print("Invalid functionstype provided.")





# Testing function fill_missing
def test_fill_missing():
    '''Tests the fill_missing method of DataCleaner class.'''

    test_data("fill_missing") #creating test_data.csv

    ##### Testing mean strategy #####
    #initialize DataCleaner with sample dataframe
    cleaner_mean = dc.read_csv("test_data.csv")

    #test mean method
    assert cleaner_mean.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_mean.fill_missing("mean") is None  # Check return type
    assert cleaner_mean.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert cleaner_mean.df.loc[2, 'A'] == 3.0  # Check specific filled value
    assert cleaner_mean.df.loc[0, 'B'] == 4.0  # Check specific filled value

    ##### Testing median strategy #####
    test_data("fill_missing") #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_median = dc.read_csv("test_data.csv")

    #test median method
    assert cleaner_median.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_median.fill_missing("median") is None  # Check return type
    assert cleaner_median.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert cleaner_median.df.loc[2, 'A'] == 3.0  # Check specific filled value
    assert cleaner_median.df.loc[0, 'B'] == 4.0  # Check specific filled value


    ##### Testing mode strategy #####
    test_data("fill_missing") #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_mode = dc.read_csv("test_data.csv")

    #test mode method
    assert cleaner_mode.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_mode.fill_missing("mode") is None  # Check return type
    assert cleaner_mode.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert cleaner_mode.df.loc[2, 'A'] == 5  # Check specific filled value
    assert cleaner_mode.df.loc[0, 'B'] == 5  # Check specific filled value


    ##### Testing drop strategy #####
    test_data("fill_missing") #creating test_data.csv
    
    #initialize DataCleaner with sample dataframe
    cleaner_drop = dc.read_csv("test_data.csv")

    #test drop method
    assert cleaner_drop.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_drop.fill_missing("drop") is None  # Check return type
    assert cleaner_drop.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert len(cleaner_drop.df) == 2  # Check number of rows after dropping

    ##### Testing invalid strategy #####
    assert cleaner_drop.fill_missing("invalid_strategy") is None  # Check return type

    # Remove test dataframe
    if os.path.exists("test_data.csv"):
        os.remove("test_data.csv")

    


# Testing function remove_duplicates
def test_remove_duplicates():
    '''Tests the remove_duplicates method of DataCleaner class.'''

    test_data("remove_duplicates") #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_duplicates = dc.read_csv("test_data.csv")

    ##### test remove_duplicates method #####
    assert len(cleaner_duplicates.df) == 6  # Check initial number of rows
    assert cleaner_duplicates.remove_duplicates() is None  # Check return type
    assert len(cleaner_duplicates.df) == 3  # Check number of rows after removing duplicates

    ##### Testing invalid strategy #####
    assert cleaner_duplicates.fill_missing("invalid_strategy") is None  # Check return type


    assert len(cleaner_duplicates.df) == 5  # Check initial number of rows
    assert cleaner_duplicates.remove_duplicates() is None  # Check return type
    assert len(cleaner_duplicates.df) == 5  # Check number of rows remains the

    

    # Remove test dataframe
    if os.path.exists("test_data.csv"):
        os.remove("test_data.csv")

    

# testing function remove_outliers
def test_remove_outliers():
    '''Tests the remove_outliers method of DataCleaner class.'''

    test_data("remove_outliers") #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_outliers = dc.read_csv("test_data.csv")

    ##### test remove_outliers method #####
    assert len(cleaner_outliers.df) == 5  # Check initial number of rows
    assert cleaner_outliers.remove_outliers() is None  # Check return type
    assert len(cleaner_outliers.df) == 2  # Check number of rows after removing outliers

    ##### Testing method with no outliers #####
    test_data("clean") #creating test_data.csv

    assert len(cleaner_outliers.df) == 5  # Check initial number of rows
    assert cleaner_outliers.remove_outliers() is None  # Check return type
    assert len(cleaner_outliers.df) == 5  # Check number of rows remains the same

    # Remove test dataframe
    if os.path.exists("test_data.csv"):
        os.remove("test_data.csv")



# Testing function normalize_data
def normalize_data():
    '''Tests the normalize_data method of DataCleaner class.'''

    test_data("normalize_data") #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_normalize = dc.read_csv("test_data.csv")

    ##### test normalize_data method #####
    assert cleaner_normalize.normalize_data() is None  # Check return type
    assert abs(cleaner_normalize.df.loc[0, 'A'] - 0.0) < 1e-6  # Check specific normalized value
    assert abs(cleaner_normalize.df.loc[4, 'B'] - 1.0) < 1e-6  # Check specific normalized value
    assert abs(cleaner_normalize.df.loc[2, 'C'] - 0.5) < 1e-6  # Check specific normalized value

    # Remove test dataframe
    if os.path.exists("test_data.csv"):
        os.remove("test_data.csv")


    
###### Testing a clean dataframe ######
# Will there be intervention
def test_clean_dataframe():
    '''Tests the methods of DataCleaner class on a clean dataframe.'''

    test_data("clean") #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_clean = dc.read_csv("test_data.csv")

    #### test fill_missing method #####
    assert cleaner_clean.fill_missing("mean") is None  # Check return type
    assert cleaner_clean.df.isnull().sum().sum() == 0  # Check no missing values
    assert len(cleaner_clean.df) == 5  # Check number of rows remains the same

    ##### test remove_duplicates method #####
    assert len(cleaner_clean.df) == 5  # Check initial number of rows
    assert cleaner_clean.remove_duplicates() is None  # Check return type
    assert len(cleaner_clean.df) == 5  # Check number of rows remains the same

    ##### test remove_outliers method #####
    assert len(cleaner_clean.df) == 5  # Check initial number of rows
    assert cleaner_clean.remove_outliers() is None  # Check return type
    assert len(cleaner_clean.df) == 5  # Check number of rows remains the same

    ##### test normalize_data method #####
    assert cleaner_clean.normalize_data() is None  # Check return type
    assert abs(cleaner_clean.df.loc[0, 'A'] - 0.0) < 1e-6  # Check specific normalized value
    assert abs(cleaner_clean.df.loc[4, 'B'] - 1.0) < 1e-6  # Check specific normalized value
    assert abs(cleaner_clean.df.loc[2, 'C'] - 0.5) < 1e-6  # Check specific normalized value

    # Remove test dataframe
    if os.path.exists("test_data.csv"):
        os.remove("test_data.csv")




    
    



