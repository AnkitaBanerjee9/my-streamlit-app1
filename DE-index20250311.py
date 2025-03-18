import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt

st.set_page_config(page_title="Transaction Analyzer",
                   page_icon=":bar_chart:",
                   )

def generate_report():
    print("Hello!")

# Load Excel file
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=None)

    # Streamlit app
    st.title("Data Query and Graph Generator")

    # Select columns
    #st.sidebar.header("Please Filter Here:")
    #columns = st.sidebar.multiselect("Select columns to include", df.columns.tolist(), default=df.columns.tolist())

    # Select logical row names based on values in a specific column
    #st.sidebar.header("Please Filter Here:")
    #logical_column = st.sidebar.selectbox("Select column to filter rows", df.columns.tolist())
    #row_names = df[logical_column].unique().tolist()

    #st.sidebar.header("Please Filter Here:")
    #selected_rows = st.sidebar.multiselect("Select rows based on logical names", row_names, default=row_names)

     #Filter dataframe based on logical row names
    #filtered_df = df[df[logical_column].isin(selected_rows)][columns]

    # Display filtered dataframe without index
    #st.write("Filtered Dataframe")
    #st.dataframe(filtered_df)
    with st.expander("View DataFrame"):
        st.dataframe(df)

    # Get the list of columns
    columns = df.columns.tolist()

    # Select column to filter
    #st.sidebar.header("Please Filter Here:")
    #column_to_filter = st.sidebar.selectbox("Select column to filter", columns)
    column_to_filter = st.selectbox("Select column to filter", columns)

    # Get unique values in the selected column
    unique_values = df[column_to_filter].unique()

    # Select value to filter by
    #st.sidebar.header("Please Filter Here:")
    #filter_value = st.sidebar.selectbox("Select value to filter by", unique_values)
    filter_value = st.selectbox("Select value to filter by", unique_values)

    # Filter the DataFrame
    filtered_df = df[df[column_to_filter] == filter_value]

    # Display the filtered DataFrame
    #st.write("### Filtered Data")
    #st.dataframe(filtered_df)
    with st.expander("View Filetred DataFrame"):
        st.dataframe(filtered_df)

    del filtered_df['Status']

    st.sidebar.header("Please Filter Here:")
    selected_columns = st.sidebar.multiselect("Select columns to include", filtered_df.columns.tolist(), default=filtered_df.columns.tolist())

    if selected_columns:
        filtered_df1 = filtered_df[selected_columns]
    st.write("Filtered Table:")
    st.dataframe(filtered_df1)
    st.title(":bar_chart:  Transaction Analysis")
    if st.button('Generate Report'):
        #print("Hello")
        generate_report() 
    st.bar_chart(filtered_df1.set_index('TransactionName'), stack=False) 
else:
    st.write("")







    
        
  

