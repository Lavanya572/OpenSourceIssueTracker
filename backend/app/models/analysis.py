from pydantic import BaseModel


class IssueAnalysisRequest(BaseModel):
    title: str
    body: str = ""
    labels: list[str] = []
    language: str | None = None


class IssueAnalysisResponse(BaseModel):
    difficulty: str
    score: int
    confidence: float
    skills: list[str]
    reason: str
    suggested_approach: list[str]