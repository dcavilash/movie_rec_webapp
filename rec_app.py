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

    mv1_df = pd.DataFrame(mv1)
    filtered_mv1_df = mv1_df[mv1_df['vote_average'] >= min_rating - 0.5]

    # Add selected movie if it's lower than min_rating
    if index not in filtered_mv1_df['id'].values:
        filtered_mv1_df = pd.concat([filtered_mv1_df, mv1_df[mv1_df['id'] == index].iloc[0].to_frame().T], ignore_index=True)

    rec_df = filtered_mv1_df.iloc[[i[0] for i in distances[:18]]]
    rec_df.loc[rec_df.index, 'poster path'] = rec_df['id'].apply(lambda x: get_poster_and_rating(x)[0])
    rec_df.loc[rec_df.index, 'user rating'] = rec_df['id'].apply(lambda x: get_poster_and_rating(x)[1])

    return rec_df[rec_df['user rating'] >= min_rating]

st.title("Movie Recommendation System With Current User Rating Filter")
st.header("by Avilash Barua")
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
        st.text(rec_df.iloc[0]['title'])
        st.divider()
        st.text(f"User Rating: {rec_df.iloc[0]['user rating']}/10")

    st.text("You might like:")

    cols_row1, cols_row2 = st.columns(5, 5)
    for i in range(1, 11):
        col = cols_row1 if i <= 5 else cols_row2
        with col[i % 5]:
            st.image(rec_df.iloc[i]['poster path'])
            st.text(rec_df.iloc[i]['title'])
            st.text(f"User Rating: {rec_df.iloc[i]['user rating']}/10")