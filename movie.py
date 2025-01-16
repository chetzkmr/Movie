import requests
import streamlit as st
import pickle
import gzip

st.set_page_config(
    page_title="Chethan's Movie Recommender",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a modern theme
st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #2E4053, #1C2833);
            color: #FDFEFE;
        }
        .stApp {
            background-color: #1C2833;
        }
        .header {
            font-size: 3rem;
            font-weight: bold;
            color: #FFC300; /* Modern yellow header */
            text-align: center;
            margin-bottom: 20px;
        }
        /* Style only the outer container of selectbox */
        div[data-baseweb="select"] > div {
            background-color: #2C3E50; /* Darker background for the select box */
            color: #FDFEFE; /* White text for better visibility */
            border-radius: 5px;
            border: 1px solid #34495E;
        }
        div[data-baseweb="select"]:hover > div {
            border: 1px solid #FFC300; /* Highlight border on hover */
        }
        .subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #D5D8DC;
            margin-bottom: 20px;
        }
        .movie-title {
            font-size: 1rem;
            font-weight: bold;
            color: #F7DC6F;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

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

# Load movies and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# App Header
st.markdown('<div class="header">🎬 Chethan\'s Movie Recommendation System</div>', unsafe_allow_html=True)

# Movie selection with updated styling for `st.selectbox`
movie_list = movies['title'].values
selected_movie = st.selectbox(
    '🎥 Type or Select a Movie to Get Recommendations:',
    movie_list,
)

# Button and recommendations logic
if st.button('💡 Show Recommendations'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)

    st.markdown('<div class="subheader">Here are your top 5 recommendations:</div>', unsafe_allow_html=True)

    # Display recommendations as cards
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f'<div class="movie-title">{recommended_movies_name[idx]}</div>', unsafe_allow_html=True)
            st.image(recommended_movies_poster[idx], use_container_width=True)
