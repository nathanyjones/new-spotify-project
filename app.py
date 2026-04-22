#Load in Libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ast 

from spotify_tools import recommend_similar

#Plot formatting
plt.rcParams.update({
    "figure.facecolor": (0, 0, 0, 0),  # (R, G, B, Alpha)
    "axes.facecolor": (0, 0, 0, 0),
    "savefig.transparent": True
})
plt.style.use('dark_background')

# Custom text style
st.set_page_config(page_title="Artist Exploration", layout = 'wide')

#Load in data
DATA_PATH = 'data/app_data.csv'
df = pd.read_csv(DATA_PATH)


#Creates a unique list for every artist
artist_list = df['artists'].unique().tolist()
artist_list.insert(0, 'All Artists')

#Title
st.title("Spotify Artist Exploration")

#Dropdown to select an artist
artist = st.selectbox('Select an artist:', options = artist_list)

#ALL ARTISTS
if artist == 'All Artists':
    # Print the df
    st.dataframe(df)
    
    tab1, tab2, tab3 = st.tabs(['Length','Acousticness', 'Tempo'])
    
    acous_avg = df.groupby('year')['acousticness'].mean().reset_index()
    durat_avg = df.groupby('year')['duration_s'].mean().reset_index()
    tempo_avg = df.groupby('year')['tempo'].mean().reset_index()
    # Song length
    with tab1:
    
        col1, col2 = st.columns(2)
        # Scatterplot
        with col1:
            fig, ax = plt.subplots()
            ax.scatter(durat_avg['year'], durat_avg['duration_s'] , color='#1DB954')
            ax.set_title('Average Song Length by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Length (in seconds)')
            ax.set_ylim(0,400)
            st.pyplot(fig)
        # Histogram
        with col2:
            fig, ax = plt.subplots()
            ax.hist(x = df['duration_s'], color = '#1DB954', bins = 1000)
            ax.set_title('Distribution of Song Length')
            ax.set_xlim(left = 100, right = 700)
            ax.set_xlabel('Length (in seconds)')
            ax.set_ylabel('Count')
            st.pyplot(fig)

    # Acousticness
    with tab2:
        col1, col2 = st.columns(2)
        # Scatterplot
        with col1:
            fig, ax = plt.subplots()
            ax.scatter(acous_avg['year'], acous_avg['acousticness'] , color='#1DB954')
            ax.set_title('Average Acousticness by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Acousticness')
            st.pyplot(fig)
        # Histogram
        with col2:
            fig, ax = plt.subplots()
            ax.hist(x = df['acousticness'], color = '#1DB954', bins = 1000)
            ax.set_title('Distribution of Song Accousticness')
            ax.set_xlabel('Acousticness')
            ax.set_ylabel('Count')
            ax.set_ylim(bottom = 0, top = 600)
            st.pyplot(fig)

    # Tempo
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.scatter(tempo_avg['year'], tempo_avg['tempo'] , color='#1DB954')
            ax.set_title(f'Average Tempo by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Tempo (Beats Per Minute)')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots()
            ax.hist(x = df['tempo'], color = '#1DB954', bins = 800)
            ax.set_title(f'Distribution of Song Tempo')
            ax.set_xlabel('Tempo (Beats Per Minute)')
            ax.set_xlim(50, 220)
            st.pyplot(fig)


# INDIVIDUAL ARTISTS
else: 
    
    # Reduces the DataFrame to just the selected artist
    df_selected = df[df['artists'] == artist].reset_index()
    #Must have at least 3 songs in the year to count
    df_selected = df_selected.groupby('year').filter(lambda x: len(x) >= 3).reset_index(drop = True)

    # Display dataframe on the app
    st.dataframe(df_selected)

    # Add a button using custom function to display song recs
    song = st.selectbox("Pick a song:", df_selected['name'])
    if st.button("Recommend"):
        recs = recommend_similar(df, song)
        st.dataframe(recs)

    tab1, tab2, tab3 = st.tabs(['Length','Acousticness', 'Tempo'])
    with tab1:
    
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.scatter(df_selected['year'], df_selected['duration_s'] , color='#1DB954')
            ax.set_title(f'Length of Songs by {artist}')
            ax.set_xlabel('Release Year')
            ax.set_ylabel('Length (in seconds)')
            st.pyplot(fig)
        
        with col2:
             fig, ax = plt.subplots()
             ax.hist(x = df_selected['duration_s'], color = '#1DB954', bins = 50)
             ax.set_title(f'Distribution of the Lengths of Songs by {artist}')
             ax.set_xlabel('Song Length')
             st.pyplot(fig)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.scatter(df_selected['year'], df_selected['acousticness'] , color='#1DB954')
            ax.set_title(f'Acousticness of Songs by {artist}')
            ax.set_xlabel('Release Year')
            ax.set_ylabel('Acousticness')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots()
            ax.hist(x = df_selected['acousticness'], color = '#1DB954', bins = 50)
            ax.set_title(f'Distribution of the Acousticness of Songs by {artist}')
            ax.set_xlabel('Acousticness')
            ax.set_ylabel('Count')
            st.pyplot(fig)
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.scatter(df_selected['year'], df_selected['tempo'] , color='#1DB954')
            ax.set_title(f'Tempo of Songs by {artist}')
            ax.set_xlabel('Release Year')
            ax.set_ylabel('Tempo (Beats Per Minute)')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots()
            ax.hist(x = df_selected['tempo'], color = '#1DB954', bins = 50)
            ax.set_title(f'Distribution of the Tempo of Songs by {artist}')
            ax.set_xlabel('Tempo (Beats Per Minute)')
            st.pyplot(fig)
    
    
