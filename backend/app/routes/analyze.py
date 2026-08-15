from fastapi import APIRouter

from app.models.analysis import (
    IssueAnalysisRequest,
    IssueAnalysisResponse
)

from app.services.analyzer_service import analyze_issue


router = APIRouter()


@router.post(
    "/issues/analyze",
    response_model=IssueAnalysisResponse
)
def analyze_issue_endpoint(
    issue: IssueAnalysisRequest
):

    return analyze_issue(issue)