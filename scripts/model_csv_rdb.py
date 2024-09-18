import psycopg2
import os 
import pandas as pd

db_host = 'localhost'
db_name = 'modelcars'
db_user = 'postgres'
db_password = 'Kamui'

csv_path = '../data/cleaned/'

# Function to connect to PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        conn.autocommit = False  # To control transactions manually
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to insert data into a table
def insert_data_from_csv(conn, table_name, file_name):
    try:
        cursor = conn.cursor()

        # Load CSV data into a DataFrame
        csv_file_path = os.path.join(csv_path, file_name)
        df = pd.read_csv(csv_file_path)

        # Generate column names from the DataFrame
        columns = ', '.join(df.columns)

        # Prepare the SQL statement for insertion
        for index, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
            
            # Execute the insert command
            cursor.execute(sql, tuple(row))

        conn.commit()
        print(f"Data inserted successfully into {table_name}")

    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        conn.rollback()

# Main function to orchestrate the data loading
def load_all_data():
    # Connect to the database
    conn = connect_to_db()
    if conn is None:
        return

    try:
        # Order matters: Insert parent tables first to respect foreign key constraints
        # insert_data_from_csv(conn, 'customers', 'customers.csv')
        # insert_data_from_csv(conn, 'products', 'products.csv')
        # insert_data_from_csv(conn, 'offices', 'offices.csv')
        # insert_data_from_csv(conn, 'employees', 'employees.csv')
        # insert_data_from_csv(conn, 'product_lines', 'product_lines.csv')
        insert_data_from_csv(conn, 'orders', 'orders.csv')
        # insert_data_from_csv(conn, 'order_details', 'order_details.csv')
        # insert_data_from_csv(conn, 'payments', 'payments.csv')
        # insert_data_from_csv(conn, 'warehouses', 'warehouses.csv')

    except Exception as e:
        print(f"Error during data loading: {e}")

    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    load_all_data()

# 10167,2003-10-23,2003-10-30,NULL,Cancelled,Customer called to cancel. The warehouse was notified in time and the order didn't ship. They have a new VP of Sales and are shifting their sales model. Our VP of Sales should contact them.,448