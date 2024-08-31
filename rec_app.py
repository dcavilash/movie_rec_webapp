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

def get_poster_and_rating(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    data = requests.get(url, headers=headers).json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}", data['vote_average']

def recommendme(movie, min_rating):
    index = mv1[mv1['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])

    id = mv1[mv1['title'] == movie]['id'].iloc[0]
    rec_movie=[]
    rec_poster=[]
    rec_rating=[]
    for i in distances[0:100]:
        movie_id = mv1.iloc[i[0]].id
        poster_address, rating = get_poster_and_rating(movie_id)

        #filtering out movies with min rating, selected movie gets a pass anyway for display
        if rating >= min_rating or movie_id == id:
            rec_movie.append(mv1.iloc[i[0]].title)
            rec_poster.append(poster_address)
            rec_rating.append(rating)
            
        rec_df = pd.DataFrame({'title': rec_movie,'poster path': rec_poster,'user rating': rec_rating})
        if len(rec_df) >= 11:
            break
    
    return rec_df

st.title("Movie Recommendation System With Current User Rating Filter")
st.subheader("by Avilash Barua")
st.divider()

movie_selected = st.selectbox("Select or Search a Movie", movie_list)

col1, col2 = st.columns(2)
with col1:
    st.write("Minimum User Rating:")
with col2:
    min_rating = float(st.slider("", min_value=0.0, max_value=8.0, step=0.1, value=0.0))

if st.button("Get Recommendations"):
    rec_df = recommendme(movie_selected, min_rating)

    cols_row0 = st.columns(4)
    with cols_row0[1]:
        st.image(rec_df.iloc[0]['poster path'])
    with cols_row0[2]:
        st.text(f"{rec_df.iloc[0]['title']}")
        st.divider()
        st.text(f"User Rating: \n {rec_df.iloc[0]['user rating']}/10")

    cols_row1 = st.columns(5)
    for i in range(1, 6):  # Fill the first row, skipping the main movie
        with cols_row1[i - 1]:
            st.image(rec_df.iloc[i]['poster path'])
            st.text(f"{rec_df.iloc[i]['title']}\n{rec_df.iloc[i]['user rating']}/10")

    st.divider()
    cols_row2 = st.columns(5)
    for i in range(6, 11):  # Fill the second row
        with cols_row2[i - 6]:
            st.image(rec_df.iloc[i]['poster path'])
            st.text(f"{rec_df.iloc[i]['title']}\n{rec_df.iloc[i]['user rating']}/10")
