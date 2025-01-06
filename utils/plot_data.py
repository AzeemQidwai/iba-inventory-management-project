import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def preprocess_data(data):
    """
    Prepares the DataFrame for monthly analysis by adding a 'Month' column.

    Args:
      data (pd.DataFrame): Input DataFrame containing a 'Date' column.

    Returns:
      pd.DataFrame: DataFrame with a 'Month' column and processed date values.
    """
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is datetime
    data['Month'] = data['Date'].dt.to_period('M')  # Extract month
    return data


def calculate_monthly_stock(data):
    """
    Calculates the opening and closing stock for each month.

    Args:
      data (pd.DataFrame): DataFrame containing stock data with 'Date',
                           'Open Stock Amount', and 'Closing Stock Amount' columns.

    Returns:
      pd.DataFrame: Monthly opening and closing stock amounts.
    """
    # Calculate opening stock for the 1st of each month
    opening_stock = data[data['Date'].dt.day == 1].groupby('Month')['Open Stock Amount'].sum()

    # Calculate closing stock for the last day of each month
    closing_stock = data.groupby('Month').apply(
        lambda x: x[x['Date'] == x['Date'].max()]['Closing Stock Amount'].sum()
    )

    # Combine results into a single DataFrame
    monthly_data = pd.DataFrame({
        'Opening Stock': opening_stock,
        'Closing Stock': closing_stock
    }).reset_index()

    monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()  # Convert to datetime for plotting
    return monthly_data


def calculate_monthly_material_flow(data):
    """
    Calculates the monthly Material Issued Amount and Material Received Amount.

    Args:
      data (pd.DataFrame): DataFrame containing material flow data with 'Material Issued Amount'
                           and 'Material Received Amount' columns.

    Returns:
      pd.DataFrame: Monthly Material Issued and Received amounts.
    """
    # Calculate Material Issued Amount for each month
    material_issued = data.groupby('Month')['Material Issued Amount'].sum()

    # Calculate Material Received Amount for each month
    material_received = data.groupby('Month')['Material Received Amount'].sum()

    # Combine results into a single DataFrame
    monthly_data = pd.DataFrame({
        'Material Issued': material_issued,
        'Material Received': material_received
    }).reset_index()

    monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()  # Convert to datetime for plotting
    return monthly_data


