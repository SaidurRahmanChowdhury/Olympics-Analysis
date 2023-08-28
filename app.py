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

if user_menu == 'Medal Tally':
    
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title(f"Medal Tally in {selected_year} Olympics" )
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(f"{selected_country} Overall Perfomance")
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(f"{selected_country}'s Overall Perfomance in {selected_year}")
    
    st.dataframe(medal_tally)