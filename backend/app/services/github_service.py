import requests

from app.config import settings
from app.models.issue import Issue
from app.exceptions import GitHubAPIError


GITHUB_SEARCH_URL = f"{settings.GITHUB_API}/search/issues"

repository_cache = {}


def map_issue(item) -> Issue:

    repository_info = get_repository_info(
        item["repository_url"]
    )

    return Issue(
        id=item["id"],
        issue_number=item["number"],
        title=item["title"],
        repository=item["repository_url"].replace(
            "https://api.github.com/repos/",
            ""
        ),

        language=repository_info["language"],

        stars=repository_info["stars"],

        forks=repository_info["forks"],

        open_issues=repository_info["open_issues"],

        labels=[
            label["name"]
            for label in item["labels"]
        ],
        url=item["html_url"],
        created_at=item["created_at"]
    )

def get_repository_info(repository_url):

    # Check cache first
    if repository_url in repository_cache:
        return repository_cache[repository_url]


    response = requests.get(
        repository_url,
        headers={
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
    )

    response.raise_for_status()

    data = response.json()

    repository_info = {
        "language": data["language"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"]
    }

    # Store result in cache
    repository_cache[repository_url] = repository_info

    return repository_info

def get_repository_language(
    owner: str,
    repo: str
):

    repository_url = (
        f"{settings.GITHUB_API}/repos/"
        f"{owner}/{repo}"
    )

    if repository_url in repository_cache:
        return repository_cache[
            repository_url
        ]["language"]

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = github_get(
        repository_url,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    repository_info = {
        "language": data.get("language"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0)
    }

    repository_cache[
        repository_url
    ] = repository_info

    return repository_info["language"]

def github_get(url, headers, params=None):

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

    except requests.RequestException:

        raise GitHubAPIError(
            "Unable to connect to GitHub.",
            503
        )

    if response.status_code == 401:

        raise GitHubAPIError(
            "GitHub authentication failed. Check your GitHub token.",
            401
        )

    if response.status_code == 403:

        raise GitHubAPIError(
            "GitHub API rate limit exceeded or access was denied.",
            429
        )

    if response.status_code == 404:

        raise GitHubAPIError(
            "GitHub resource not found.",
            404
        )

    if response.status_code >= 500:

        raise GitHubAPIError(
            "GitHub is currently unavailable.",
            502
        )

    response.raise_for_status()

    return response

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

    response = github_get(
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
        "page": page,
        "per_page": per_page,
        "total": data["total_count"],
        "issues": issues
    }

def get_issue(
    owner: str,
    repo: str,
    issue_number: int
):

    url = (
        f"{settings.GITHUB_API}/repos/"
        f"{owner}/{repo}/issues/{issue_number}"
    )

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = github_get(
        url,
        headers=headers
    )



    response.raise_for_status()

    item = response.json()

    language = get_repository_language(
        owner,
        repo
    )

    return {
        "title": item["title"],
        "body": item["body"] or "",
        "labels": [
            label["name"]
            for label in item["labels"]
        ],
        "language": None
    }

