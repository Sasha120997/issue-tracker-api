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


def test_get_projects() -> None:
    response = client.get("/projects")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_project() -> None:
    create_response = client.post(
        "/projects",
        json={
            "name": "Test project",
            "description": "Test"
        },
    )

    project = create_response.json()

    response = client.get(f"/projects/{project['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Test project"

def test_get_project_404() -> None:
    create_response = client.post(
        "/projects",
        json={
            "name": "Test project",
            "description": "Test",
        },
    )

    project = create_response.json()

    response = client.get(f"/projects/{10}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_update_project() -> None:
    create_response = client.post(
        "/projects",
        json={
            "name": "Original",
            "description": "Keep this",
        },
    )

    project = create_response.json()

    response = client.patch(
        f"/projects/{project['id']}",
        json={
            "name": "Updated",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated"
    assert data["description"] == "Keep this"


def test_delete_project() -> None:
    create_response = client.post(
        "/projects",
        json={
            "name": "Delete me",
        },
    )

    project = create_response.json()

    response = client.delete(
        f"/projects/{project['id']}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/projects/{project['id']}"
    )

    assert get_response.status_code == 404