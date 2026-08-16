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

def test_github_api_error_handler():

    from fastapi.testclient import TestClient
    from app.main import app
    from app.exceptions import GitHubAPIError

    @app.get("/test-github-error")
    def test_error():
        raise GitHubAPIError(
            "GitHub resource not found.",
            404
        )

    client = TestClient(app)

    response = client.get("/test-github-error")

    assert response.status_code == 404

    assert response.json() == {
        "error": "GitHub API error",
        "message": "GitHub resource not found."
    }