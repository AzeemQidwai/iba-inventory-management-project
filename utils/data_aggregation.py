import pandas as pd

def get_aggregate_flow(data, column):
    """
    Calculate the aggregate
    """
    # Group by 'Type' and aggregate the sums
    grouped = data.groupby(column).agg({
      'Material Issued Amount': 'sum',
      'Material Received Amount': 'sum'
    }).reset_index()

    # Calculate the total sums
    total_issued = grouped['Material Issued Amount'].sum()
    total_received = grouped['Material Received Amount'].sum()

    # Calculate the percentages
    grouped['Material Issued Amount %'] = (grouped['Material Issued Amount'] / total_issued) * 100
    grouped['Material Received Amount %'] = (grouped['Material Received Amount'] / total_received) * 100

    return grouped


def get_top_stock(data, date_column, stock_columns, sort_by, top_n=10, earliest=True):
    """
    Gets the top materials by stock on the earliest or latest date.

    Parameters:
        data (pd.DataFrame): The input DataFrame.
        date_column (str): The column name representing dates.
        stock_columns (list): List of columns to include in the result (e.g., material codes and stock values).
        sort_by (str): The column to sort by for top N results.
        top_n (int): Number of top materials to return. Default is 10.
        earliest (bool): Whether to filter by the earliest date. If False, filters by the latest date.

    Returns:
        pd.DataFrame: The top materials by stock for the specified date.
    """
    # Get the target date
    target_date = data[date_column].min() if earliest else data[date_column].max()

    # Filter data for the target date
    filtered_data = data[data[date_column] == target_date][stock_columns]

    # Get the top N materials by the specified column
    top_stock = filtered_data.sort_values(by=sort_by, ascending=False).head(top_n)

    return target_date, top_stock

def get_top_stock_by_date(data, date_column, stock_columns, sort_by, top_n=10, earliest=True):
    """
    Gets the top materials by stock on the earliest or latest date.

    Parameters:
        data (pd.DataFrame): The input DataFrame.
        date_column (str): The column name representing dates.
        stock_columns (list): List of columns to include in the result (e.g., material codes and stock values).
        sort_by (str): The column to sort by for top N results.
        top_n (int): Number of top materials to return. Default is 10.
        earliest (bool): Whether to filter by the earliest date. If False, filters by the latest date.

    Returns:
        pd.Timestamp, pd.DataFrame: The target date and the top materials by stock for that date.
    """
    # Get the target date
    target_date = data[date_column].min() if earliest else data[date_column].max()

    # Filter data for the target date
    filtered_data = data[data[date_column] == target_date][stock_columns]

    # Get the top N materials by the specified column
    top_stock = filtered_data.sort_values(by=sort_by, ascending=False).head(top_n)

    return target_date, top_stock


def merge_stock_data(primary_stock, secondary_stock, merge_on):
    """
    Merges primary stock data with secondary stock data on a specified key.

    Parameters:
        primary_stock (pd.DataFrame): The primary stock DataFrame.
        secondary_stock (pd.DataFrame): The secondary stock DataFrame to merge.
        merge_on (str): The column name to merge on.

    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    return primary_stock.merge(secondary_stock, on=merge_on, how='left')