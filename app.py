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
        st.header("Participating Nations Over The Years:")
        st.plotly_chart(fig)
        
        
        events_over_time=helper.data_over_time(df,'Event')
        fig=px.line(events_over_time,x='Number of Years',y='Event')
        st.header("Events Over The Years:")
        st.plotly_chart(fig)
        
        athletes_over_time=helper.data_over_time(df,'Name')
        fig=px.line(athletes_over_time,x='Number of Years',y='Name')
        st.header("Athletes Over The Years:")
        st.plotly_chart(fig)
        
        
        st.header("Number of Events Over Time:")
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
        
        
        st.header('Top 15 Successful Atheletes:')
        
        sports_list=df['Sport'].unique().tolist()
        sports_list.sort()
        sports_list.insert(0,'Overall')
        selected_sports=st.selectbox('Select a sport:',sports_list)
        x=helper.most_successful(df,selected_sports)
        
        st.table(x)

if user_menu == 'Country-wise Analysis':
    
    st.sidebar.title('Country Wise Analysis:')
    
    region_list=df['region'].dropna().unique().tolist()
    region_list.sort()
    
    selected_region=st.sidebar.selectbox('Select a Region:',region_list)
    
    country_df=helper.yearwise_medal_tally(df,selected_region)
    fig=px.line(country_df,x='Year',y='Medal')
    st.header(selected_region + " Medal Tally Over The Years:")
    st.plotly_chart(fig)
    
    st.title(selected_region + ' excels in the following sports')
    pt=helper.country_event_heatmap(df,selected_region)
    
    fig,ax=plt.subplots(figsize=(20, 20))

    if not pt.empty:
        
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
        
    else:
        
        # Display an attractive centered warning message when pt is empty
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
                <div style="background-color: #ffe6e6; padding: 20px; border-radius: 5px; text-align: center;">
                    <p style="color: #ff0000; font-size: 18px; font-weight: bold;">
                        This team hasn't won any Olympics medals.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    
   