from fastapi import FastAPI

from app.routes import analyze

from app.routes.issues import router as issue_router

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import GitHubAPIError

app = FastAPI(
    title="Open Source Issue Finder",
    version="1.0.0"
)



@app.get("/")
def home():

    return {
        "message": "Welcome to Open Source Issue Finder!"
    }


app.include_router(issue_router)

app.include_router(analyze.router)

@app.exception_handler(GitHubAPIError)
async def github_api_error_handler(
    request: Request,
    exc: GitHubAPIError
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message
        }
    )