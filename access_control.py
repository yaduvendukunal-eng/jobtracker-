
import streamlit as st

ROLE_PERMISSIONS = {
    "Student": {
        "learning",
        "consent",
    },
    "Employer": {
        "employer",
        "followups",
        "candidates",
    },
    "College Placement Officer": {
        "college",
    },
}


def require_access(page_name):
    """Require login and permission before showing a protected page."""

    if not st.session_state.get("logged_in", False):
        st.warning("Please log in to access this page.")
        st.switch_page("login.py")
        st.stop()

    role = st.session_state.get("user_role")

    if page_name not in ROLE_PERMISSIONS.get(role, set()):
        st.error("Access denied: you do not have permission to view this page.")
        st.page_link("pages/home.py", label="Return Home", icon="🏠")
        st.stop()
