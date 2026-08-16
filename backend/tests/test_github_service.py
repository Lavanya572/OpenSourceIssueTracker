from app.services.github_service import search_issues


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