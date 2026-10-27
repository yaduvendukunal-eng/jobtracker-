
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

TRACKER_PATH = DATA_DIR / "candidate_tracker.csv"

STATUSES = [
    "Offer Accepted",
    "Preparing",
    "Joining Confirmed",
    "Concern Raised",
    "Joined",
    "Did Not Join",
]


def load_tracker():
    if TRACKER_PATH.exists():
        return pd.read_csv(TRACKER_PATH, keep_default_na=False)

    return pd.DataFrame(columns=[
        "candidate_id",
        "status",
        "last_contact_date",
        "confirmation_response",
        "follow_up_note",
    ])


def get_candidate_tracker(candidate_ids):
    tracker = load_tracker()
    existing = set(tracker["candidate_id"].astype(str))

    new_rows = [
        {
            "candidate_id": str(candidate_id),
            "status": "Offer Accepted",
            "last_contact_date": "",
            "confirmation_response": "Not requested",
            "follow_up_note": "",
        }
        for candidate_id in candidate_ids
        if str(candidate_id) not in existing
    ]

    if new_rows:
        tracker = pd.concat(
            [tracker, pd.DataFrame(new_rows)],
            ignore_index=True,
        )
        tracker.to_csv(TRACKER_PATH, index=False)

    return tracker


def save_tracker(tracker):
    tracker.to_csv(TRACKER_PATH, index=False)
