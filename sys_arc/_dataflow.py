import pulumi
import pulumi_gcp as gcp


# Step 1: Data Ingestion
# Create a Pub/Sub topic
topic = gcp.pubsub.Topic('player-updates')

# Create a Cloud Storage bucket for batch data
bucket = gcp.storage.Bucket('data-bucket')


# Step 2: Batch Processing
# Create a Dataflow job for batch processing (simplified example, replace with actual job details)
batch_dataflow_job = gcp.dataflow.Job(
    'batch-job',
    template_gcs_path="gs://dataflow-templates/latest/Word_Count",
    parameters={
        'inputFile': f'gs://{bucket.name}/input/*.txt',
        'output': f'gs://{bucket.name}/output/'
    },
    region=pulumi.Config('gcp').require('region')
)

# Step 3: Real-Time Processing
# Create a Dataflow job for real-time processing (simplified example, replace with actual job details)
stream_dataflow_job = gcp.dataflow.Job(
    'stream-job',
    template_gcs_path="gs://dataflow-templates/latest/Stream_Demo",
    parameters={
        'inputSubscription': topic.id,
        'outputTable': 'project:dataset.table'
    },
    region=pulumi.Config('gcp').require('region')
)

# Step 4: Data Storage
# Create a BigQuery dataset
dataset = gcp.bigquery.Dataset('data-dataset', dataset_id='my_dataset')

# Create a BigQuery table (simplified schema)
table = gcp.bigquery.Table(
    'data-table',
    dataset_id=dataset.dataset_id,
    table_id='my_table',
    schema='[{"name": "word", "type": "STRING", "mode": "REQUIRED"}, {"name": "count", "type": "INTEGER", "mode": "REQUIRED"}]'
)

# Step 5: Serving Layer
# Create a Cloud Function to query BigQuery (simplified example)
function = gcp.cloudfunctions.Function(
    'query-function',
    entry_point='query_bigquery',
    runtime='python39',
    source_archive_bucket=bucket.name,
    source_archive_object='function-source.zip',
    trigger_http=True,
    available_memory_mb=256,
    environment_variables={
        'DATASET_ID': dataset.dataset_id,
        'TABLE_ID': table.table_id
    }
)

# Define the Cloud Function code (simplified example, replace with actual code)
pulumi.Output.all(bucket.name, function.source_archive_object).apply(lambda args: (
    f"""
    import base64
    import google.cloud.bigquery as bigquery

    def query_bigquery(request):
        client = bigquery.Client()
        dataset_id = '{args[0]}'
        table_id = '{args[1]}'
        query = f'SELECT * FROM `{{dataset_id}}.{{table_id}}` LIMIT 10'
        query_job = client.query(query)
        results = query_job.result()
        return [row for row in results]
    """
)).apply(lambda function_code: open('function_source/query_bigquery.py', 'w').write(function_code))

# Deploy the Cloud Function
bucket_object = gcp.storage.BucketObject(
    'function-source',
    bucket=bucket.name,
    source=pulumi.AssetArchive({
        '.': pulumi.FileArchive('./function_source')
    })
)

pulumi.export('bucket_name', bucket.name)
pulumi.export('topic_name', topic.name)
pulumi.export('dataset_id', dataset.dataset_id)
pulumi.export('table_id', table.table_id)
pulumi.export('function_url', function.https_trigger_url)