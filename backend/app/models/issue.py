from pydantic import BaseModel

class Issue(BaseModel):
    title: str
    repository: str
    labels: list[str]
    url: str
    created_at: str



'''Issue blueprint - check in postman api for all the model headings'''