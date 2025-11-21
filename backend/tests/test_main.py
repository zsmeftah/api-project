from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.database import Base, get_db
from backend.app.main import app
from backend.app.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_login_and_get_token():
    response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

def test_read_users_me():
    token = test_login_and_get_token()
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_create_indicator_as_admin():
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "testuser@example.com").first()
    user.role = "admin"
    db.commit()
    db.close()

    token = test_login_and_get_token()
    
    response = client.post(
        "/zones/",
        json={"name": "TestZone", "postal_code": "00000"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    zone_id = response.json()["id"]

    indicator_data = {
        "type": "temperature",
        "source": "Test",
        "value": 25.5,
        "unit": "C",
        "zone_id": zone_id,
        "timestamp": "2025-01-01T12:00:00"
    }
    response = client.post(
        "/indicators/",
        json=indicator_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["value"] == 25.5

def test_read_indicators_with_filter():
    token = test_login_and_get_token()
    response = client.get(
        "/indicators/?type=temperature",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_stats_average():
    token = test_login_and_get_token()
    response = client.get(
        "/stats/average?zone_id=1&type=temperature",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "labels" in data
    assert "series" in data
    assert data["series"][0] == 25.5