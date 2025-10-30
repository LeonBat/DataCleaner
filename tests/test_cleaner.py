#######################
# File for testing the cleaner module
#######################

#importing class Cleaner from cleaner module
import dctoolkit as dc

#Libraries
import pandas as pd


#### Testing the DataCleaner methods ####

#Sample dataframe for testing
def test_data():
    '''Creates a sample dataframe for testing purposes.'''
    data = {
        'A': [1, 2, None, 4, 5, None],
        'B': [None, 2, 3, None, 5, 6],
        'C': [1, None, None, 4, 5, 6]
    }
    df = pd.DataFrame(data)
    df.to_csv('test_data.csv', index=False)



# Testing function fill_missing
def test_fill_missing():
    '''Tests the fill_missing method of DataCleaner class.'''

    test_data() #creating test_data.csv

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
    test_data() #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_median = dc.read_csv("test_data.csv")

    #test median method
    assert cleaner_median.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_median.fill_missing("median") is None  # Check return type
    assert cleaner_median.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert cleaner_median.df.loc[2, 'A'] == 3.0  # Check specific filled value
    assert cleaner_median.df.loc[0, 'B'] == 4.0  # Check specific filled value


    ##### Testing mode strategy #####
    test_data() #creating test_data.csv

    #initialize DataCleaner with sample dataframe
    cleaner_mode = dc.read_csv("test_data.csv")

    #test mode method
    assert cleaner_mode.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_mode.fill_missing("mode") is None  # Check return type
    assert cleaner_mode.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert cleaner_mode.df.loc[2, 'A'] == 5  # Check specific filled value
    assert cleaner_mode.df.loc[0, 'B'] == 5  # Check specific filled value


    ##### Testing drop strategy #####
    test_data() #creating test_data.csv
    
    #initialize DataCleaner with sample dataframe
    cleaner_drop = dc.read_csv("test_data.csv")

    #test drop method
    assert cleaner_drop.df.isnull().sum() == 6  # Check initial missing values
    assert cleaner_drop.fill_missing("drop") is None  # Check return type
    assert cleaner_drop.df.isnull().sum().sum() == 0  # Check all missing values filled
    assert len(cleaner_drop.df) == 2  # Check number of rows after dropping

    
    




    
    



