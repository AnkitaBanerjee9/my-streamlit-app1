import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configure the page
st.set_page_config(page_title="Performance Load Test Dashboard", layout="wide")

# Title of the app
st.title("Performance Load Test Report Analysis")

# Sidebar instructions and file upload
st.sidebar.header("Upload Test Reports")
file_run1 = st.sidebar.file_uploader("Upload Test Report for Run 1", type=["csv", "xlsx"])
file_run2 = st.sidebar.file_uploader("Upload Test Report for Run 2 (Optional)", type=["csv", "xlsx"])

# Function to load data into a DataFrame
@st.cache_data
def load_data(file):
    if file is not None:
        if file.name.endswith('csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        return df
    return None

# Load datasets
df1 = load_data(file_run1)
df2 = load_data(file_run2)

# Display uploaded data and some basic filtering options
if df1 is not None:
    st.header("Run 1 Data Preview")
    st.write(df1.head())

    # Sample filters: Adjust these filters based on your report structure
    st.sidebar.subheader("Filters for Run 1")

    # Example: Filter by a response time column (replace 'response_time' with actual column name)
    if 'response_time' in df1.columns:
        min_val = float(df1['response_time'].min())
        max_val = float(df1['response_time'].max())
        response_filter = st.sidebar.slider("Response Time Range (Run 1)", min_val, max_val, (min_val, max_val))
        df1 = df1[(df1['response_time'] >= response_filter[0]) & (df1['response_time'] <= response_filter[1])]

    # Create a histogram for response times using Plotly
    if 'response_time' in df1.columns:
        st.subheader("Response Time Distribution - Run 1")
        fig = px.histogram(df1, x="response_time", nbins=50, title="Run 1 Response Times")
        st.plotly_chart(fig, use_container_width=True)
    
if df2 is not None:
    st.header("Run 2 Data Preview")
    st.write(df2.head())

    st.sidebar.subheader("Filters for Run 2")
    if 'response_time' in df2.columns:
        min_val = float(df2['response_time'].min())
        max_val = float(df2['response_time'].max())
        response_filter2 = st.sidebar.slider("Response Time Range (Run 2)", min_val, max_val, (min_val, max_val))
        df2 = df2[(df2['response_time'] >= response_filter2[0]) & (df2['response_time'] <= response_filter2[1])]

    if 'response_time' in df2.columns:
        st.subheader("Response Time Distribution - Run 2")
        fig2 = px.histogram(df2, x="response_time", nbins=50, title="Run 2 Response Times")
        st.plotly_chart(fig2, use_container_width=True)

# Comparison section if two files are uploaded
if (df1 is not None) and (df2 is not None):
    st.header("Comparison Between Run 1 and Run 2")
    
    # Compute average response times (modify as per your actual data columns)
    if 'response_time' in df1.columns and 'response_time' in df2.columns:
        avg_run1 = df1['response_time'].mean()
        avg_run2 = df2['response_time'].mean()
        comparison_df = pd.DataFrame({
            "Test Run": ["Run 1", "Run 2"],
            "Average Response Time": [avg_run1, avg_run2]
        })
        st.write("### Average Response Times", comparison_df)
        
        # Bar chart comparison using Plotly
        comp_fig = px.bar(comparison_df, x="Test Run", y="Average Response Time",
                          title="Average Response Time Comparison",
                          text_auto='.2f')
        st.plotly_chart(comp_fig, use_container_width=True)
    
    # You can add more comparisons such as percentile analysis, error rates, etc.
    st.markdown("**Note:** You can further customize filters and charts based on the metrics available in your reports.")

# Additional options (if needed)
st.sidebar.markdown("## About")
st.sidebar.info("This dashboard was built using Streamlit, Pandas, Matplotlib, and Plotly. Customize the code for your specific needs.")


