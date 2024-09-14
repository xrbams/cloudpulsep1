import pymysql
import pytest

# Database connection settings
DB_CONFIG = {
    'host': 'your_database_host',
    'user': 'your_database_user',
    'password': 'your_database_password',
    'database': 'your_database_name',
    'port': 3306
}

@pytest.fixture
def db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    yield connection
    connection.close()

def test_player_exists(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM players WHERE id = 1")
        result = cursor.fetchone()
        assert result[0] == 1

def test_team_name(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM teams WHERE name = 'TeamName'")
        result = cursor.fetchone()
        assert result[0] == 1
