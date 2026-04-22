#Load in data
import pandas as pd
import ast

df = pd.read_csv('data.csv')
def fix_artists(df):
    #Seperate out the lists in the artist column
    df['artists'] = df['artists'].apply(ast.literal_eval)
    # One row per artist
    df = df.explode('artists')

def reduce_list(df):
    #Filter out artists with less than 40 songs and less than 10 unique years
    df = df.groupby('artists').filter(lambda x: len(x) >= 40).reset_index(drop = True)
    df = df.groupby('artists').filter(lambda x: x['year'].nunique() >= 10)

    #Filter out classical artists & music producers, they dont work well with what we hope to display
    df = df.groupby('artists').filter(lambda x: x['acousticness'].mean() <= .75)

def column_cleaning(df):
#Convert miliseconds into seconds and rename the column
    df = df[df['duration_ms'] > 53000]
    df['duration_ms'] = df['duration_ms']/1000

    df = df.rename(columns = {'duration_ms' : 'duration_s'})

#Replace 1s and 0s in explicit column
    df['explicit'] = df['explicit'].map({1: 'Yes', 0: 'No'})

#Sort by artist name
df = df.sort_values(by ='artists').reset_index(drop = True)

df = df[['name', 'artists', 'year', 'duration_s', 'tempo', 'acousticness', 'energy', 'valence', 'key', 'popularity', 'explicit']]

df = df.drop_duplicates(subset=['name', 'artists']).reset_index(drop=True)

df.to_csv('app_data.csv', index = False)