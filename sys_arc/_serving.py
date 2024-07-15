import json
import functions_framework
from google.cloud import bigquery

import pulumi
import pulumi_gcp as gcp

@functions_framework.http
def query_bigquery(request):
    client = bigquery.Client()
    query = 'SELECT * FROM `sports_data.player_views` '
    query_job = client.query(query)

    results = query_job.result()

    players = []
    for row in results:
        players.append(dict(row))

    return (json.dumps(players), 200, {'Content-Type': 'application/json'})

# # Define the Cloud Function source code directory
# source_directory = './function_source'

# # Create a bucket object for the Cloud Function source
# bucket_object = gcp.storage.BucketObject(
#     'function-source',
#     bucket=bucket.name,
#     source=pulumi.AssetArchive({
#         '.': pulumi.FileArchive(source_directory)
#     })
# )

# # Create the Cloud Function
# function = gcp.cloudfunctions.Function(
#     'query-function',
#     entry_point='query_bigquery',
#     runtime='python39',
#     source_archive_bucket=bucket.name,
#     source_archive_object=bucket_object.name,
#     trigger_http=True,
#     available_memory_mb=256,
#     environment_variables={
#         'DATASET_ID': 'player_dataset',
#         'TABLE_ID': 'player'
#     }
# )

# # Output the function URL
# pulumi.export('function_url', function.https_trigger_url)