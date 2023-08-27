import pandas as pd

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

def preprocess():
    global df, region_df

    # Filtering for summer olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region_df
    df = df.merge(region_df, on='NOC', how='left')

    # Dropping duplicates
    df.drop_duplicates(inplace=True)

    # One hot encoding medals
    medal_dummies = pd.get_dummies(df['Medal'])
    df = pd.concat([df, medal_dummies], axis=1)
    return df

