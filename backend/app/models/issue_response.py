from pydantic import BaseModel

from app.models.issue import Issue


class IssueSearchResponse(BaseModel):
    page: int
    per_page: int
    total: int
    issues: list[Issue]