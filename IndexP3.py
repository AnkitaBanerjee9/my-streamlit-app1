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

df = load_data(uploaded_file)

if df is not None:
    # Section 1: Report Preview & Filtering
    st.header("Report Preview & Filtering")
    
    preview_columns = st.sidebar.multiselect("Select columns for preview", df.columns.tolist(), default=df.columns.tolist())
    logical_column = st.sidebar.selectbox("Select column for row filtering", df.columns.tolist())
    unique_vals = df[logical_column].dropna().unique().tolist()
    selected_vals = st.sidebar.multiselect("Select row values to display", unique_vals, default=unique_vals)
    
    preview_df = df[df[logical_column].isin(selected_vals)][preview_columns]
    st.dataframe(preview_df)

    # Section 2: Download Filtered Data
    st.sidebar.subheader("Download Filtered Data")
    file_format = st.sidebar.radio("Select format", ["CSV", "Excel"])
    
    if st.sidebar.button("Download"):
        if file_format == "CSV":
            preview_df.to_csv("filtered_data.csv", index=False)
            st.sidebar.success("Filtered data saved as filtered_data.csv")
        else:
            preview_df.to_excel("filtered_data.xlsx", index=False)
            st.sidebar.success("Filtered data saved as filtered_data.xlsx")

    # Section 3: Response Time Comparison
    st.header("Response Time Comparison: Run1 vs Run2 vs Run3")
    
    required_cols = ['TransactionName', 'SLA', 'Run1-90Percent', 'Run2-90Percent', 'Run3-90Percent']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"The following required columns are missing: {missing}")
    else:
        avg_run1 = df['Run1-90Percent'].mean()
        avg_run2 = df['Run2-90Percent'].mean()
        avg_run3 = df['Run3-90Percent'].mean()
        
        st.write(f"**Run1-90Percent Average Response Time:** {avg_run1:.2f}")
        st.write(f"**Run2-90Percent Average Response Time:** {avg_run2:.2f}")
        st.write(f"**Run3-90Percent Average Response Time:** {avg_run3:.2f}")
        
        best_run = min(avg_run1, avg_run2, avg_run3)
        if best_run == avg_run1:
            st.success("Run1-90Percent has the best (lowest) response times overall.")
        elif best_run == avg_run2:
            st.success("Run2-90Percent has the best (lowest) response times overall.")
        else:
            st.success("Run3-90Percent has the best (lowest) response times overall.")

        # Section 4: Graphical Comparison
        st.subheader("Graphical Comparison by Transaction")
        
        transaction_options = df['TransactionName'].dropna().unique().tolist()
        selected_transactions = st.multiselect("Select transactions to display in graph", transaction_options, default=transaction_options)

        min_rt_run1 = float(df['Run1-90Percent'].min())
        max_rt_run1 = float(df['Run1-90Percent'].max())
        rt_range_run1 = st.slider("Select Run1 response time range", min_rt_run1, max_rt_run1, (min_rt_run1, max_rt_run1))
        
        min_rt_run2 = float(df['Run2-90Percent'].min())
        max_rt_run2 = float(df['Run2-90Percent'].max())
        rt_range_run2 = st.slider("Select Run2 response time range", min_rt_run2, max_rt_run2, (min_rt_run2, max_rt_run2))
        
        min_rt_run3 = float(df['Run3-90Percent'].min())
        max_rt_run3 = float(df['Run3-90Percent'].max())
        rt_range_run3 = st.slider("Select Run3 response time range", min_rt_run3, max_rt_run3, (min_rt_run3, max_rt_run3))
        
        df_graph = df[
            (df['TransactionName'].isin(selected_transactions)) &
            (df['Run1-90Percent'].between(rt_range_run1[0], rt_range_run1[1])) &
            (df['Run2-90Percent'].between(rt_range_run2[0], rt_range_run2[1])) &
            (df['Run3-90Percent'].between(rt_range_run3[0], rt_range_run3[1]))
        ]
        
        df_plot = df_graph[['TransactionName', 'Run1-90Percent', 'Run2-90Percent', 'Run3-90Percent']].melt(
            id_vars='TransactionName',
            value_vars=['Run1-90Percent', 'Run2-90Percent', 'Run3-90Percent'],
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

        # Section 5: Anomaly Detection (Highlight Slow Transactions)
        st.subheader("Anomaly Detection: Transactions Exceeding SLA")
        
        df_anomalies = df[df['Run1-90Percent'] > df['SLA']]
        if not df_anomalies.empty:
            st.warning("The following transactions exceed the SLA:")
            st.dataframe(df_anomalies[['TransactionName', 'SLA', 'Run1-90Percent']])
        else:
            st.success("No transactions exceed SLA limits.")

        # Section 6: Performance Trend Analysis
        st.subheader("Performance Trend Analysis")
        
        df_trend = df[['TransactionName', 'Run1-90Percent', 'Run2-90Percent', 'Run3-90Percent']].melt(
            id_vars='TransactionName',
            value_vars=['Run1-90Percent', 'Run2-90Percent', 'Run3-90Percent'],
            var_name='Run',
            value_name='Response Time'
        )

        fig_trend = px.line(
            df_trend, 
            x='TransactionName', 
            y='Response Time', 
            color='Run', 
            markers=True, 
            title="Response Time Trend Over Runs"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Section 7: Dark Mode Toggle
        st.sidebar.subheader("Toggle Dark Mode")
        dark_mode = st.sidebar.checkbox("Enable Dark Mode")
        if dark_mode:
            st.markdown(
                """
                <style>
                body { background-color: #0e1117; color: white; }
                .stDataFrame { background-color: #1e1e1e; }
                </style>
                """,
                unsafe_allow_html=True
            )

else:
    st.info("Please upload a report file to begin the analysis.")
