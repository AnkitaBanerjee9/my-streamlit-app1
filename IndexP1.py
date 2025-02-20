import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the page
st.set_page_config(page_title="Performance Report Comparison", layout="wide")
st.title("Performance Report Analysis")

# Sidebar for file upload
st.sidebar.header("Upload Test Report")
uploaded_file = st.sidebar.file_uploader("Upload the report file", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    return None

# Load data from the uploaded file
df = load_data(uploaded_file)

if df is not None:
    # Data Filtering Section
    st.title("Data Query and Graph Generator")
    
    # Sidebar: Select columns to include
    st.sidebar.header("Please Filter Here:")
    selected_columns = st.sidebar.multiselect("Select columns to include", df.columns.tolist(), default=df.columns.tolist())

    # Sidebar: Select logical row names based on values in a specific column
    logical_column = st.sidebar.selectbox("Select column to filter rows", df.columns.tolist())
    row_names = df[logical_column].unique().tolist()
    selected_rows = st.sidebar.multiselect("Select rows based on logical names", row_names, default=row_names)

    # Filter dataframe based on selected rows and columns
    filtered_df = df[df[logical_column].isin(selected_rows)][selected_columns]

    # Display filtered dataframe
    st.write("Filtered Dataframe")
    st.dataframe(filtered_df)

    # Transaction Analysis Bar Chart
    st.title(":bar_chart: Transaction Analysis")
    # Setting TransactionName as index for a simple bar chart
    if 'TransactionName' in filtered_df.columns:
        st.bar_chart(filtered_df.set_index('TransactionName'))
    else:
        st.error("The column 'TransactionName' is required for the Transaction Analysis chart.")

    # Report Preview and Response Time Comparison Section
    st.header("Report Preview")
    st.write(df.head())

    # Required columns for response time comparison
    required_cols = ['TransactionName', 'SLA', 'Run1-90Percent', 'Run2-90Percent', 'Run3-90Percent']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"The following required columns are missing: {missing}")
    else:
        # Calculate average response times for Run1 and Run2
        st.subheader("Average Response Time Comparison")
        avg_run1 = df['Run1-90Percent'].mean()
        avg_run2 = df['Run2-90Percent'].mean()
        
        st.write(f"**Run1-90Percent Average Response Time:** {avg_run1:.2f}")
        st.write(f"**Run2-90Percent Average Response Time:** {avg_run2:.2f}")
        
        if avg_run1 < avg_run2:
            st.success("Run1-90Percent has the best (lowest) response times overall.")
        elif avg_run1 > avg_run2:
            st.success("Run2-90Percent has the best (lowest) response times overall.")
        else:
            st.info("Both runs have similar response times.")

        # Graphical Comparison by Transaction
        st.subheader("Graphical Comparison by Transaction")
        # Reshape the DataFrame for plotting a grouped bar chart
        df_plot = df[['TransactionName', 'Run1-90Percent', 'Run2-90Percent']].melt(
            id_vars='TransactionName',
            value_vars=['Run1-90Percent', 'Run2-90Percent'],
            var_name='Run',
            value_name='Response Time'
        )
        
        fig = px.bar(
            df_plot, 
            x='TransactionName', 
            y='Response Time', 
            color='Run', 
            barmode='group',
            title="Response Time Comparison per Transaction"
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload a report file to begin the analysis.")
