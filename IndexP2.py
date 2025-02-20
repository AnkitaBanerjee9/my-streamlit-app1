import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the page
st.set_page_config(page_title="Performance Report Comparison", layout="wide")
st.title("Performance Report Analysis")

# Sidebar: File upload
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
    # -----------------------------
    # Section 1: Report Preview Filters
    # -----------------------------
    st.header("Report Preview & Filtering")
    st.write("Use the filters below to select specific rows and columns from the report preview.")
    
    # Filter: Select columns to display in the preview table
    preview_columns = st.sidebar.multiselect("Select columns for preview", df.columns.tolist(), default=df.columns.tolist())
    
    # Filter: Select rows based on a logical column
    logical_column = st.sidebar.selectbox("Select column for row filtering", df.columns.tolist())
    unique_vals = df[logical_column].dropna().unique().tolist()
    selected_vals = st.sidebar.multiselect("Select row values to display", unique_vals, default=unique_vals)
    
    # Filtered preview dataframe based on selected columns and rows
    preview_df = df[df[logical_column].isin(selected_vals)][preview_columns]
    
    st.dataframe(preview_df)
    
    # -----------------------------
    # Section 2: Transaction Analysis Chart
    # -----------------------------
    st.title(":bar_chart: Transaction Analysis")
    if 'TransactionName' in preview_df.columns:
        st.bar_chart(preview_df.set_index('TransactionName'))
    else:
        st.error("The column 'TransactionName' is required for the Transaction Analysis chart.")
    
    # -----------------------------
    # Section 3: Response Time Comparison
    # -----------------------------
    st.header("Response Time Comparison: Run1 vs Run2")
    #st.subheader("Full Report Preview")
    #st.write(df.head())
    
    # Required columns check
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
        
        # -----------------------------
        # Section 4: Graphical Comparison with Additional Filter
        # -----------------------------
        st.subheader("Graphical Comparison by Transaction")
        st.write("Use the filter below to narrow the transactions displayed in the graph.")
        
        # Additional filter for graphical comparison:
        # Option 1: Filter by TransactionName (multiselect)
        transaction_options = df['TransactionName'].dropna().unique().tolist()
        selected_transactions = st.multiselect("Select transactions to display in graph", transaction_options, default=transaction_options)
        
        # Option 2: Filter by response time range for Run1 (you can also add for Run2 if needed)
        min_rt = float(df['Run1-90Percent'].min())
        max_rt = float(df['Run1-90Percent'].max())
        rt_range = st.slider("Select Run1 response time range", min_rt, max_rt, (min_rt, max_rt))
        rt_range = st.slider("Select Run2 response time range", min_rt, max_rt, (min_rt, max_rt))
        rt_range = st.slider("Select Run3 response time range", min_rt, max_rt, (min_rt, max_rt))
        
        # Filter the dataframe for plotting based on the above filters
        df_graph = df[
            (df['TransactionName'].isin(selected_transactions)) &
            (df['Run1-90Percent'] >= rt_range[0]) &
            (df['Run1-90Percent'] <= rt_range[1])
        ]
        
        # Reshape data for plotting comparison between Run1 and Run2
        df_plot = df_graph[['TransactionName', 'Run1-90Percent', 'Run2-90Percent','Run3-90Percent']].melt(
            id_vars='TransactionName',
            value_vars=['Run1-90Percent', 'Run2-90Percent','Run3-90Percent'],
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
