import pytest
import requests
from app.services.github_service import search_issues
from app.exceptions import GitHubAPIError
from app.services.github_service import github_get


def test_search_issues(mocker):

    fake_github_response = {
        "total_count": 1,
        "items": [
            {
                "id": 123,
                "number": 10,
                "title": "Fix README typo",
                "repository_url": (
                    "https://api.github.com/repos/"
                    "test/demo"
                ),
                "labels": [
                    {
                        "name": "good first issue"
                    }
                ],
                "html_url": (
                    "https://github.com/"
                    "test/demo/issues/10"
                ),
                "created_at": (
                    "2026-08-16T10:00:00Z"
                )
            }
        ]
    }

    mock_response = mocker.Mock()

    mock_response.json.return_value = (
        fake_github_response
    )

    mock_response.status_code = 200

    mocker.patch(
        "app.services.github_service.github_get",
        return_value=mock_response
    )

    mocker.patch(
        "app.services.github_service.get_repository_info",
        return_value={
            "language": "Python",
            "stars": 10,
            "forks": 2,
            "open_issues": 5
        }
    )

    result = search_issues(
        language="Python",
        label="good first issue",
        state="open",
        page=1,
        per_page=10
    )

    assert result["total"] == 1
    assert result["page"] == 1
    assert result["per_page"] == 10

    assert len(result["issues"]) == 1

    issue = result["issues"][0]

    assert issue.title == "Fix README typo"
    assert issue.repository == "test/demo"
    assert issue.language == "Python"
    assert issue.stars == 10
    assert issue.forks == 2
    assert issue.open_issues == 5
    assert "good first issue" in issue.labels

def test_repository_cache(mocker):

    from app.services.github_service import (
        get_repository_info,
        repository_cache
    )

    repository = "test/demo"

    fake_repository = {
        "language": "Python",
        "stars": 10,
        "forks": 2,
        "open_issues": 5
    }

    repository_cache.clear()

    mock_response = mocker.Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "language": "Python",
        "stargazers_count": 10,
        "forks_count": 2,
        "open_issues_count": 5
    }

    mock_get = mocker.patch(
        "app.services.github_service.requests.get",
        return_value=mock_response
    )

    result1 = get_repository_info(repository)

    result2 = get_repository_info(repository)

    assert result1 == fake_repository
    assert result2 == fake_repository

    assert mock_get.call_count == 1

def test_github_404(mocker):

    mock_response = mocker.Mock()

    mock_response.status_code = 404
    mock_response.ok = False

    mocker.patch(
        "app.services.github_service.requests.get",
        return_value=mock_response
    )

    with pytest.raises(GitHubAPIError) as error:

        github_get(
            "https://api.github.com/test",
            headers={}
        )

    assert error.value.status_code == 404
    assert error.value.message == (
        "GitHub resource not found."
    )

def test_github_401(mocker):

    mock_response = mocker.Mock()

    mock_response.status_code = 401
    mock_response.ok = False

    mocker.patch(
        "app.services.github_service.requests.get",
        return_value=mock_response
    )

    with pytest.raises(GitHubAPIError) as error:

        github_get(
            "https://api.github.com/test",
            headers={}
        )

    assert error.value.status_code == 401

def test_github_403(mocker):

    mock_response = mocker.Mock()

    mock_response.status_code = 403
    mock_response.ok = False

    mocker.patch(
        "app.services.github_service.requests.get",
        return_value=mock_response
    )

    with pytest.raises(GitHubAPIError) as error:

        github_get(
            "https://api.github.com/test",
            headers={}
        )

    assert error.value.status_code == 429

def test_github_500(mocker):

    mock_response = mocker.Mock()

    mock_response.status_code = 500
    mock_response.ok = False

    mocker.patch(
        "app.services.github_service.requests.get",
        return_value=mock_response
    )

    with pytest.raises(GitHubAPIError) as error:

        github_get(
            "https://api.github.com/test",
            headers={}
        )

    assert error.value.status_code == 502

def test_github_connection_error(mocker):

    mocker.patch(
        "app.services.github_service.requests.get",
        side_effect=requests.RequestException()
    )

    with pytest.raises(GitHubAPIError) as error:

        github_get(
            "https://api.github.com/test",
            headers={}
        )

    assert error.value.status_code == 503
    assert error.value.message == (
        "Unable to connect to GitHub."
    )