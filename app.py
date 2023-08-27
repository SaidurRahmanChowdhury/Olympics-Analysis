import streamlit as st
import pandas as pd
import preprocessor, helper

# Set page title and icon
st.set_page_config(
    page_title="Olympics Analysis",
    page_icon="🏅",
    layout="wide"
)

# Load and preprocess data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

# Add some CSS styles for the sidebar
st.markdown(
    """
    <style>
    .sidebar {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .sidebar-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #007BFF;
    }
    .sidebar-option {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .sidebar-option:hover {
        background-color: #007BFF;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-header">Menu</div>', unsafe_allow_html=True)

# Define radio buttons as styled options
user_menu = st.sidebar.radio(
    '',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-wise Analysis'),
    index=0,
    key='menu'
)

# Display content based on user selection
st.dataframe(df)

if user_menu == 'Medal Tally':
    medal_tally = helper.medal_tally(df)
    st.dataframe(medal_tally)
