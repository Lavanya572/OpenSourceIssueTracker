from app.models.analysis import (
    IssueAnalysisRequest,
    IssueAnalysisResponse
)


BEGINNER_KEYWORDS = {
    "documentation": -2,
    "docs": -2,
    "readme": -2,
    "typo": -2,
    "example": -1,
    "comment": -1,
    "formatting": -1,
    "rename": -1
}


INTERMEDIATE_KEYWORDS = {
    "bug": 1,
    "refactor": 2,
    "api": 1,
    "database": 2,
    "authentication": 2,
    "testing": 1,
    "performance": 2
}


ADVANCED_KEYWORDS = {
    "architecture": 4,
    "concurrency": 4,
    "security": 3,
    "compiler": 4,
    "kernel": 4,
    "distributed": 4,
    "memory management": 4
}

SKILL_KEYWORDS = {
    "Python": ["python"],
    "C++": ["c++", "cpp"],
    "C": [" c ", "c programming"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "reactjs"],
    "Node.js": ["node.js", "nodejs", "node"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "Flask": ["flask"],
    "SQL": ["sql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "Docker": ["docker", "container"],
    "AWS": ["aws", "amazon web services"],
    "Git": ["git", "github"],
    "REST API": ["rest api", "restful api", "api"],
    "HTML": ["html"],
    "CSS": ["css"],
}

def detect_skills(text: str) -> list[str]:

    text = text.lower()

    detected_skills = []

    for skill, keywords in SKILL_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                detected_skills.append(skill)

                break

    return detected_skills


def analyze_issue(
    issue: IssueAnalysisRequest
) -> IssueAnalysisResponse:

    score = 0

    labels = [
        label.lower()
        for label in issue.labels
    ]

    text = (
        issue.title + " " + issue.body
    ).lower()

    skills = detect_skills(text)

    if issue.language and issue.language not in skills:
        skills.insert(0, issue.language)

    score = 0

    # -----------------------------
    # Label-based scoring
    # -----------------------------

    if "good first issue" in labels:
        score -= 3

    if "beginner" in labels:
        score -= 3

    if "help wanted" in labels:
        score -= 1

    if "security" in labels:
        score += 3

    # -----------------------------
    # Beginner keywords
    # -----------------------------

    for keyword, value in BEGINNER_KEYWORDS.items():

        if keyword in text:
            score += value

    # -----------------------------
    # Intermediate keywords
    # -----------------------------

    for keyword, value in INTERMEDIATE_KEYWORDS.items():

        if keyword in text:
            score += value

    # -----------------------------
    # Advanced keywords
    # -----------------------------

    for keyword, value in ADVANCED_KEYWORDS.items():

        if keyword in text:
            score += value

    # -----------------------------
    # Determine difficulty
    # -----------------------------

    if score <= -2:

        difficulty = "Beginner"

    elif score <= 3:

        difficulty = "Intermediate"

    else:

        difficulty = "Advanced"

    # -----------------------------
    # Confidence
    # -----------------------------

    confidence = min(
        0.95,
        0.50 + abs(score) * 0.05
    )

    return IssueAnalysisResponse(
        difficulty=difficulty,
        score=score,
        confidence=round(confidence, 2),
        skills=skills,
        reason=f"Difficulty score: {score}",
        suggested_approach=[
            "Read the issue description carefully",
            "Find the relevant code",
            "Implement the required change",
            "Run the existing tests"
        ]
    )