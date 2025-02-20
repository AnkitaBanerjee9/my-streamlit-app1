import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.title("Performance Load Test Report")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)


import plotly.express as px

# Plotting response times
if uploaded_file is not None:
    fig = px.line(df, x='Timestamp', y='ResponseTime', title='Response Time Over Time')
    st.plotly_chart(fig)


uploaded_file_1 = st.file_uploader("Choose first file", type=["csv", "xlsx"], key='1')
uploaded_file_2 = st.file_uploader("Choose second file", type=["csv", "xlsx"], key='2')

if uploaded_file_1 is not None and uploaded_file_2 is not None:
    df1 = pd.read_csv(uploaded_file_1)
    df2 = pd.read_csv(uploaded_file_2)
    
    st.write("Comparing Test Runs")
    
    # Plotting comparison graph
    df1['Run'] = 'Run 1'
    df2['Run'] = 'Run 2'
    df_combined = pd.concat([df1, df2])
    fig = px.line(df_combined, x='Timestamp', y='ResponseTime', color='Run', title='Response Time Comparison')
    st.plotly_chart(fig)


if uploaded_file is not None:
    min_response_time = st.slider('Min Response Time', min_value=float(df['ResponseTime'].min()), max_value=float(df['ResponseTime'].max()))
    filtered_df = df[df['ResponseTime'] >= min_response_time]
    fig = px.line(filtered_df, x='Timestamp', y='ResponseTime', title='Filtered Response Time')
    st.plotly_chart(fig)
