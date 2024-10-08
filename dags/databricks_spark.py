"""
### Run notebooks in databricks as a Databricks Workflow using the Airflow Databricks provider

This DAG runs two Databricks notebooks as a Databricks workflow.
"""
from airflow.decorators import dag 
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksNotebookOperator, DatabricksSubmitRunOperator
from airflow.providers.databricks.operators.databricks_workflow import (
    DatabricksWorkflowTaskGroup,
)
from airflow.models.baseoperator import chain
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils.dates import days_ago
from pendulum import datetime
from datetime import timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
import pandas as pd 
import psycopg2 as db
import sqlite3 as sql
import base64
import requests
from airflow.hooks.base_hook import BaseHook

# Define constants for Databricks and GCS
DATABRICKS_LOGIN_EMAIL = "bmsakamali@gmail.com"
DATABRICKS_NOTEBOOK_NAME_1 = "postgre_nb"
DATABRICKS_NOTEBOOK_NAME_2 = "postgre_nb2"
DATABRICKS_NOTEBOOK_PATH_1 = f"/Users/{DATABRICKS_LOGIN_EMAIL}/{DATABRICKS_NOTEBOOK_NAME_1}"
DATABRICKS_NOTEBOOK_PATH_2 = f"/Users/{DATABRICKS_LOGIN_EMAIL}/{DATABRICKS_NOTEBOOK_NAME_2}"
DATABRICKS_JOB_CLUSTER_ID = "1008-100905-j1csvnee"

GCS_BUCKET_NAME = "raw_data_sources-2c76fed" 
GCS_SQLITE_FILE = "sqlite-database-upload-9572c98"
# "gs://raw_data_sources-2c76fed/sqlite-database-upload-9572c98" 
LOCAL_SQLITE_FILE = "/tmp/data.sqlite"
TABLES = ['customers', 'employees', 'offices', 'orderdetails', 'orders', 'payments', 
          'productlines', 'products', 'warehouses']
#ETL-Cluster-V1

GCS_PROCESSED_FOLDER = "transformed"

DATABRICKS_CONN_ID = "databricks_conn"
GCP_CONN_ID = "GCP_CONN"
DB_CONN_ID = "db_conn"

# Function to download SQLite database from GCS
def download_sqlite_file():
    pass  # Handled by GCSDownloadFileOperator

# Function to extract tables from the SQLite file
def extract_all_tables():
    conn = sql.connect(LOCAL_SQLITE_FILE)
    for table in TABLES:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        csv_path = f'/tmp/{table}.csv'
        df.to_csv(csv_path, index=False)
        print(f"Data from {table} saved as {csv_path}")
    conn.close()

# Function to upload CSVs to Databricks File System (DBFS)
def upload_csv_to_dbfs(csv_file_path, dbfs_path):
    """Upload a CSV file to Databricks File System."""
    databricks_conn = BaseHook.get_connection('databricks_conn')
    DATABRICKS_INSTANCE = databricks_conn.host
    DATABRICKS_TOKEN = "dapif5217f364e50250c317e25b7571df5b7"

    
    # Check if the local CSV file exists
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'rb') as f:
            # Read the file content and base64 encode it
            file_content = f.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')

            # Create the DBFS API call to upload the file in parts
            response = requests.post(
                f"{DATABRICKS_INSTANCE}/api/2.0/dbfs/put",
                headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"},
                json={
                    'path': dbfs_path,
                    'overwrite': True,
                    'contents': encoded_content  # Send the base64-encoded content
                }
            )

        if response.status_code == 200:
            print(f"{csv_file_path} uploaded to DBFS successfully.")
        else:
            print(f"Error uploading {csv_file_path}: {response.text}")
    else:
        print(f"Error: {csv_file_path} does not exist.")

