import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie):
    response = requests.get('https://www.omdbapi.com/?t={}&apikey=81d01e65'.format(movie))
    data = response.json()
    if data["Poster"] == 'N/A':
        return 'https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg'
    return data['Poster']

def fetch_info(movie):
    response = requests.get('https://www.omdbapi.com/?t={}&apikey=81d01e65'.format(movie))
    data = response.json()
    return data

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].title
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

movies_list = pickle.load(open('movieslist.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))



st.title("MovieEcho")

selected_movie_name = st.selectbox(
    'Get movie recommendation',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    data = fetch_info(selected_movie_name)

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(data['Title'])
        if data['Poster'] == 'N/A':
            st.image('https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg')
        else:
            st.image(data['Poster'])

    with right_column:
        st.subheader('Plot')
        st.write(data['Plot'])
        st.text('Runtime: ' + data['Runtime'])
        st.text('Genre: ' + data['Genre'])
        st.text('Top Actors: ')
        for i in data['Actors'].split(','):
            st.text(i)
        st.text('Director: ' + data['Director'])
        for i in data['Ratings']:
            if i['Source'] == 'Rotten Tomatoes':
                st.text('Rotten Tomatoes Rating: ' + i['Value'])

    st.title('Similar to ' + selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])