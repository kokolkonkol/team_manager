import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_page(client):
    """Test root page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Team Manager" in response.text

def test_employees_list(client):
    """Test employees listing"""
    response = client.get("/employees")
    assert response.status_code == 200
    assert "Employees List" in response.text

def test_surveys_list(client):
    """Test surveys listing"""
    response = client.get("/surveys")
    assert response.status_code == 200
    assert "Surveys" in response.text