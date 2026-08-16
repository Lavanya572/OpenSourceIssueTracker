from typing import Optional
from fastapi import APIRouter

from app.services.github_service import search_issues
from app.models.issue_response import IssueSearchResponse
from fastapi import APIRouter, Query

router = APIRouter()


@router.get(
    "/issues",
    response_model=IssueSearchResponse,
    summary="Search beginner-friendly GitHub issues",
    description=(
        "Search GitHub issues using language, label, "
        "state and pagination filters."
    )
)
def fetch_issues(
    language: str | None = Query(
        default=None,
        min_length=1
    ),

    label: str | None = Query(
        default=None,
        min_length=1
    ),

    state: str = Query(
        default="open",
        pattern="^(open|closed)$"
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    per_page: int = Query(
        default=10,
        ge=1,
        le=100
    )
):

    return search_issues(
        language,
        label,
        state,
        page,
        per_page
    )