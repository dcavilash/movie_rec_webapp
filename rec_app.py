import streamlit as st
import pickle
import requests
import pandas as pd

# Load movie data and similarity matrix
mv1 = pickle.load(open('movies.pkl', 'rb'))
movie_list = mv1['title'].values
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

# API authentication
my_api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkNWY1ZTc1ZDgyNjMzYTU5NmE4ZWJkM2ZkYzgwZTM2YSIsIm5iZiI6MTcyNDk4MDY5MC4xMjY1ODQsInN1YiI6IjY2ZDExOGUwNmRmMzFjZGNhMzMwNDVkZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CieuhUZpIRe6qQlEg0IlIXR28pba6V44j7GY07VkzUs"
headers = {"accept": "application/json", "Authorization": "Bearer " + my_api_token}


@st.cache_data(persist=True)
def get_poster_and_rating(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    data = requests.get(url, headers=headers).json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}", data['vote_average']


@st.cache_data(persist=True)
def recommendme(movie, min_rating, selected_genres):
    index = mv1[mv1['title'] == movie].index[0]
    
    # Get similarity scores and sort them
    distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
    
    # Get the ID of the selected movie
    id = mv1[mv1['title'] == movie]['id'].iloc[0]
    m_sel_poster_address, m_sel_rating = get_poster_and_rating(id)

    # Initialize lists for recommendations (include the selected movie first)
    rec_movie = [mv1.iloc[index].title]
    rec_poster = [m_sel_poster_address]
    rec_rating = [m_sel_rating]

    # Filter and sort movies
    for i in distances:
        movie_id = mv1.iloc[i[0]].id
        if movie_id == id:
            continue  # Skip the selected movie
        
        poster_address, rating = get_poster_and_rating(movie_id)
        if rating < min_rating:
            continue  # Skip movies below the minimum rating
        
        # Filter by selected genres if applicable
        if selected_genres:
            recommended_movie_genres = set(mv1.iloc[i[0]].genres.split(", "))
            if not any(genre in selected_genres for genre in recommended_movie_genres):
                continue  # Skip if none of the selected genres match
        
        # Append valid recommendations
        rec_movie.append(mv1.iloc[i[0]].title)
        rec_poster.append(poster_address)
        rec_rating.append(rating)
        
        # Break loop if we have enough recommendations
        if len(rec_movie) == 9:
            break

    # Create DataFrame with recommendations
    rec_df = pd.DataFrame({'title': rec_movie, 'poster path': rec_poster, 'user rating': rec_rating})
    
    return rec_df



st.title("Dynamic Movie Recommendation System")
with st.expander("info"):
    st.text("Avilash's Project")
    #st.subheader("by Avilash Barua")
    #st.markdown("dcavilash@ github project")
    st.markdown("[GitHub](https://github.com/dcavilash/movie_rec_webapp) with Project Description")
st.divider()

c1, c2 = st.columns(2)
with c1:
    movie_selected = st.selectbox("Select or Search a Movie", [""] + movie_list)
    st.divider()
    min_rating = 0.0
    min_rating = float(st.slider("Minimum User Rating:", min_value=0.0, max_value=8.0, step=0.1, value=0.0))

if movie_selected and movie_selected != "":
    id = mv1[mv1['title'] == movie_selected]['id'].iloc[0]
    m_sel_poster_address, m_sel_rating = get_poster_and_rating(id)
    with c2:
        c21, c22 = st.columns(2)
        with c21:
            st.image(m_sel_poster_address)
        with c22:
            st.markdown(f"User Rating:<br><b><span style='font-size:20px'>{m_sel_rating}</b>/10", unsafe_allow_html=True)
            
#create genre toggle buttons
genres_of_selected_movie = mv1[mv1['title'] == movie_selected]['genres'].values[0].split(", ")
selected_genres = st.multiselect("Filter by Genre:", options = genres_of_selected_movie, default = None)

if st.button("Get Recommendations"):
    rec_df = recommendme(movie_selected, min_rating, selected_genres)

    cols_row1 = st.columns(4)
    for i in range(1, 5):  # Fill the first row
        with cols_row1[i - 1]:
            st.image(rec_df.iloc[i]['poster path'])
            st.markdown(f"{rec_df.iloc[i]['title']}<br><b><span style='font-size:20px'>{rec_df.iloc[i]['user rating']}</b>/10", unsafe_allow_html=True)

    st.divider()
    cols_row2 = st.columns(4)
    for i in range(5, 9):  # Fill the second row
        with cols_row2[i - 5]:
            st.image(rec_df.iloc[i]['poster path'])
            st.markdown(f"{rec_df.iloc[i]['title']}<br><b><span style='font-size:20px'>{rec_df.iloc[i]['user rating']}</b>/10", unsafe_allow_html=True)

