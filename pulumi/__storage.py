import pulumi
from pulumi_gcp import storage
import os

bucket_name = "raw_data_sources"  # Change this to your desired bucket name
bucket_location = "us-east1"  # Change to your preferred GCP region
sqlite_file_path = "../data/raw/data.sqlite"  # Path to your local SQLite database

def create_storage_bucket():
    # Create a new GCP storage bucket
    bucket = storage.Bucket(
        bucket_name,
        location=bucket_location,
        force_destroy=True  # If you want to allow auto-deletion of bucket
    )
    return bucket


def send_sqlite_data(bucket):
    # Ensure the SQLite file exists before uploading
    if not os.path.isfile(sqlite_file_path):
        raise FileNotFoundError(f"SQLite file '{sqlite_file_path}' not found.")
    
    # Upload the SQLite file to the bucket
    bucket_object = storage.BucketObject(
        "sqlite-database-upload",  # Name of the object in the bucket
        bucket=bucket.name,  # Reference the bucket created above
        source=pulumi.FileAsset(sqlite_file_path)  # Use FileAsset to upload the file
    )

    # Export the name of the bucket and the file that was uploaded
    pulumi.export("bucket_name", bucket.name)
    pulumi.export("uploaded_file", bucket_object.name)

def create_transformed_folder(bucket):
    # Create an empty "transformed" folder in the bucket
    storage.BucketObject(
        "transformed/", 
        bucket=bucket.name,
        content="This is a sample text file in the transformed folder."
    )

def create_big_query_bucket():
    # Create an empty "transformed" folder in the bucket
    bucket = storage.Bucket(
        "big_query_temp",
        location=bucket_location,
        force_destroy=True  # If you want to allow auto-deletion of bucket
    )
    return bucket