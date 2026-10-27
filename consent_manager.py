
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CONSENT_PATH = DATA_DIR / "consent.csv"

COLUMNS = [
    "candidate_id",
    "share_learning_progress",
    "share_joining_status",
]


def load_consent():
    if CONSENT_PATH.exists():
        return pd.read_csv(CONSENT_PATH)

    return pd.DataFrame(columns=COLUMNS)


def get_candidate_consent(candidate_id):
    consent = load_consent()
    rows = consent[
        consent["candidate_id"].astype(str) == str(candidate_id)
    ]

    if rows.empty:
        return {
            "share_learning_progress": False,
            "share_joining_status": False,
        }

    row = rows.iloc[0]
    return {
        "share_learning_progress": (
            str(row["share_learning_progress"]).lower()
            in ["true", "1"]
        ),
        "share_joining_status": (
            str(row["share_joining_status"]).lower()
            in ["true", "1"]
        ),
    }


def save_candidate_consent(
    candidate_id,
    share_learning_progress,
    share_joining_status,
):
    consent = load_consent()

    consent = consent[
        consent["candidate_id"].astype(str) != str(candidate_id)
    ]

    new_row = pd.DataFrame([{
        "candidate_id": str(candidate_id),
        "share_learning_progress": share_learning_progress,
        "share_joining_status": share_joining_status,
    }])

    consent = pd.concat([consent, new_row], ignore_index=True)
    DATA_DIR.mkdir(exist_ok=True)
    consent.to_csv(CONSENT_PATH, index=False)
