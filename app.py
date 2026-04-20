#Load in Libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ast 

#Plot formatting
plt.rcParams.update({
    "figure.facecolor": (0, 0, 0, 0),  # (R, G, B, Alpha)
    "axes.facecolor": (0, 0, 0, 0),
    "savefig.transparent": True
})
plt.style.use('dark_background')

st.set_page_config(page_title="Artist Exploration", layout = 'wide')

#Load in data and section off by artist
DATA_PATH = 'data.csv'
df = pd.read_csv(DATA_PATH)

#Seperate out the lists in the artist column
df['artists'] = df['artists'].apply(ast.literal_eval)
# One row per artist
df = df.explode('artists')

#Filter out artists with less than 40 songs and less than 10 unique years
df = df.groupby('artists').filter(lambda x: len(x) >= 40).reset_index(drop = True)
df = df.groupby('artists').filter(lambda x: x['year'].nunique() >= 10)

#Filter out classical artists & music producers, they dont work well with what we hope to display
df = df.groupby('artists').filter(lambda x: x['acousticness'].mean() <= .75)

#Creates a unique list for every artist
artist_list = df['artists'].unique().tolist()
artist_list.insert(0, 'All Artists')

#Convert miliseconds into seconds and rename the column
df = df[df['duration_ms'] > 53000]
df['duration_ms'] = df['duration_ms']/1000
df = df.rename(columns = {'duration_ms' : 'duration_s'})


#Dropdown to select an artist
artist = st.selectbox('Select an artist:', options = artist_list)

if artist == 'All Artists':

    st.dataframe(df)
    tab1, tab2 = st.tabs(['Average Song Length','Average Song Acousticness'])
    
    acous_avg = df.groupby('year')['acousticness'].mean().reset_index()
    durat_avg = df.groupby('year')['duration_s'].mean().reset_index()

    with tab1:
    
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.scatter(durat_avg['year'], durat_avg['duration_s'] , color='#1DB954')
            ax.set_title('Average Song Length by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Length (in seconds)')
            st.pyplot(fig)
        
        with col2:
             fig, ax = plt.subplots()
             ax.hist(x = df['duration_s'], color = '#1DB954', bins = 1000)
             ax.set_title('Distribution of Song Length')
             ax.set_xlim(left = 100, right = 700)
             st.pyplot(fig)


    with tab2:
        fig, ax = plt.subplots()
        ax.scatter(acous_avg['year'], acous_avg['acousticness'] , color='#1DB954')
        ax.set_title('Average Acousticness by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Acousticness')
        st.pyplot(fig)
else: 
    
    #Reduces the DataFrame to just the selected artist
    df_selected = df[df['artists'] == artist].reset_index()
    #Must have at least 3 songs in the year to count
    df_selected = df_selected.groupby('year').filter(lambda x: len(x) >= 3).reset_index(drop = True)

    #Display dataframe on the app
    st.dataframe(df_selected)

    tab1, tab2 = st.tabs(['Average Song Length','Average Song Acousticness'])
    with tab1:
    
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.scatter(df_selected['year'], df_selected['duration_s'] , color='#1DB954')
            ax.set_title('Song Length by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Length (in seconds)')
            st.pyplot(fig)
        
        with col2:
             fig, ax = plt.subplots()
             ax.hist(x = df_selected['duration_s'], color = '#1DB954', bins = 50)
             ax.set_title('Distribution of Song Length')
             ax.set_xlabel('Song Length')
             st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots()
        ax.scatter(df_selected['release_date'], df_selected['acousticness'] , color='#1DB954')
        ax.set_title('Acousticness')
        ax.set_xlabel('Year')
        ax.set_ylabel('Acousticness')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_major_locator(mdates.YearLocator(1)) 
        st.pyplot(fig)
    
    
