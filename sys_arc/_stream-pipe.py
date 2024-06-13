import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
from apache_beam.io.gcp.pubsub import ReadFromPubSub

class ParseMessage(beam.DoFn):
    def process(self, message):
        import json
        record = json.loads(message)
        return [record]

def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as p:
        (p
         | 'Read from Pub/Sub' >> ReadFromPubSub(subscription='projects/YOUR_PROJECT_ID/subscriptions/player-updates-sub')
         | 'Parse JSON messages' >> beam.ParDo(ParseMessage())
         | 'Write to BigQuery' >> WriteToBigQuery(
             'YOUR_PROJECT_ID:sports_data.players',
             schema='id:INTEGER, first_name:STRING, last_name:STRING, age:INTEGER, nationality:STRING, height:INTEGER, weight:INTEGER, position:STRING',
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
         ))

if __name__ == '__main__':
    run()