def plot_trends(monthly_data, y1, y2, labels, title, save_path):
    """
    Plots the trends for two metrics.

    Args:
      monthly_data (pd.DataFrame): DataFrame containing monthly data with a 'Month' column and the metrics to plot.
      y1 (str): Column name for the first metric.
      y2 (str): Column name for the second metric.
      labels (tuple): Labels for the two metrics (e.g., ('Opening Stock', 'Closing Stock')).
      title (str): Title of the plot.
      save_path (str): File path to save the plot.

    Returns:
      None. Displays the plot.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=monthly_data,
        x='Month',
        y=y1,
        label=labels[0],
        marker='o',
    )
    sns.lineplot(
        data=monthly_data,
        x='Month',
        y=y2,
        label=labels[1],
        marker='^',
    )
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title(title)
    plt.legend(title='Metric')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plt.savefig(save_path)
    plt.show()


def plot_monthly_stock(data, save_path='monthly_material_open_close.png'):
    """
    Main function to process data and plot monthly stock trends.

    Args:
      data (pd.DataFrame): Input DataFrame with inventory stock data.
      save_path (str): File path to save the plot.

    Returns:
      None. Displays the plot.
    """
    # Preprocess the data
    data = preprocess_data(data)

    # Calculate monthly stock trends
    monthly_data = calculate_monthly_stock(data)

    # Plot the trends
    plot_trends(
        monthly_data,
        y1='Opening Stock',
        y2='Closing Stock',
        labels=('Opening Stock', 'Closing Stock'),
        title='Monthly Opening and Closing Stock Trend',
        save_path=save_path,
    )


def plot_monthly_material_flow(data, save_path='monthly_material_flow.png'):
    """
    Main function to process data and plot monthly material flow trends.

    Args:
      data (pd.DataFrame): Input DataFrame with material flow data.
      save_path (str): File path to save the plot.

    Returns:
      None. Displays the plot.
    """
    # Preprocess the data
    data = preprocess_data(data)

    # Calculate monthly material flow trends
    monthly_data = calculate_monthly_material_flow(data)

    # Plot the trends
    plot_trends(
        monthly_data,
        y1='Material Issued',
        y2='Material Received',
        labels=('Material Issued', 'Material Received'),
        title='Monthly Material Issued and Received Trend',
        save_path=save_path,
    )

def plot_grouped_data(data, group_by_column, count_column, title, xlabel, ylabel, save_path, is_xticks=False, xticks_labels=None):
    """
    Generates a bar plot for grouped data using Seaborn.
    
    Parameters:
        data (pd.DataFrame): Input DataFrame.
        group_by_column (str): Column to group by.
        count_column (str): Column to count unique values.
        title (str): Plot title.
        xlabel (str): X-axis label.
        ylabel (str): Y-axis label.
        save_path (str): File path to save the plot.
        is_xticks (bool): Whether to modify x-tick labels.
        xticks_labels (list): Custom labels for x-ticks, if required.
    """
    grouped_data = data.groupby(group_by_column)[count_column].nunique().sort_values(ascending=False)
    
    # Display data
    display(grouped_data)
    
    # Plot using Seaborn
    sns.barplot(x=grouped_data.index, y=grouped_data.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if is_xticks and xticks_labels:
        plt.xticks(ticks=range(len(xticks_labels)), labels=xticks_labels)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


def group_and_plot(data, group_by_column, count_column, plot_type, bins=20, kde=True, title='', xlabel='', ylabel='', save_path=''):
    """
    Groups data by a column, performs unique count aggregation, and plots distribution.

    Parameters:
        data (pd.DataFrame): The input dataset.
        group_by_column (str): The column to group by.
        count_column (str): The column for counting unique values.
        plot_type (str): Type of plot ('bar' or 'hist').
        bins (int): Number of bins for histogram.
        kde (bool): Whether to include a KDE plot for histograms.
        color (str): Color of the plot.
        title (str): Plot title.
        xlabel (str): X-axis label.
        ylabel (str): Y-axis label.
        save_path (str): File path to save the plot.
    """
    grouped_data = data.groupby(group_by_column)[count_column].nunique().sort_values(ascending=False)

    # Display grouped data
    display(grouped_data)

    # Plot
    if plot_type == 'hist':
        sns.histplot(grouped_data, bins=bins, kde=kde)
    elif plot_type == 'bar':
        sns.barplot(x=grouped_data.index, y=grouped_data.values)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def calculate_and_plot_average_lead_time(data, group_by_column, agg_column, title, xlabel, ylabel, save_path):
    """
    Groups data, calculates average lead time, and plots distribution.

    Parameters:
        data (pd.DataFrame): The input dataset.
        group_by_column (str): The column to group by.
        agg_column (str): The column to calculate averages.
        title (str): Plot title.
        xlabel (str): X-axis label.
        ylabel (str): Y-axis label.
        save_path (str): File path to save the plot.
    """
    # Group by and calculate average lead time
    grouped_data = data.groupby(group_by_column, as_index=False).agg({agg_column: 'mean'}).rename(columns={agg_column: 'Average Lead Time'})

    # Display average lead time
    average_lead_time = grouped_data['Average Lead Time'].mean()
    print(f"Average Lead Time: {average_lead_time:.2f} days")

    # Plot distribution
    sns.histplot(grouped_data['Average Lead Time'], bins=20, kde=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def plot_daily_material_amount(data, column, save_path, title, y_label):
    """
    Plots the daily sum of the material issued amount over time using Seaborn and saves the plot as a PNG file.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the data.
        column (str): The name of the column representing the material issued amount.
        file_name (str): The name of the file to save the plot as.
        title (str): The title of the plot.
        y_label (str): The label for the Y-axis.
    """
    # Ensure the 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Group by 'Date' and sum the material issued amount for each date
    daily_issued_amount = data.groupby('Date')[column].sum().reset_index()

    # Create the line plot using Seaborn
    sns.lineplot(data=daily_issued_amount, x='Date', y=column)

    # Add titles and labels
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(y_label)

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # Adjust layout and gridlines
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(save_path, format='png')

    # Display the plot
    plt.show()


def plot_average_monthly_amount(data, column, save_path, title, y_label):
    """
    Plots the average monthly amount over time using Seaborn and saves the plot as a PNG file.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the data.
        column (str): The name of the column representing the amount to be averaged.
        file_name (str): The name of the file to save the plot as.
        title (str): The title of the plot.
        y_label (str): The label for the y-axis.
    """
    # Ensure the 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Extract the month and year from the 'Date' column
    data['Month'] = data['Date'].dt.to_period('M')

    # Group by 'Month' and calculate the average for the specified column
    monthly_average = data.groupby('Month')[column].mean().reset_index()

    # Create the line plot using Seaborn
    sns.lineplot(
        x=monthly_average['Month'].astype(str),
        y=monthly_average[column]
    )

    # Add titles and labels
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(y_label)

    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    plt.yticks()

    # Save the plot as a PNG file
    plt.tight_layout()
    plt.savefig(save_path, format='png')

    # Display the plot
    plt.show()


def plot_material_over_time(data, material_df, value_column, smoothed_column, title_prefix, y_label, file_prefix, window=7):
    """
    Plots separate graphs for materials over time, showing both original and smoothed values.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the data.
        material_df (pd.DataFrame): DataFrame with the list of materials to plot.
        value_column (str): Column name for the original values (e.g., 'Material Issued' or 'Material Received').
        smoothed_column (str): Column name for the smoothed values.
        title_prefix (str): Prefix for the plot title (e.g., 'Material Issued' or 'Material Received').
        y_label (str): Label for the Y-axis.
        file_prefix (str): Prefix for the saved file name.
        window (int): Window size for the rolling average. Default is 7.
    """
    for material in material_df['Material Code']:
        material_data = data[data['Material Code'] == material].sort_values('Date')  # Ensure data is sorted by date
        material_data[smoothed_column] = material_data[value_column].rolling(window=window, min_periods=1).mean()  # Apply rolling average


        # Create the plot using Seaborn
        sns.lineplot(
            data=material_data,
            x='Date',
            y=smoothed_column,
            label=f'{material} (Smoothed)',
            linewidth=2,
            linestyle='--',
            color='blue'
        )
        sns.lineplot(
            data=material_data,
            x='Date',
            y=value_column,
            label=f'{material} (Original)',
            alpha=0.4,
            color='orange'
        )

        # Add titles and labels
        plt.title(f'{title_prefix} Over Time: {material}')
        plt.xlabel('Date')
        plt.ylabel(y_label)

        # Add a legend
        plt.legend()

        # Save the plot
        plt.tight_layout()
        plt.savefig(f'../results/eda/{file_prefix}_over_time_{material}.png', format='png', dpi=300)

        # Display the plot
        plt.show()