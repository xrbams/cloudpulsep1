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
