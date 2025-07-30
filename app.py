import streamlit as st
import pickle
import pandas as pd
import requests

# Load pickled data
movie_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster from TMDb API
def fetch_poster(movie_id):
    api =  '8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return None

# Recommend function with poster support
def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].movie_id  # assumes you have 'movie_id' column
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Streamlit App
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox(
    'Select a movie to get recommendations:',
    movie_list['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0], use_container_width=True)
    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1], use_container_width=True)        
    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2], use_container_width=True)
    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3], use_container_width=True) 
    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4], use_container_width=True)
    st.success('Recommendations displayed above!')
# Note: Replace    