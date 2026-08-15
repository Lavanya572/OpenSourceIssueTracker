from fastapi import APIRouter, HTTPException

from app.services.github_service import get_issue
from app.services.analyzer_service import analyze_issue
from app.models.analysis import IssueAnalysisResponse

from app.models.analysis import (
    IssueAnalysisRequest,
    IssueAnalysisResponse
)


router = APIRouter()




@router.post(
    "/issues/analyze/{owner}/{repo}/{issue_number}",
    response_model=IssueAnalysisResponse
)
def analyze_github_issue(
    owner: str,
    repo: str,
    issue_number: int
):

    issue = get_issue(
        owner,
        repo,
        issue_number
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    request = IssueAnalysisRequest(
        title=issue["title"],
        body=issue["body"],
        labels=issue["labels"],
        language=issue["language"]
    )

    return analyze_issue(request)