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


def test_filter_tickets_by_project() -> None:
    project_a = create_test_project()
    project_b = create_test_project()

    client.post(
        "/tickets",
        json={
            "title": "Ticket A",
            "project_id": project_a["id"],
        },
    )

    client.post(
        "/tickets",
        json={
            "title": "Ticket B",
            "project_id": project_b["id"],
        },
    )

    response = client.get(
        f"/tickets?project_id={project_a['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert all(
        ticket["project_id"] == project_a["id"]
        for ticket in data
    )