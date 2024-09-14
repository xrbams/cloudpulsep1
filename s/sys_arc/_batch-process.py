import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions

import pulumi
import pulumi_gcp as gcp
def batch():

    project_ID = "smart-charter-422809-k0"
    bucket_name = "data-bucket-9858dba"
    player_topic_name = "player-updates-1de6ac7"

    # Define pipeline options
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = project_ID
    google_cloud_options.job_name = 'batch-job'
    google_cloud_options.staging_location = 'gs://{bucket_name}/staging'
    google_cloud_options.temp_location = 'gs://{bucket_name}/temp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'

    # Define the pipeline
    with beam.Pipeline(options=options) as p:
        (p
        | 'ReadData' >> beam.io.ReadFromText('gs://{bucket_name}/input/*.txt')
        | 'ParseCSV' >> beam.Map(lambda line: line.split(','))
        | 'ProcessData' >> beam.Map(lambda fields: {'name': fields[0], 'count': int(fields[1])})
        | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
            table='{project_ID}:sports_data.players',
            schema='SCHEMA_AUTODETECT',
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        ))
    
    batch_dataflow_job = gcp.dataflow.Job(
        'batch-job',
        template_gcs_path=None,
        on_delete='cancel',
        parameters={},
        environment={'stagingLocation': f'gs://{bucket_name}/staging'}
    )



#  table='{project_ID}:sports_data.players',