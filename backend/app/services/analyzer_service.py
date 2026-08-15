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

def generate_reason(
    issue: IssueAnalysisRequest,
    difficulty: str,
    score: int
) -> str:

    labels = [
        label.lower()
        for label in issue.labels
    ]

    text = (
        issue.title + " " + issue.body
    ).lower()

    reasons = []

    if "good first issue" in labels:
        reasons.append(
            "The issue is marked as a good first issue."
        )

    if "beginner" in labels:
        reasons.append(
            "The issue has a beginner-related label."
        )

    if "documentation" in text or "docs" in text:
        reasons.append(
            "The issue appears to involve documentation."
        )

    if "bug" in labels or "bug" in text:
        reasons.append(
            "The issue involves fixing a bug."
        )

    if "refactor" in text:
        reasons.append(
            "The issue involves changing or restructuring existing code."
        )

    if "security" in labels or "security" in text:
        reasons.append(
            "The issue involves security-related functionality."
        )

    if not reasons:
        reasons.append(
            "The difficulty was estimated using the issue's "
            "labels and technical keywords."
        )

    return " ".join(reasons) + f" Difficulty score: {score}."

def generate_approach(
    issue: IssueAnalysisRequest,
    skills: list[str]
) -> list[str]:

    labels = [
        label.lower()
        for label in issue.labels
    ]

    text = (
        issue.title + " " + issue.body
    ).lower()

    steps = []

    # Documentation issues
    if (
        "documentation" in text
        or "docs" in text
        or "readme" in text
    ):
        steps = [
            "Read the issue description carefully",
            "Open the documentation or README mentioned in the issue",
            "Locate the incorrect or missing information",
            "Make the required documentation change",
            "Review the changes for accuracy",
            "Submit a pull request"
        ]

        return steps

    # Bug issues
    if "bug" in labels or "bug" in text:

        steps = [
            "Read the issue description and reproduction steps",
            "Reproduce the problem locally",
            "Find the relevant code",
            "Identify the root cause",
            "Implement the fix",
            "Run the existing tests",
            "Submit a pull request"
        ]

        return steps

    # Refactoring
    if "refactor" in text:

        steps = [
            "Understand the existing implementation",
            "Identify the code that needs restructuring",
            "Plan the refactoring carefully",
            "Make the changes without changing expected behavior",
            "Run the existing tests",
            "Review the changes",
            "Submit a pull request"
        ]

        return steps

    # Security
    if (
        "security" in labels
        or "security" in text
    ):

        steps = [
            "Read the issue carefully",
            "Understand the affected security component",
            "Reproduce the reported behavior if possible",
            "Identify the security weakness",
            "Implement the fix carefully",
            "Add or update security tests",
            "Run the complete test suite",
            "Submit a pull request"
        ]

        return steps

    # Default
    return [
        "Read the issue description carefully",
        "Understand the expected behavior",
        "Find the relevant code",
        "Implement the required change",
        "Run the existing tests",
        "Review the changes",
        "Submit a pull request"
    ]

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

    reason = generate_reason(
        issue,
        difficulty,
        score
    )

    suggested_approach = generate_approach(
        issue,
        skills
    )

    return IssueAnalysisResponse(
        difficulty=difficulty,
        score=score,
        confidence=round(confidence, 2),
        skills=skills,
        reason=reason,
        suggested_approach=suggested_approach
    )