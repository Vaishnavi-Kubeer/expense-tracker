import streamlit as st
import pandas as pd

st.header("This is Header")
st.subheader("In subheader")
st.text("I am Vaishnavi Kubeer")
st.write("Here is simple tables")

df=pd.DataFrame({
    "Name":['Infosys','Infy'],
    "Employee":["Vaishu","Anvesh"]
})
st.table(df)
st.table({
"date":['2024-08-21','2024-09-06'],"Name":['Vaishu','Vaishali']
})

st.line_chart([10,20,20,30,40,50,52])

age = st.slider("Select age",0,100)
st.write(f"selected age : {age}")

st.checkbox("Show/Hide")

st.selectbox("Select",[1,2,3,4],label_visibility="collapsed")
option=st.selectbox("Category",['Rent','Food','Shopping'],label_visibility="collapsed")
st.write(f"selected category: {option}")
o=st.multiselect("Select mulitple",[1,2,3,4,5,6])
st.write(f"selected category: {o}")