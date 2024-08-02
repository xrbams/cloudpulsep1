import json
import functions_framework
from google.cloud import bigquery

# Define the schema for validation
SCHEMA = [
    {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "first_name", "type": "STRING", "mode": "REQUIRED"},
    {"name": "last_name", "type": "STRING", "mode": "REQUIRED"},
    {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "nationality", "type": "STRING", "mode": "REQUIRED"},
    {"name": "height", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "weight", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "position", "type": "STRING", "mode": "REQUIRED"}
]

@functions_framework.http
def query_bigquery(request):
    client = bigquery.Client()
    path = request.path
    method = request.method
    
    if path == '/players' and method == 'GET':
        return get_all_players(client)
    elif path.startswith('/players/') and method == 'GET':
        player_id = path.split('/')[-1]
        return get_player_by_id(client, player_id)
    elif path == '/players' and method == 'POST':
        try:
            player_data = request.get_json()
        except Exception as e:
            return (f'Invalid JSON data: {e}', 400)
        return add_player(client, player_data)
    else:
        return ('Not Found', 404)

def get_all_players(client):
    try:
        query = 'SELECT * FROM `sports_data.player_views`'
        query_job = client.query(query)
        results = query_job.result()
        players = [dict(row) for row in results]
        return (json.dumps(players), 200, {'Content-Type': 'application/json'})
    except Exception as e:
        return (f'Error fetching all players: {e}', 500)

def get_player_by_id(client, player_id):
    try:
        query = 'SELECT * FROM `sports_data.player_views` WHERE id = @player_id'
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("player_id", "INTEGER", player_id)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        players = [dict(row) for row in results]
        if players:
            return (json.dumps(players[0]), 200, {'Content-Type': 'application/json'})
        else:
            return ('Player not found', 404)
    except Exception as e:
        return (f'Error fetching player by ID: {e}', 500)

def add_player(client, player_data):
    try:
        # Validate player data against the schema
        if not validate_player_data(player_data):
            return ('Invalid player data', 400)
        
        table_id = 'sports_data.player_views'
        errors = client.insert_rows_json(table_id, [player_data])
        if errors == []:
            return ('Player is inserted ...', 200)
        else:
            return (f'Failed to insert player: {errors}', 400)
    except Exception as e:
        return (f'Error adding player: {e}', 500)

def validate_player_data(player_data):
    for field in SCHEMA:
        field_name = field["name"]
        field_type = field["type"]
        field_mode = field["mode"]

        if field_name not in player_data:
            return False

        value = player_data[field_name]
        
        if field_mode == "REQUIRED" and value is None:
            return False
        
        if field_type == "INTEGER":
            if not isinstance(value, int):
                return False
        elif field_type == "STRING":
            if not isinstance(value, str):
                return False

    return True