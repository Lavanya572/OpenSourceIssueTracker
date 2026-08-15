from app.models.analysis import (
    IssueAnalysisRequest,
    IssueAnalysisResponse
)


def analyze_issue(
    issue: IssueAnalysisRequest
) -> IssueAnalysisResponse:

    difficulty = "Intermediate"
    confidence = 0.50

    labels = [
        label.lower()
        for label in issue.labels
    ]

    if "good first issue" in labels:
        difficulty = "Beginner"
        confidence = 0.85

    elif "beginner" in labels:
        difficulty = "Beginner"
        confidence = 0.80

    elif "help wanted" in labels:
        difficulty = "Intermediate"
        confidence = 0.65

    elif "security" in labels:
        difficulty = "Advanced"
        confidence = 0.80

    return IssueAnalysisResponse(
        difficulty=difficulty,
        confidence=confidence,
        skills=[],
        reason="Difficulty was estimated using issue labels.",
        suggested_approach=[
            "Read the issue description carefully",
            "Find the relevant code",
            "Implement the required change",
            "Run the existing tests"
        ]
    )