from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_page():

    response = client.get(
        "/issues",
        params={
            "page": -1
        }
    )

    assert response.status_code == 422


def test_invalid_per_page():

    response = client.get(
        "/issues",
        params={
            "per_page": 101
        }
    )

    assert response.status_code == 422


def test_invalid_state():

    response = client.get(
        "/issues",
        params={
            "state": "invalid"
        }
    )

    assert response.status_code == 422