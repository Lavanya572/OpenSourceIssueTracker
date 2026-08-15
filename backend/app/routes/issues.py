from typing import Optional
from fastapi import APIRouter

from app.services.github_service import search_issues

router = APIRouter()


@router.get("/issues")
def fetch_issues(
    language: Optional[str] = None,
    label: Optional[str] = None,
    state: str = "open",
    page: int = 1,
    per_page: int = 10,
):
    return search_issues(
        language,
        label,
        state,
        page,
        per_page
    )