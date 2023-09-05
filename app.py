import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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
    
if user_menu == "Overall Analysis":
        
        editions=df['Year'].nunique()-1
        cities=df['City'].nunique()
        sports=df['Sport'].nunique()
        events=df['Event'].nunique()
        athletes=df['Name'].nunique()
        nations=df['region'].nunique()
        
        # Center-align the title "Top Statistics"
        st.markdown("<h1 style='text-align: center;'>Top Statistics</h1>", unsafe_allow_html=True)
        
        col1,col2,col3=st.columns(3)
        
        with col1:
            st.header("Editions")
            st.title(editions) 
            
        with col2:
            st.header("Hosts")
            st.title(cities) 
            
        with col3:
            st.header("Sports")
            st.title(sports) 
            
        col1,col2,col3=st.columns(3)
        
        with col1:
            st.header("Events")
            st.title(events) 
            
        with col2:
            st.header("Athletes")
            st.title(athletes) 
            
        with col3:
            st.header("Nations")
            st.title(nations) 
        
        
        nations_over_time=helper.data_over_time(df,'region')
        fig=px.line(nations_over_time,x='Number of Years',y='region')
        st.title("Participating Nations Over The Years:")
        st.plotly_chart(fig)
        
        
        events_over_time=helper.data_over_time(df,'Event')
        fig=px.line(events_over_time,x='Number of Years',y='Event')
        st.title("Events Over The Years:")
        st.plotly_chart(fig)
        
        athletes_over_time=helper.data_over_time(df,'Name')
        fig=px.line(athletes_over_time,x='Number of Years',y='Name')
        st.title("Athletes Over The Years:")
        st.plotly_chart(fig)
        
        
        st.title("Number of Events Over Time:")
        # Create a larger figure size
        fig,ax=plt.subplots(figsize=(20, 20))

        # Create the pivot table and customize the heatmap
        x=df.drop_duplicates(['Year','Sport','Event'])
        pivot_table = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
        sns.set(font_scale=1.2)  # Increase font size
        ax=sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5, cbar=False)

        # Add labels and title
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('Sport', fontsize=14)
        plt.title('Number of Events by Year and Sport', fontsize=16)

        # Rotate tick labels for better readability
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)

        # Show the plot
        st.pyplot(fig)
        
        
        st.title('Top 15 Successful Atheletes:')
        
        sports_list=df['Sport'].unique().tolist()
        sports_list.sort()
        sports_list.insert(0,'Overall')
        selected_sports=st.selectbox('Select a sport:',sports_list)
        x=helper.most_successful(df,selected_sports)
        
        st.table(x)
