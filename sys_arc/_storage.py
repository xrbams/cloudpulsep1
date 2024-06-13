import pulumi
import pulumi_gcp as gcp

def setup_storage():
    # Create a BigQuery dataset
    dataset = gcp.bigquery.Dataset(
        'data-dataset',
        dataset_id='sports_data',
        location='US'
    )

    # Create the teams table
    teams_table = gcp.bigquery.Table(
        'teams-table',
        dataset_id=dataset.dataset_id,
        table_id='teams',
        schema="""[
            {"name": "team_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "date_of_issue", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {"name": "city", "type": "STRING", "mode": "REQUIRED"},
            {"name": "sponsor", "type": "STRING", "mode": "REQUIRED"},
            {"name": "playerId", "type": "INTEGER", "mode": "REQUIRED"}
        ]"""
    )

    # Create the players table
    players_table = gcp.bigquery.Table(
        'players-table',
        dataset_id=dataset.dataset_id,
        table_id='players',
        schema="""[
            {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "first_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "last_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "nationality", "type": "STRING", "mode": "REQUIRED"},
            {"name": "height", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "weight", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "position", "type": "STRING", "mode": "REQUIRED"}
        ]"""
    )

    pulumi.export('dataset_id', dataset.dataset_id)
    pulumi.export('teams_table', teams_table.table_id)
    pulumi.export('players_table', players_table.table_id)
