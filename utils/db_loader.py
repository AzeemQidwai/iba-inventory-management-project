import sqlite3
import csv
from tqdm.notebook import tqdm
import argparse

# Function to create SQLite DB from CSV with tqdm for progress
def create_db_from_csv(csv_file, db_name, table_name):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the CSV file
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract headers
        columns = ', '.join([f'"{header}" TEXT' for header in headers])  # Define columns as TEXT

        # Create table with a primary key
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})')

        # Insert rows from CSV into the table with tqdm for progress
        rows = list(reader)  # Convert reader to a list for tqdm
        for row in tqdm(rows, desc="Inserting rows", unit="row"):
            placeholders = ', '.join(['?'] * len(row))  # Exclude placeholder for the primary key
            column_names = ', '.join([f'"{header}"' for header in headers])  # Properly quote column names
            cursor.execute(f'INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})', row)

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Main function
def main():
    parser = argparse.ArgumentParser(description="Create SQLite database from CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file.")
    parser.add_argument("db_name", help="Path to the SQLite database file.")
    parser.add_argument("table_name", help="Name of the table to create in the database.")

    args = parser.parse_args()

    create_db_from_csv(args.csv_file, args.db_name, args.table_name)

if __name__ == "__main__":
    main()
