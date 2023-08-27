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

st.sidebar.title("Olympics Analysis")
# Define radio buttons as styled options
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


# Display content based on user selection
st.dataframe(df)

if user_menu == 'Medal Tally':
    
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    st.dataframe(medal_tally)