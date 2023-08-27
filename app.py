import streamlit as st
import pandas as pd
import preprocessor,helper


df=preprocessor.preprocess()

# Define a radio button in the sidebar
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-wise Analysis')
)

st.dataframe(df)

if user_menu=='Medal Tally':
    medal_tally=helper.medal_tally(df)
    st.dataframe(medal_tally)