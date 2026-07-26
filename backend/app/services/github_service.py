import requests

from app.config import settings
from app.models.issue import Issue


GITHUB_SEARCH_URL = f"{settings.GITHUB_API}/search/issues"


def map_issue(item) -> Issue:
    return Issue(
        title=item["title"],
        repository=item["repository_url"].replace(
            "https://api.github.com/repos/",
            ""
        ),
        labels=[
            label["name"]
            for label in item["labels"]
        ],
        url=item["html_url"],
        created_at=item["created_at"]
    )

def get_beginner_issues():

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "q": 'is:issue is:open label:"good first issue"',
        "sort": "created",
        "order": "desc",
        "per_page": 10
    }

    response = requests.get(
        GITHUB_SEARCH_URL,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    print(response.status_code)

    print(response.json())

    issues = [map_issue(item) for item in data["items"]]
    return issues