import streamlit as st
from datetime import datetime
import requests

import pandas as pd
from streamlit import bar_chart


#API_URL="http://localhost:8000"
API_URL="https://expense-tracker-g6xy.onrender.com"


def analytics_by_Category_tab():
    col1,col2=st.columns(2)
    with col1:
        start_date = st.date_input("start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("end Date", datetime(2024, 8, 5))
    if st.button("Get Analytics"):
        payload={
            "start_date":start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics/",json=payload)
        if response.status_code==200:
            expense_summary= response.json()
            #st.write(expense_summary)
        else:
            st.error("Failed to retrieve expenses data")
            expense_summary=[]
        data ={
            "Category":list(expense_summary.keys()),
            "Total":[expense_summary[c]['total']for c in expense_summary],
            "Percentage": [expense_summary[c]['percentage'] for c in expense_summary]
        }
        df=pd.DataFrame(data)
        df_sorted=df.sort_values(by="Percentage",ascending=False)

        st,bar_chart(df_sorted.set_index("Category")["Percentage"])

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        st.table(df_sorted)

