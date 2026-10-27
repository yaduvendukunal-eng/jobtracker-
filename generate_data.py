
from pathlib import Path
import random
import pandas as pd

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

roles = [
    "Java Developer",
    "Python Developer",
    "Data Analyst",
    "Web Developer",
    "Software Engineer",
]

records = []

for i in range(1, 201):
    days_until_joining = random.randint(-15, 90)
    days_since_activity = random.randint(0, 40)
    unanswered_confirmations = random.randint(0, 3)
    joining_date_deferred = random.choice([0, 0, 0, 1])
    student_reported_uncertainty = random.choice([0, 0, 0, 1])

    # Synthetic demo outcomes only—not validated predictions.
    risk = (
        0.10
        + 0.25 * (days_since_activity >= 21)
        + 0.30 * (unanswered_confirmations >= 2)
        + 0.10 * joining_date_deferred
        + 0.15 * student_reported_uncertainty
    )

    if days_until_joining > 0:
        outcome = "Pending"
    else:
        outcome = (
            "Did Not Join"
            if random.random() < min(risk, 0.90)
            else "Joined"
        )

    records.append({
        "candidate_id": f"CAND{i:03d}",
        "role": random.choice(roles),
        "days_until_joining": days_until_joining,
        "days_since_learning_activity": days_since_activity,
        "unanswered_confirmations": unanswered_confirmations,
        "joining_date_deferred": joining_date_deferred,
        "student_reported_uncertainty": student_reported_uncertainty,
        "outcome": outcome,
    })

df = pd.DataFrame(records)
output_path = DATA_DIR / "candidates.csv"
df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print(f"Total candidates: {len(df)}")
print(df["outcome"].value_counts())
print(f"\nSaved to: {output_path}")
