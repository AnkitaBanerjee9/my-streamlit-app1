import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt

st.set_page_config(page_title="Transaction Analyzer",
                   page_icon=":bar_chart:",
                   )

# Load Excel file
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=None)

    # Streamlit app
    st.title("Data Query and Graph Generator")

    # Select columns
    st.sidebar.header("Please Filter Here:")
    columns = st.sidebar.multiselect("Select columns to include", df.columns.tolist(), default=df.columns.tolist())

    # Select logical row names based on values in a specific column
    st.sidebar.header("Please Filter Here:")
    logical_column = st.sidebar.selectbox("Select column to filter rows", df.columns.tolist())
    row_names = df[logical_column].unique().tolist()

    st.sidebar.header("Please Filter Here:")
    selected_rows = st.sidebar.multiselect("Select rows based on logical names", row_names, default=row_names)

    # Filter dataframe based on logical row names
    filtered_df = df[df[logical_column].isin(selected_rows)][columns]

    # Display filtered dataframe without index
    st.write("Filtered Dataframe")
    st.dataframe(filtered_df)

    
    st.title(":bar_chart:  Transaction Analysis")
    st.bar_chart(filtered_df.set_index('TransactionName'), stack=False) 


