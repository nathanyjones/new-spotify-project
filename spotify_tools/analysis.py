import pandas as pd
# Summary stats for artists
def artist_summary(df, artist):

    df = df[df['artists'] == artist]

    return df.describe()[['duration_s', 'energy', 'acousticness', 'tempo']]

def feature_trend(df, feature):
    """
    Average feature value per year.
    """

    df = df.copy()
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    return df.groupby('year')[feature].mean().reset_index()