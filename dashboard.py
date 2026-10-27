
import streamlit as st

st.set_page_config(
    page_title="JoinTrack",
    page_icon="🎯",
    layout="wide",
)

overview = st.Page(
    "app.py",
    title="Overview",
    icon="📊",
    default=True,
)

candidates = st.Page(
    "pages/candidates.py",
    title="Candidates",
    icon="👥",
)

learning = st.Page(
    "pages/learning.py",
    title="Learning Plans",
    icon="📚",
)

followups = st.Page(
    "pages/followups.py",
    title="Follow-ups",
    icon="🤝",
)

consent = st.Page(
    "pages/consent.py",
    title="Student Consent",
    icon="🔐",
)

employer = st.Page(
    "pages/employer.py",
    title="Employer Portal",
    icon="🏢",
)

college = st.Page(
    "pages/college.py",
    title="College Portal",
    icon="🎓",
)

navigation = st.navigation({
    "JoinTrack": [
        overview,
        candidates,
        learning,
        followups,
        consent,
        employer,
        college,
    ]
})


navigation.run()
