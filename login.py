
import streamlit as st

st.set_page_config(
    page_title="JoinTrack Login",
    page_icon="🎯",
    layout="centered",
)

st.set_option("client.showSidebarNavigation", False)

st.title("🎯 JoinTrack")
st.subheader("Pre-Joining Management System")
st.write("Choose your role to enter your dashboard.")

role = st.selectbox(
    "Login as",
    ["Student", "Employer", "College Placement Officer"],
)

if role == "Student":
    account_id = st.selectbox(
        "Select demo student",
        ["CAND001", "CAND002", "CAND003"],
    )
else:
    account_id = st.text_input(
        "Demo account name",
        value="demo_user",
    )

if st.button("Continue", type="primary", use_container_width=True):
    if account_id.strip():
        st.session_state["user_role"] = role
        st.session_state["account_id"] = account_id
        st.session_state["logged_in"] = True
        st.switch_page("pages/home.py")
    else:
        st.error("Please enter an account name.")

st.caption(
    "Hackathon demo login only. No password verification or "
    "real authentication is implemented."
)
