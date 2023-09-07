import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns
import scipy

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

st.sidebar.image('https://cdn.pixabay.com/photo/2016/07/22/16/39/olympia-1535219_1280.jpg')
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
            st.header("Cities")
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
    
    st.title(selected_region + ' excels in the following sports:')
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
        
    
    st.title('Top 10 Successful Atheletes in ' +selected_region +':')
    coutrywise_atheletes=helper.most_successful_countrywise(df,selected_region)  
    st.table(coutrywise_atheletes)
    

    

if user_menu == 'Athlete wise Analysis':
    
    # Create a dataframe without duplicate rows based on 'Name' and 'region' columns
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Filter and clean data for age of athletes with medals
    overall_age = athlete_df['Age'].dropna()
    gold_age = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    silver_age = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_age = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # Create a distribution plot
    fig = ff.create_distplot(
        [overall_age, gold_age, silver_age, bronze_age],
        ['Overall', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        colors=['#3498db', '#f1c40f', '#95a5a6', '#e74c3c'],  # Custom colors for each curve
        show_hist=False,  # Hide histograms
        show_rug=False,   # Hide rug plots
    )

    # Customize the layout
    fig.update_layout(
        title="Age Distribution of Athletes by Medal",
        xaxis_title="Age",
        yaxis_title="Density",
        legend=dict(x=0.75, y=0.95),  # Adjust legend position
        font=dict(family="Arial", size=12),
        plot_bgcolor='#ecf0f1',  # Background color,
        autosize=False,
        width=1000,
        height=600
    )
    st.title('Distribution of Age:')
    # Show the updated figure
    st.plotly_chart(fig)
    
    x=[]
    name=[]
    famous_sports=['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics',
               'Art Competitions','Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Shooting',
               'Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis',
               'Golf','Softball','Archery','Volleyball','Synchronized Swimming','Table Tennis','Baseball',
               'Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Triathlon','Rugby','Polo',
               'Ice Hockey']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
        
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    # Customize the layout
    fig.update_layout(
            title="Age Distribution of Gold Medalists in Famous Sports",
            xaxis_title="Age",
            yaxis_title="Density",
            autosize=False,
            width=1000,
            height=600
        )
    st.title('Distribution of Age of Gold Medalist:')
    st.plotly_chart(fig)
    
    
    
    y=[]
    name1=[]
    famous_sports1=['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics',
               'Art Competitions','Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Shooting',
               'Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis',
               'Golf','Softball','Archery','Volleyball','Synchronized Swimming','Table Tennis','Baseball',
               'Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Triathlon','Rugby','Polo',
               'Ice Hockey']
    
    for sport1 in famous_sports1:
        temp_df1=athlete_df[athlete_df['Sport']==sport1]
        y.append(temp_df1[temp_df1['Medal']=='Silver']['Age'].dropna())
        name1.append(sport1)
        
    fig1=ff.create_distplot(y,name1,show_hist=False,show_rug=False)
    # Customize the layout
    fig.update_layout(
            title="Age Distribution of Silver Medalists in Famous Sports",
            xaxis_title="Age",
            yaxis_title="Density",
            autosize=False,
            width=1000,
            height=600
        )
    st.title('Distribution of Age of Silver Medalist:')
    st.plotly_chart(fig1)
    
    st.title('Height Vs Weight:')
    sports_list=df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sports=st.selectbox('Select a sport:',sports_list)
    temp_df=helper.weight_vs_height(df,selected_sports)
    fig,ax=plt.subplots(figsize=(20, 20))
    
    ax=sns.scatterplot(y=temp_df['Height'],x=temp_df['Weight'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig)
    
    
    st.title('Men Vs Women Perticipation Over The Years:')
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])

    st.plotly_chart(fig)
    