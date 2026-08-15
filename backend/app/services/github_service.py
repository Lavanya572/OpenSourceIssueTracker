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

def search_issues(
    language=None,
    label=None,
    state="open",
    page=1,
    per_page=10
):

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    query = ["is:issue"]

    if state:
        query.append(f"is:{state}")

    if language:
        query.append(f"language:{language}")

    if label:
        query.append(f'label:"{label}"')

    search_query = " ".join(query)

    params = {
        "q": search_query,
        "sort": "created",
        "order": "desc",
        "page": page,
        "per_page": per_page
    }

    response = requests.get(
        GITHUB_SEARCH_URL,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    issues = [
        map_issue(item)
        for item in data["items"]
    ]

    return {
        "total_count": data["total_count"],
        "page": page,
        "per_page": per_page,
        "issues": issues
    }

