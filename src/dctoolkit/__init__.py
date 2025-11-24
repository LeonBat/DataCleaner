from .cleaner import DataCleaner


def read_csv(path: str) -> DataCleaner:
    """
    This function reads a CSV file and returns a DataCleaner object.
    Mimics pandas.read_csv functionality.

    Parameters:
    - path: The path to the CSV file.

    Returns:
    - DataCleaner: An instance of the DataCleaner class initialized
    """
    return DataCleaner(path)


def __getattr__(self, name: str):
    """
    This function allows direct access to DataFrame methods and attributes
    from the DataCleaner class.
    """
    return getattr(self.df, name)
