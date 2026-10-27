
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "risk_results.csv"

st.title("🎯 JoinTrack")
st.caption("Pre-joining engagement and explainable risk monitoring")

if not DATA_PATH.exists():
    st.error("Risk results not found. Run generate_data.py and risk_engine.py first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

a, b, c, d = st.columns(4)
a.metric("Total candidates", len(df))
b.metric("High risk", int((df["risk_level"] == "High").sum()))
c.metric("Medium risk", int((df["risk_level"] == "Medium").sum()))
d.metric("Joined", int((df["outcome"] == "Joined").sum()))

st.subheader("Risk distribution")
counts = (
    df["risk_level"]
    .value_counts()
    .reindex(["High", "Medium", "Low"], fill_value=0)
    .rename_axis("Risk level")
    .reset_index(name="Candidates")
)
st.bar_chart(counts, x="Risk level", y="Candidates")

st.subheader("Candidates requiring review")
high_risk = df[df["risk_level"] == "High"]

if high_risk.empty:
    st.success("No candidates currently have a high rule-based risk score.")
else:
    st.dataframe(
        high_risk[
            ["candidate_id", "role", "risk_score", "risk_reasons"]
        ],
        use_container_width=True,
        hide_index=True,
    )

st.info(
    "Demo uses synthetic data and rule-based flags. "
    "Scores are not validated predictions of joining behavior."
)
