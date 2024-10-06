"""A Python Pulumi program"""
import pulumi
from pulumi_gcp import storage
from __storage import create_storage_bucket, send_sqlite_data, create_transformed_folder
from __iam_conn import generate_IAM


# generate_IAM()
bucket = create_storage_bucket()
send_sqlite_data(bucket)
create_transformed_folder(bucket)