def upload_and_run_notebook(**kwargs):
    for table in TABLES:
        local_csv_path = f'/tmp/{table}.csv'  # Local path to the CSV file
        dbfs_path = f'dbfs:/tmp/{table}.csv'    # DBFS path to upload the file
        upload_csv_to_dbfs(local_csv_path, dbfs_path)  # Upload CSV file

        # Prepare parameters for the Databricks notebook
        base_parameters = {
            "file_path": dbfs_path,
            "table_name": table,
        }

        # Create a task to trigger the Databricks notebook
        run_task = DatabricksSubmitRunOperator(
            task_id=f'run_notebook_{table}',
            existing_cluster_id=DATABRICKS_JOB_CLUSTER_ID,  # Replace with your cluster ID
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_task={
                'notebook_path': DATABRICKS_NOTEBOOK_PATH_2,  # Update with your notebook path
                'base_parameters': base_parameters,
            },
            dag=kwargs['dag']
        )

        # Set task dependencies dynamically
        if 'previous_task' in kwargs:
            previous_task = kwargs['previous_task']
            previous_task >> run_task
        kwargs['previous_task'] = run_task  # Update the previous task for the next iteration

# Function to upload processed CSVs back to GCS
def upload_processed_to_gcs(**kwargs):
    for table in TABLES:
        upload_task = LocalFilesystemToGCSOperator(
            task_id=f"upload_{table}_to_gcs",
            src=f"/tmp/{table}.csv",  # Local CSV file path
            dst=f"{GCS_PROCESSED_FOLDER}/{table}.csv",  # GCS destination
            bucket=GCS_BUCKET_NAME,  # GCS bucket name
            gcp_conn_id=GCP_CONN_ID,  # GCP connection ID
        )
        # Execute the upload task for each file
        upload_task.execute(context=kwargs)
    

# Define the payload for running a notebook
notebook_task_params_1 = {
    "existing_cluster_id": DATABRICKS_JOB_CLUSTER_ID,
    "notebook_task": {
        "notebook_path": DATABRICKS_NOTEBOOK_PATH_1
    }
}
notebook_task_params_2 = {
    "existing_cluster_id": DATABRICKS_JOB_CLUSTER_ID,
    "notebook_task": {
        "notebook_path": DATABRICKS_NOTEBOOK_PATH_2
    }
}


with DAG(
    dag_id='databricks_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval=timedelta(minutes=15),
    catchup=False
) as dag:

    # Task to download the SQLite file from GCS
    download_sqlite_task = GCSToLocalFilesystemOperator(
        task_id="download_sqlite_file",
        bucket=GCS_BUCKET_NAME,
        object_name=GCS_SQLITE_FILE,
        filename=LOCAL_SQLITE_FILE,
        gcp_conn_id=GCP_CONN_ID,
    )

    # Task to extract tables from the SQLite file
    extract_tables_task = PythonOperator(
        task_id='extract_all_tables',
        python_callable=extract_all_tables,
        dag=dag
    )

    # Task to upload extracted CSVs to Databricks File System (DBFS)
    upload_to_dbfs_task = PythonOperator(
        task_id='upload_and_run_notebook',
        python_callable=upload_and_run_notebook,
        provide_context=True,
        dag=dag
    )

    # Task to run the first Databricks notebook
    run_notebook_1 = DatabricksSubmitRunOperator(
        task_id="run_notebook_1",
        databricks_conn_id=DATABRICKS_CONN_ID,
        json=notebook_task_params_1,
        dag=dag
    )

    # Task to run the second Databricks notebook
    run_notebook_2 = DatabricksSubmitRunOperator(
        task_id="run_notebook_2",
        databricks_conn_id=DATABRICKS_CONN_ID,
        json=notebook_task_params_2,
        dag=dag
    )

    # Task to upload processed CSVs back to GCS
    upload_processed_task = PythonOperator(
        task_id='upload_processed_to_gcs',
        python_callable=upload_processed_to_gcs,
        provide_context=True,
        dag=dag
    )

    # Chain the tasks together
    chain(download_sqlite_task, extract_tables_task, upload_to_dbfs_task, run_notebook_1, run_notebook_2, upload_processed_task)


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

    # export DATABRICKS_HOST="https://4025938785050141.1.gcp.databricks.com/"
    # export DATABRICKS_TOKEN="dapif5217f364e50250c317e25b7571df5b7"

    