import streamlit as st
from datetime import datetime
import requests
from add_update import add_update_tab
from analytics_by_category import analytics_by_Category_tab
from analytics_by_month import analytics_by_month_tab

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Global CSS function
def apply_custom_css():
    st.markdown(
        """
        <style>
        .stApp { background-color: #d1bc84; }
        html, body, [class*="st-"] { font-family: 'Poppins', sans-serif; }
        h1, h2, h3 { color: #FF5733; text-align: center; }
        div.stButton > button:first-child { background-color: #4CAF50; color: white; border-radius: 8px; }
        [data-testid="stSidebar"] { background-color: #EAEAEA; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply styles (ONLY ONCE in app.py)
apply_custom_css()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# If not logged in, show login form
if not st.session_state.logged_in:
    st.title("Login to Access Expense Management System")

    entered_user = st.text_input("Username")
    entered_pass = st.text_input("Password", type="password")
    login_button = st.button("Login")

    # Check credentials
    if login_button:
        if entered_user == st.secrets["USERNAME"] and entered_pass == st.secrets["PASSWORD"]:
            st.session_state.logged_in = True  # Store login state in session
            st.success("Login Successful!")
            st.rerun()  # Refresh page to show the main content
        else:
            st.error("Invalid credentials")
    st.stop()  # Prevent the rest of the app from loading until logged in

# If logged in, show the main app


API_URL = "https://expense-tracker-g6xy.onrender.com"

# tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Month"])
#
# with tab1:
#     add_update_tab()
# with tab2:
#     analytics_by_Category_tab()
# with tab3:
#     analytics_by_month_tab()

# Sidebar Navigation
with st.sidebar:
    st.title("Navigation")
    selected_tab = st.radio("Go to", ["Add/Update", "Analytics (Category)", "Analytics (Month)"])

# Main Content Based on Sidebar Selection
st.title("Expense Management System")

if selected_tab == "Add/Update":
    add_update_tab()
elif selected_tab == "Analytics (Category)":
    analytics_by_Category_tab()
elif selected_tab == "Analytics (Month)":
    analytics_by_month_tab()

# Logout Button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False  # Clear login state
    st.rerun()  # Refresh page to return to login screen



