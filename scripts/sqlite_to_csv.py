import sqlite3
import pandas as pd
import os

# SQLite database path
sqlite_db = '../data/raw/data.sqlite'

# Directory where CSV files will be saved
csv_output_dir = '../data/processed/'

# Create output directory if it doesn't exist
if not os.path.exists(csv_output_dir):
    os.makedirs(csv_output_dir)

# Connect to the SQLite database
sqlite_conn = sqlite3.connect(sqlite_db)
sqlite_cursor = sqlite_conn.cursor()

# Fetch all table names from the SQLite database
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Loop through all tables
for table_name in tables:
    table_name = table_name[0]
    print(f"Exporting table: {table_name}")
    
    # Load the table into a pandas DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
    
    # Define CSV file path for the current table
    csv_file_path = os.path.join(csv_output_dir, f"{table_name}.csv")
    
    # Export DataFrame to CSV
    df.to_csv(csv_file_path, index=False)
    
    print(f"Table {table_name} exported to {csv_file_path}")

# Close SQLite connection
sqlite_conn.close()

print("All tables have been exported to CSV files.")
