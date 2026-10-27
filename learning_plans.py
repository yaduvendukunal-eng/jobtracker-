
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

PLAN_PATH = DATA_DIR / "learning_progress.csv"

ROLE_TASKS = {
    "Java Developer": [
        ("Java fundamentals", "Revise OOP, collections, and exceptions", 3),
        ("SQL basics", "Practice SELECT, JOIN, and GROUP BY", 3),
        ("Git and GitHub", "Create a repository and practice branching", 2),
        ("Mini project", "Build a small Java CRUD application", 5),
    ],
    "Python Developer": [
        ("Python fundamentals", "Revise functions, collections, and exceptions", 3),
        ("APIs", "Build a small REST API", 4),
        ("Testing", "Write unit tests for core functions", 2),
        ("Mini project", "Build a small Python application", 5),
    ],
    "Data Analyst": [
        ("Excel", "Practice formulas, sorting, and pivot tables", 3),
        ("SQL", "Practice filtering, joins, and aggregations", 4),
        ("Data visualization", "Create charts from a sample dataset", 3),
        ("Mini project", "Analyze a dataset and summarize findings", 4),
    ],
    "Web Developer": [
        ("HTML and CSS", "Build a responsive page", 3),
        ("JavaScript", "Practice DOM and event handling", 4),
        ("Git and GitHub", "Practice commits and branches", 2),
        ("Mini project", "Build a small interactive website", 5),
    ],
    "Software Engineer": [
        ("Programming fundamentals", "Practice data structures and algorithms", 4),
        ("Git and GitHub", "Practice commits, branches, and pull requests", 2),
        ("Testing", "Write tests for a small program", 3),
        ("Mini project", "Build and document a small application", 5),
    ],
}


def load_progress():
    if PLAN_PATH.exists():
        return pd.read_csv(PLAN_PATH)

    return pd.DataFrame(columns=[
        "candidate_id", "role", "task",
        "description", "estimated_days", "completed"
    ])


def ensure_candidate_plan(candidate_id, role):
    progress = load_progress()

    existing = progress[
        progress["candidate_id"] == candidate_id
    ]

    if not existing.empty:
        return progress

    tasks = ROLE_TASKS.get(
        role,
        ROLE_TASKS["Software Engineer"]
    )

    new_rows = [{
        "candidate_id": candidate_id,
        "role": role,
        "task": task,
        "description": description,
        "estimated_days": days,
        "completed": False,
    } for task, description, days in tasks]

    progress = pd.concat(
        [progress, pd.DataFrame(new_rows)],
        ignore_index=True,
    )

    progress.to_csv(PLAN_PATH, index=False)
    return progress


def save_progress(progress):
    progress.to_csv(PLAN_PATH, index=False)
