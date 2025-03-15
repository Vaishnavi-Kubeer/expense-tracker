import streamlit as st
from datetime import datetime
import requests

#API_URL="http://localhost:8000"
API_URL="https://expense-tracker-g6xy.onrender.com"


def add_update_tab():
    selected_date= st.date_input("Enter Date",datetime.today().date(),label_visibility="collapsed")
    response=requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code==200:
        existing_expenses= response.json()
        #st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses data")
        existing_expenses=[]

    categories=["Rent","Food","Shopping","Entertainment","Groceries","Travelling","Vacation","Other"]
    expenses_data = []

    def update_total():
        st.session_state.total_amount = sum(
            st.session_state.get(f"amount_{i}", 0.0) for i in range(7)
        )

    # Initialize session state total amount if not set
    if "total_amount" not in st.session_state:
        st.session_state.total_amount = 0.0

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")
        for i in range(7):
            if i<len(existing_expenses):
                amount=existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount=0.0
                category="Food"
                notes=""

            col1,col2,col3=st.columns(3)
            with col1:
                amount_input=st.number_input(label="Amount",min_value=0.0,step=1.0,value=amount,on_change=update_total(), key=f"amount_{i}",label_visibility="collapsed")
            with col2:
                category_input=st.selectbox(label="Category",options=categories,index=categories.index(category) ,key=f"category_{i}",label_visibility="collapsed")
            with col3:
                notes_input=st.text_input(label="",value=notes,key=f"notes_{i}",label_visibility="collapsed")

            expenses_data.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })
        st.markdown(f"💰 Total Amount Spent: INR{st.session_state.total_amount:.2f}")
        submit_button=st.form_submit_button()
        if submit_button:
            # Filter out empty expenses where amount is 0 and notes are empty
            filtered_expenses = [e for e in expenses_data if e["amount"] > 0 or e["notes"].strip()]
            response=requests.post(f"{API_URL}/expenses/{selected_date}",json=filtered_expenses)
            if response.status_code==200:
                st.success("Expenses added/updated successfully")
                # Reset session state values
                st.session_state.expense_data = [{"amount": 0.0, "category": "Food", "notes": ""} for _ in range(7)]

                # Rerun the script to refresh inputs
                st.rerun()
            else:
                st.success("Failed to add/update")