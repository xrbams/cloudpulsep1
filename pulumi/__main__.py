"""A Python Pulumi program"""
import pulumi
from pulumi_gcp import storage
from __storage import create_storage_bucket, send_sqlite_data, create_transformed_folder, create_big_query_bucket
from __bigquery import create_warehouse
from __iam_conn import generate_IAM


# generate_IAM()
bucket = create_storage_bucket()

send_sqlite_data(bucket)
create_transformed_folder(bucket)
bg_bucket = create_big_query_bucket()

