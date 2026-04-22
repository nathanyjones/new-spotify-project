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

def top_songs(df, feature, n=10):
    """
    Return top n songs ranked by a given feature.
    """

    df = df.copy()

    # Check column exists
    if feature not in df.columns:
        raise ValueError(f"{feature} is not a valid column")

    # Convert to numeric safely
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Drop missing values
    df = df.dropna(subset=[feature])

    # Remove duplicates (important)
    df = df.drop_duplicates(subset=['name', 'artists'])

    # Sort and select top n
    top = df.sort_values(feature, ascending=False).head(n)

    # Return clean output
    return top[['name', 'artists', feature]]