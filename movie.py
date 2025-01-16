import requests
import streamlit as st
import pickle
import gzip

api_key= st.secrets["api_key"]

def fetch_poster(movie_id):
    url =f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "http://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name, recommended_movies_poster

st.header("Chethan's Movie Recommendation System")

# Load the movie list
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Load the compressed similarity.pkl.gz
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or Select a movie to get recommendation',
    movie_list
)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    
    # Create individual columns and add content to each column
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.text(recommended_movies_name[0])
    col1.image(recommended_movies_poster[0], use_column_width=True)

    col2.text(recommended_movies_name[1])
    col2.image(recommended_movies_poster[1], use_column_width=True)

    col3.text(recommended_movies_name[2])
    col3.image(recommended_movies_poster[2], use_column_width=True)

    col4.text(recommended_movies_name[3])
    col4.image(recommended_movies_poster[3], use_column_width=True)

    col5.text(recommended_movies_name[4])
    col5.image(recommended_movies_poster[4], use_column_width=True)
