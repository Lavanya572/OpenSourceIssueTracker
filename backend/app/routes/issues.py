from fastapi import APIRouter

from app.services.github_service import get_beginner_issues

router = APIRouter()


@router.get("/issues")
def fetch_issues():

    return get_beginner_issues()