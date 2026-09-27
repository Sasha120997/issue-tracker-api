from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def create_test_project() -> dict:
    response = client.post(
        "/projects",
        json={
            "name": "Test project",
        },
    )

    return response.json()


def test_create_ticket() -> None:
    project = create_test_project()

    response = client.post(
        "/tickets",
        json={
            "title": "Fix bug",
            "description": "Something broke",
            "project_id": project["id"],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Fix bug"
    assert data["project_id"] == project["id"]
    assert data["status"] == "open"
    assert "id" in data