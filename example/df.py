import pandas as pd


def drop_column_inplace(df, column_name):
    """
    Drops a column from the DataFrame inplace.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    column_name (str): The name of the column to drop.

    Returns:
    None
    """
    df.drop(columns=[column_name], inplace=True)


def drop_column_copy(df, column_name):
    """
    Drops a column from the DataFrame without modifying the original.

    Parameters:
    df (pd.DataFrame): The DataFrame to use.
    column_name (str): The name of the column to drop.

    Returns:
    pd.DataFrame: A new DataFrame with the column dropped.
    """
    return df.drop(columns=[column_name], inplace=False)


def fillna_inplace(df, value):
    return df.fillna(value, inplace=True)


def fillna_copy(df, value):
    return df.fillna(value, inplace=False)


def sort_values_inplace(df, by):
    return df.sort_values(by=by, inplace=True)


def sort_values_copy(df, by):
    return df.sort_values(by=by, inplace=False)
