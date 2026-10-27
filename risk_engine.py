
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "candidates.csv"
OUTPUT_PATH = BASE_DIR / "data" / "risk_results.csv"


def calculate_risk(row):
    score = 0
    reasons = []

    if row["days_since_learning_activity"] >= 21:
        score += 30
        reasons.append("No learning activity for 3 weeks")

    if row["unanswered_confirmations"] >= 2:
        score += 35
        reasons.append("Two or more unanswered confirmations")

    if 0 <= row["days_until_joining"] <= 14:
        score += 20
        reasons.append("Joining date is within 14 days")

    if row["student_reported_uncertainty"] == 1:
        score += 15
        reasons.append("Student reported uncertainty")

    if row["joining_date_deferred"] == 1:
        score += 10
        reasons.append("Joining date was deferred")

    if score >= 50:
        level = "High"
    elif score >= 25:
        level = "Medium"
    else:
        level = "Low"

    return pd.Series({
        "risk_score": score,
        "risk_level": level,
        "risk_reasons": "; ".join(reasons)
        if reasons else "No configured risk signals",
    })



def recommend_action(row):
    """Recommend a follow-up based on the candidate's risk factors."""
    actions = []

    try:
        inactive_days = int(row.get("days_since_learning_activity", 0) or 0)
    except (ValueError, TypeError):
        inactive_days = 0

    try:
        unanswered = int(row.get("unanswered_confirmations", 0) or 0)
    except (ValueError, TypeError):
        unanswered = 0

    try:
        days_until_joining = int(row.get("days_until_joining", 999) or 0)
    except (ValueError, TypeError):
        days_until_joining = 999

    uncertain = str(
        row.get("student_reported_uncertainty", 0)
    ).strip().lower() in {"1", "1.0", "true", "yes"}

    deferred = str(
        row.get("joining_date_deferred", 0)
    ).strip().lower() in {"1", "1.0", "true", "yes"}

    if inactive_days >= 21:
        actions.append(
            "Contact the candidate and offer help restarting their learning plan."
        )

    if unanswered >= 2:
        actions.append(
            "Follow up on unanswered confirmations and ask whether support is needed."
        )

    if 0 <= days_until_joining <= 14:
        actions.append(
            "Confirm joining arrangements and check that required documents are ready."
        )

    if uncertain:
        actions.append(
            "Arrange a supportive check-in to understand the candidate's concerns."
        )

    if deferred:
        actions.append(
            "Confirm the revised joining date and update the follow-up schedule."
        )

    if not actions:
        actions.append(
            "Continue routine check-ins and monitor for changes."
        )

    return actions



def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. "
            "Run generate_data.py first."
        )

    df = pd.read_csv(DATA_PATH)
    results = df.apply(calculate_risk, axis=1)
    df = pd.concat([df, results], axis=1)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Risk analysis completed!")
    print("\nRisk-level counts:")
    print(df["risk_level"].value_counts())

    print("\nSample results:")
    print(df[[
        "candidate_id",
        "role",
        "risk_score",
        "risk_level",
        "risk_reasons",
    ]].head(10).to_string(index=False))

    print(f"\nSaved results to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
