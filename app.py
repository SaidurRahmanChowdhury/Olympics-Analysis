import streamlit as st
import pandas as pd

# Define a radio button in the sidebar
st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-wise Analysis')
)
