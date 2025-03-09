import streamlit as st
from datetime import datetime
import requests
from add_update import add_update_tab
from analytics_by_category import analytics_by_Category_tab
from analytics_by_month import analytics_by_month_tab

API_URL="http://localhost:8000"

st.title("Expense Management System")

tab1,tab2,tab3=st.tabs(["Add/Update","Analytics By Category","Analytics By Month"])

with tab1:
    add_update_tab()
with tab2:
    analytics_by_Category_tab()
with tab3:
    analytics_by_month_tab()



