import pulumi
import pulumi_gcp as gcp

def setup_storage():
    # Create a Cloud Storage bucket
    bucket = gcp.storage.Bucket(
        'my-bucket',
        location='US'
    )

    # Export the bucket name
    pulumi.export('bucket_name', bucket.name)
