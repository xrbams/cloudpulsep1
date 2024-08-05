import sys
import os
import pytest

# Add the main project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from server import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_drivers(client):
#     res = client.get('/api/drivers')
#     assert res.status_code == 200
#     data = res.get_json()
#     assert isinstance(data, list)
#     assert 'Driver' in data[0]
#     assert 'Team' in data[0]
#     assert 'LapTime' in data[0]
