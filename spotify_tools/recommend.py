import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


FEATURE_COLS = [
 'energy', 'acousticness',
    'tempo', 'valence'
]
def recommend_similar(df, song_name, n=5):

    df = df.copy()

    # Convert to numeric
    for col in FEATURE_COLS:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=FEATURE_COLS).reset_index(drop=True)

    if song_name not in df['name'].values:
        raise ValueError("Song not found")

    # Feature matrix
    X = df[FEATURE_COLS].values

    # Get the selected song vector
    idx = df[df['name'] == song_name].index[0]
    song_vec = X[idx].reshape(1, -1)

    # 🔥 ONLY compute similarity to this one song
    sim_scores = cosine_similarity(song_vec, X).flatten()

    # Get top matches
    top_idx = sim_scores.argsort()[::-1][1:n+1]

    return df.iloc[top_idx][['name', 'artists']]