import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

# Create Spark session
spark = SparkSession.builder \
    .master("local") \
    .appName("Data Cleaning and Ingestion") \
    .getOrCreate()

# Load CSV into Spark DataFrame
def load_data(file_path):
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    # df.show(10)
    # df.printSchema()
    return df

# Clean DataFrame (example)
def clean_customers_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()
    
    # Fill missing values (you can customize based on your dataset)
    df_clean = df_clean.na.fill({"addressLine2": "", "state": "", "creditLimit": 0})
    df_clean = df_clean.na.fill({"salesRepEmployeeNumber": 0})

    # Rename columns to remove spaces and standardize names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    df_clean = df_clean.withColumn("salesRepEmployeeNumber", col("salesRepEmployeeNumber").cast("integer"))
    df_clean = df_clean.withColumn("creditLimit", col("creditLimit").cast("double"))

    # Clean phone number (remove special characters)
    df_clean = df_clean.withColumn("phone", regexp_replace(col("phone"), r"[\s\.\-\(\)]", ""))
    # df_clean.show(10)
    return df_clean
# Helper function to clean phone numbers
def clean_phone_number(phone_col):
    # Replace non-digit characters except "+" with an empty string
    cleaned_phone = F.regexp_replace(phone_col, "[^+0-9]", "")
    return cleaned_phone

def clean_employees_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()
    
    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    # Clean phone numbers if a phone column exists
    if 'phone' in df_clean.columns:
        df_clean = df_clean.withColumn('phone', clean_phone_number(F.col('phone')))
    
    return df_clean

def clean_offices_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()

    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    # Clean phone numbers
    if 'phone' in df_clean.columns:
        df_clean = df_clean.withColumn('phone', clean_phone_number(F.col('phone')))
    
    return df_clean

def clean_orderdetails_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()

    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    return df_clean

def clean_orders_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()
    df_clean = df_clean.withColumn(
        'shipped_date', 
        F.when(F.col('shipped_date') == 'NaN', None)
         .otherwise(F.to_date(df_clean['shipped_date'], 'yyyy-MM-dd'))
    )
    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    return df_clean

def clean_payments_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()

    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    return df_clean

def clean_productlines_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()

    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    return df_clean

def clean_products_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()

    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    return df_clean

def clean_warehouses_data(df):
    # Drop duplicates
    df_clean = df.dropDuplicates()

    # Standardize column names
    for col_name in df_clean.columns:
        df_clean = df_clean.withColumnRenamed(col_name, col_name.replace(" ", "_").lower())
    
    return df_clean
# Save cleaned DataFrame locally as CSV (optional)
def save_cleaned_data(df, output_file_path):
    # Assuming `df` is a Spark DataFrame
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_file_path)

    # Rename the generated part file to the desired output name
    import os
    import shutil

    # Identify the generated part file
    part_file = [f for f in os.listdir(output_file_path) if f.startswith("part") and f.endswith(".csv")][0]
    part_file_path = os.path.join(output_file_path, part_file)

    # Move and rename the part file to replace the directory
    final_output_path = f"{output_file_path}.csv"
    shutil.move(part_file_path, final_output_path)

    # Remove all files in the directory
    for f in os.listdir(output_file_path):
        os.remove(os.path.join(output_file_path, f))

    # Remove the directory
    os.rmdir(output_file_path)

# Main execution
if __name__ == "__main__":
    files_names = { "orders"}
    # files_names = {"customers", "employees", "offices", "orderdetails", "orders", "payments", "productlines", "products", "warehouses"}
    input_path = "../data/processed/"
    output_cleaned_path = "../data/cleaned/"

    # Iterate over each file and process it
    for file_name in files_names:
        file_path = f"{input_path}{file_name}.csv"  # Input file path
        output_file_path = f"{output_cleaned_path}{file_name}"  # Output cleaned file path (no .csv yet)

        # Load and clean data
        print(f"Processing {file_name}...")
        df = load_data(file_path)
        cleaning_function_name = f"clean_{file_name}_data"
        
        if cleaning_function_name in globals():
            clean_function = globals()[cleaning_function_name]
            df_clean = clean_function(df)
            
            # Save cleaned data
            save_cleaned_data(df_clean, output_file_path)
            print(f"Cleaned {file_name} saved to {output_file_path}.csv")
        else:
            print(f"No cleaning function found for {file_name}. Skipping...")