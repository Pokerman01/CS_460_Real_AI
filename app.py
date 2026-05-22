import streamlit as st

import dashboard
import landing
import login
import register
from database import init_db


init_db()

st.set_page_config(
    page_title="Smart Receipt & Tax Organizer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def init_router_state():
    defaults = {
        "page": "landing",
        "is_authenticated": False,
        "is_guest": False,
        "user_id": None,
        "username": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_router_state()

if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]

if st.session_state.page == "dashboard":
    if not st.session_state.is_authenticated and not st.session_state.is_guest:
        st.session_state.page = "login"
        login.show_page()
    else:
        dashboard.show_page()

elif st.session_state.page == "login":
    login.show_page()

elif st.session_state.page == "register":
    register.show_page()

else:
    landing.show_page()