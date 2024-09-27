import psycopg2
import pandas as pd

try:
    conn = psycopg2.connect(
        dbname="modelcars",
        user="postgres",
        password="Kamui",
        host="localhost",
        port="5433"
    )

    df = pd.read_sql(f"SELECT * FROM customers", conn)
    print(df.head())
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
