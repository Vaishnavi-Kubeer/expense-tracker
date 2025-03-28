import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from streamlit import bar_chart
import altair as alt


#API_URL="http://localhost:8000"
API_URL="https://expense-tracker-g6xy.onrender.com"


def analytics_by_month_tab():
    # Fetch available years from FastAPI
    year_response = requests.get(f"{API_URL}/years")
    if year_response.status_code == 200:
        available_years = year_response.json()
    else:
        st.error("Failed to retrieve available years")
        available_years = [datetime.now().year]  # Default to current year

    # Year Selection Dropdown
    selected_year = st.selectbox("Select Year", available_years)

    if st.button("Get Month Analytics"):
        #response = requests.get(f"{API_URL}/analyticsByMonth")
        response = requests.get(f"{API_URL}/analyticsByMonth", params={"year": selected_year})
        if response.status_code==200:
            expense_summary= response.json()
            # st.write(expense_summary)
        else:
            st.error("Failed to retrieve expenses data")
            expense_summary=[]
        if not expense_summary:
            st.warning("No data available for selected year")

        data ={
            "Month_number":[int(c) for c in expense_summary.keys()],
            "Month_name":[expense_summary[c]['month']for c in expense_summary],
            "Total": [expense_summary[c]['total'] for c in expense_summary]
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Month_number")  # Sort numerically
        # Create Bar Chart
        chart = (
            alt.Chart(df_sorted)
            .mark_bar()
            .encode(
                x=alt.X("Month_name:N", sort=df_sorted["Month_name"].tolist()),  # Sort X-axis by Month Number
                y="Total:Q",
                tooltip=["Month_name", "Total"]
            )
        )
        st.altair_chart(chart, use_container_width=True)

        # Bar Chart: Use Month Names as Index
        # df_chart = df_sorted.set_index("Month_name")
        # st.bar_chart(df_chart["Total"])  # Month Names on X-axis

        # Table: Use Month Numbers as Index
        df_table = df_sorted.set_index("Month_number")
        df_table["Total"] = df_table["Total"].map("{:.2f}".format)
        st.table(df_table)  # Month Numbers as Index
        #

    #     df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
    #
        # st.table(df)

