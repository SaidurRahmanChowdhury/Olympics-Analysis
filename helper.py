import numpy as np

def fetch_medal_tally(df,year,country):
    
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    flag=0
    if year == 'Overall' and country == 'Overall':
        temp_df=medal_df
    
    if year == 'Overall' and country != 'Overall':
        flag=1
        temp_df=medal_df[medal_df['region'] == country]
    
    if year != 'Overall' and country == 'Overall':
        temp_df=medal_df[medal_df['Year'] == int(year)]
    
    if year!= 'Overall'  and country != 'Overall':
        temp_df=medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
     
    if flag ==1:
          x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    x['total']=x['Gold'] + x['Silver'] + x['Bronze']
    
    x['Gold']=x['Gold'].astype('int')
    x['Silver']=x['Silver'].astype('int')
    x['Bronze']=x['Bronze'].astype('int')
    x['total']=x['total'].astype('int')
    
    return x

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['total']=medal_tally['total'].astype('int')
    
    
    return medal_tally

def country_year_list(df):
     years=df['Year'].unique().tolist()
     years.sort()
     years.insert(0,'Overall')
     
     country=np.unique(df['region'].dropna().values).tolist()
     country.sort()
     country.insert(0,'Overall')
     
     return years,country


def data_over_time(df,col):
    
    over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values(by='Year')
    over_time.rename(columns={'Year':'Number of Years','count':col},inplace=True)
    
    return over_time


def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    
    if sport !='Overall':
        temp_df=temp_df[temp_df['Sport'] == sport]
        
     # Rename the index column to 'Name_Count'
    result_df = temp_df['Name'].value_counts().reset_index().head(15)
    result_df.rename(columns={'Name': 'index', 'index': 'Name'}, inplace=True)
    
     # Merge the result with the original DataFrame
    x= result_df.merge(df, left_on='index', right_on='Name', how='left')[['index','count','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','count':'Medals'},inplace=True)
    return x


def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
 
    return final_df


def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    
    return pt