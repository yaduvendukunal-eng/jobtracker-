
import streamlit as st


def show_navigation():
    st.sidebar.divider()

    st.sidebar.subheader(
        f"Logged in: {st.session_state.get('user_role', 'Guest')}"
    )

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.switch_page("pages/home.py")

    if st.sidebar.button("🚪 Log out", use_container_width=True):
        for key in ["logged_in", "user_role", "account_id"]:
            st.session_state.pop(key, None)

        st.switch_page("login.py")

