import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

#https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Transaction Analyzer",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

 
# Title of the app
st.title("Performance Load Test Report Analysis")
                 

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file:
   # st.markdown('---')
    dataset = pd.read_excel(
    uploaded_file,
    engine='openpyxl'   
    )
    st.dataframe(dataset)
   # st.sidebar.header("Please Filter Here:")
    st.write('### Summary Statistics')
    
    # Identify transactions that have breached the SLA
# Assuming the first column is 'TransactionName' and the second column is 'SLA'
  

    num_rows, num_columns = dataset.shape

    # Display the results
    st.write(f"Number of rows: {num_rows}")
    st.write(f"Number of columns: {num_columns}")

    #st.write('### Transactions that have breached the SLA')
    

    st.sidebar.header("Please Filter Here:")
    transactioNames = st.sidebar.multiselect(
    "Select Transaction Names",
    options=dataset["TransactionName"].unique(),
    default=dataset["TransactionName"].unique()
    )

    selected_columns = st.sidebar.multiselect(
    "Select Columns", dataset.columns.tolist(), default=dataset.columns.tolist())
    
    dataset_selection = dataset.query(
    "TransactionName == @transactioNames"
    )

    


    
    st.title(":bar_chart:  Transaction Analysis")
    st.bar_chart(dataset_selection.set_index('TransactionName'), stack=False)  








    


  
    




 




