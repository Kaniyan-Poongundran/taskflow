from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn CI/CD",
            "description": "Learn GitHub Actions",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Learn CI/CD"
    assert data["description"] == "Learn GitHub Actions"
    assert data["completed"] is False


def test_get_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Docker",
            "description": "Learn Docker",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Docker"


def test_get_nonexistent_task():
    response = client.get("/tasks/999999")

    assert response.status_code == 404