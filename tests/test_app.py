import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test if the homepage loads successfully."""
    response = client.get('/')
    assert response.status_code == 200

def test_todos_endpoint(client):
    """Test if the /todos endpoint loads successfully."""
    response = client.get('/todos')
    assert response.status_code == 200
