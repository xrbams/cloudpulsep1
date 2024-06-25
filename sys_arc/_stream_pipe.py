import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
from apache_beam.io.gcp.pubsub import ReadFromPubSub
from apache_beam.io.gcp.bigquery import WriteToBigQuery

import pulumi
import pulumi_gcp as gcp

class ParseMessage(beam.DoFn):
    def process(self, message):
        record = json.loads(message)
        return [record]

#pubsub: player-updates-1de6ac7
#subscription: player-updates-sub-ea61560
def run():

    project_id = 'smart-charter-422809-k0'
    region = 'us-west1'
    bucket_name = 'data-bucket-9858dba'
    subs = "player-updates-sub-ea61560"
    # staging_bucket = pulumi.Output.from_input('data_bucket_name').apply(lambda x: x)
    # temp_bucket = pulumi.Output.from_input('temp_bucket_name').apply(lambda x: x)

    # Define your pipeline options
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = project_id
    google_cloud_options.region = region
    google_cloud_options.staging_location = f'gs://{bucket_name}/staging'
    google_cloud_options.temp_location = f'gs://{bucket_name}/temp'
    options.view_as(StandardOptions).runner = 'DirectRunner'
    options.view_as(StandardOptions).streaming = True

     # Define the schema for BigQuery table
    schema = {
        'fields': [
            {'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'first_name', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'last_name', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'age', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'nationality', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'height', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'weight', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'position', 'type': 'STRING', 'mode': 'REQUIRED'}
        ]
    }


    # Define the pipeline
    with beam.Pipeline(options=options) as p:
        (p
         | 'Read from Pub/Sub' >> ReadFromPubSub(subscription=f'projects/{project_id}/subscriptions/{subs}')
         | 'Parse JSON' >> beam.Map(lambda msg: json.loads(msg.decode('utf-8')))
         | 'Validate and Process Data' >> beam.Map(lambda data: {
             'id': int(data.get('id', 0)),
             'first_name': data.get('first_name', ''),
             'last_name': data.get('last_name', ''),
             'age': int(data.get('age', 0)),
             'nationality': data.get('nationality', ''),
             'height': int(data.get('height', 0)),
             'weight': int(data.get('weight', 0)),
             'position': data.get('position', '')
         })
         | 'Write to BigQuery' >> WriteToBigQuery(
             table=f'{project_id}:sports_data.players',
             schema=schema,
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
         ))
    
    stream_dataflow_job = gcp.dataflow.Job(
        'stream-job',
        template_gcs_path=None,
        on_delete='cancel',
        parameters={},
        environment={'stagingLocation': f'gs://{bucket_name}/staging'}
    )

run()
# if __name__ == '__main__':
#     run()
#     print("Stream Job Running.....")
