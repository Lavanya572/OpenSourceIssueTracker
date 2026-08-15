from pydantic import BaseModel

class Issue(BaseModel):
    id: int
    issue_number: int
    title: str
    repository: str
    language: str | None
    stars: int
    forks: int
    open_issues: int
    labels: list[str]
    url: str
    created_at: str



'''Issue blueprint - check in postman api for all the model headings'''