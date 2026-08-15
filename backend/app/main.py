from fastapi import FastAPI

from app.routes import analyze

from app.routes.issues import router as issue_router

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