"""
### Run notebooks in databricks as a Databricks Workflow using the Airflow Databricks provider

This DAG runs two Databricks notebooks as a Databricks workflow.
"""
from airflow.decorators import dag
from airflow.providers.databricks.operators.databricks import DatabricksNotebookOperator, DatabricksSubmitRunOperator
from airflow.providers.databricks.operators.databricks_workflow import (
    DatabricksWorkflowTaskGroup,
)
from airflow.models.baseoperator import chain
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from pendulum import datetime
from datetime import timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
import pandas as pd 
import psycopg2 as db

DATABRICKS_LOGIN_EMAIL = "bmsakamali@gmail.com"
DATABRICKS_NOTEBOOK_NAME_1 = "postgre_nb"
DATABRICKS_NOTEBOOK_NAME_2 = "postgre_nb2"
DATABRICKS_NOTEBOOK_PATH_1 = (
    f"/Users/{DATABRICKS_LOGIN_EMAIL}/{DATABRICKS_NOTEBOOK_NAME_1}"
)
DATABRICKS_NOTEBOOK_PATH_2 = (
    f"/Users/{DATABRICKS_LOGIN_EMAIL}/{DATABRICKS_NOTEBOOK_NAME_2}"
)
DATABRICKS_JOB_CLUSTER_ID = "0926-105824-65f2g4vz"
DATABRICKS_CONN_ID = "databricks_conn"

# Define tables to extract
tables = ['customers', 'employees', 'offices', 'order_details', 'orders', 'payments', 
          'product_lines', 'products', 'warehouses']
# Define the function to query PostgreSQL
def extract_all_tables():
    conn = db.connect(
        dbname="modelcars",
        user="postgres",
        password="Kamui",
        host="192.168.0.11",
        port="5433"
    )
    
    for table in tables:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        csv_path = f'/tmp/{table}.csv'
        df.to_csv(csv_path, index=False)
        print(f"Data from {table} saved as {csv_path}")

    conn.close()

# Function to upload CSVs to Databricks File System (DBFS)
def upload_all_to_dbfs():
    for table in tables:
        local_csv_path = f'/tmp/{table}.csv'
        dbfs_csv_path = f"dbfs:/tmp/{table}.csv"
        os.system(f"databricks fs cp {local_csv_path} {dbfs_csv_path}")
        print(f"{table}.csv uploaded to DBFS")


@dag(start_date=datetime(2024, 1, 1), schedule=timedelta(minutes=5), catchup=False)
def databricks_dag():
    # Extract all tables from PostgreSQL
    extract_postgres = PythonOperator(
        task_id='extract_all_postgres_tables',
        python_callable=extract_all_tables
    )

    # Upload all CSVs to DBFS
    upload_to_dbfs = PythonOperator(
        task_id='upload_all_to_dbfs',
        python_callable=upload_all_to_dbfs
    )
    # Define the Databricks task
    spark_etl_task = DatabricksSubmitRunOperator(
        task_id='run_spark_etl',
        databricks_conn_id=DATABRICKS_CONN_ID,
        existing_cluster_id=DATABRICKS_JOB_CLUSTER_ID,
        notebook_task={
            'notebook_path': DATABRICKS_NOTEBOOK_PATH_1,  # Update this path to your Databricks notebook
        }
    )

    # Chain the tasks together
    chain(extract_postgres, upload_to_dbfs, spark_etl_task)


databricks_dag()



    # notebook_1 = DatabricksNotebookOperator(
    #     task_id="notebook1",
    #     databricks_conn_id=DATABRICKS_CONN_ID,
    #     notebook_path=DATABRICKS_NOTEBOOK_PATH_1,
    #     source="WORKSPACE",
    #     existing_cluster_id=DATABRICKS_JOB_CLUSTER_ID,  # Use the existing cluster ID
    # )

    # notebook_2 = DatabricksNotebookOperator(
    #     task_id="notebook2",
    #     databricks_conn_id=DATABRICKS_CONN_ID,
    #     notebook_path=DATABRICKS_NOTEBOOK_PATH_2,
    #     source="WORKSPACE",
    #     existing_cluster_id=DATABRICKS_JOB_CLUSTER_ID,  # Use the existing cluster ID
    # )