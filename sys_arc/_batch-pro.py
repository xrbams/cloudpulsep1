import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery

class ParseCSV(beam.DoFn):
    def process(self, element):
        import csv
        from io import StringIO
        reader = csv.DictReader(StringIO(element))
        for row in reader:
            yield row

def run():
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        (p
         | 'Read from GCS' >> beam.io.ReadFromText('gs://YOUR_BUCKET/batch_data.csv')
         | 'Parse CSV' >> beam.ParDo(ParseCSV())
         | 'Write to BigQuery' >> WriteToBigQuery(
             'YOUR_PROJECT_ID:sports_data.players',
             schema='id:INTEGER, first_name:STRING, last_name:STRING, age:INTEGER, nationality:STRING, height:INTEGER, weight:INTEGER, position:STRING',
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
         ))

if __name__ == '__main__':
    run()
