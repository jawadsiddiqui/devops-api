import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test /health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_metrics_endpoint(client):
    """Test /metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200

def test_root_endpoint(client):
    """Test root (/) endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert "date" in data
    assert "kubernetes" in data
