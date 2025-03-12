import streamlit as st
from datetime import datetime
import requests
from add_update import add_update_tab
from analytics_by_category import analytics_by_Category_tab
from analytics_by_month import analytics_by_month_tab

# Load username/password from Streamlit secrets
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]

# Login form
st.title("Login to Access Expense Management system")
entered_user = st.text_input("Username")
entered_pass = st.text_input("Password", type="password")
login_button = st.button("Login")
login_success=False

if login_button:
    if entered_user == USERNAME and entered_pass == PASSWORD:
        st.success("Login Successful!")
        login_success=True
        st.experimental_set_query_params(auth="true")
    else:
        st.error("Invalid credentials")


if login_success:
    # API_URL="http://localhost:8000"
    API_URL = "https://expense-tracker-g6xy.onrender.com"

    st.title("Expense Management System")

    tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Month"])

    with tab1:
        add_update_tab()
    with tab2:
        analytics_by_Category_tab()
    with tab3:
        analytics_by_month_tab()




