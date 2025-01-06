import pandas as pd

def process_dataframe(df):
    """
    Process the dataframe by converting columns to the appropriate types,
    dropping unnecessary columns, renaming columns, and converting 'Material Issued' to absolute values.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be processed.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    # Convert 'Material' column to string type
    df['Material'] = df['Material'].astype(str)

    # Convert 'From Date' and 'To Date' columns to datetime
    df['From Date'] = pd.to_datetime(df['From Date'], format='%d.%m.%Y')
    df['To Date'] = pd.to_datetime(df['To Date'], format='%d.%m.%Y')

    # Drop the 'To Date' and 'ValA' columns
    df.drop(columns=['To Date', 'ValA'], inplace=True)

    # Rename columns
    df.rename(columns={
        'Material': 'Material Code',
        'Material Description': 'Material Description',
        'Opening Stock': 'Open Stock',
        'Total Issue Quantities': 'Material Issued',
        'Total Receipt Qties': 'Material Received',
        'Closing Stock': 'Closing Stock',
        'From Date': 'Date',
        'BUn': 'Unit'
    }, inplace=True)

    # Convert 'Material Issued' to absolute values
    df['Material Issued'] = df['Material Issued'].abs()
    df['Prefix'] = df['Material Code'].str[0]

    return df

def process_lead_time_data(df):
    """
    Process the lead time data by converting 'Material Code' to string type
    and dropping the 'Material Description' column.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be processed.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    # Convert 'Material Code' column to string type
    df['Material Code'] = df['Material Code'].astype(str)

    # Drop the 'Material Description' column
    df.drop(columns=['Material Description'], inplace=True)

    return df

def merge_dataframes(data, lead_time_data, prefix_data):
    """
    Merge the dataframes based on the specified columns.

    Parameters:
    data (pd.DataFrame): The main DataFrame.
    lead_time_data (pd.DataFrame): The lead time DataFrame.
    prefix_data (pd.DataFrame): The prefix data DataFrame.

    Returns:
    pd.DataFrame: The merged DataFrame.
    """
    prefix_data['Code'] = prefix_data['Code'].astype(str)

    # Merge with prefix data
    inventory = data.merge(prefix_data, left_on="Prefix", right_on="Code", how="left").drop(columns=['Code'])

    # Merge with lead time data
    inventory = inventory.merge(lead_time_data, on="Material Code", how="left")

    return inventory