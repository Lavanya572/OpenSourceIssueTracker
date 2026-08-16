from app.models.analysis import IssueAnalysisRequest
from app.services.analyzer_service import analyze_issue


def test_good_first_issue_is_beginner():

    issue = IssueAnalysisRequest(
        title="Fix README typo",
        body="Correct a typo in the documentation.",
        labels=["good first issue", "documentation"],
        language="Python"
    )

    result = analyze_issue(issue)

    assert result.difficulty == "Beginner"
    assert result.score < 0

def test_python_skill_is_detected():

    issue = IssueAnalysisRequest(
        title="Fix Python API bug",
        body="The REST API is failing.",
        labels=["bug"],
        language="Python"
    )

    result = analyze_issue(issue)

    assert "Python" in result.skills
    assert "REST API" in result.skills

def test_advanced_issue():

    issue = IssueAnalysisRequest(
        title="Fix concurrency issue",
        body=(
            "The distributed system has a memory management "
            "problem."
        ),
        labels=["security"],
        language="C++"
    )

    result = analyze_issue(issue)

    assert result.difficulty == "Advanced"

def test_bug_has_debugging_steps():

    issue = IssueAnalysisRequest(
        title="Fix API bug",
        body="The API returns an incorrect response.",
        labels=["bug"],
        language="Python"
    )

    result = analyze_issue(issue)

    assert "Reproduce the problem locally" in result.suggested_approach
    assert "Identify the root cause" in result.suggested_approach