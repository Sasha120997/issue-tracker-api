from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_project() -> None:
    response = client.post(
        "/projects",
        json={
            "name": "Test project",
            "description": "Testing",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test project"
    assert data["description"] == "Testing"
    assert "id" in data

def test_create_project_without_name_fails() -> None:
    response = client.post(
        "/projects",
        json={
            "name": "",
            "description": "Testing"
        },
    )

    assert response.status_code == 422