import streamlit as st
import pickle
import requests

mv1 = pickle.load(open('movies.pkl', 'rb'))
movie_list = mv1['title'].values
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))


my_api_token="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkNWY1ZTc1ZDgyNjMzYTU5NmE4ZWJkM2ZkYzgwZTM2YSIsIm5iZiI6MTcyNDk4MDY5MC4xMjY1ODQsInN1YiI6IjY2ZDExOGUwNmRmMzFjZGNhMzMwNDVkZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CieuhUZpIRe6qQlEg0IlIXR28pba6V44j7GY07VkzUs"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + my_api_token
    }

def get_poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    print(url)
    data = requests.get(url, headers=headers)
    data = data.json()
    poster_address = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    print(data)
    return poster_address

def recommendme(movie):
    index=mv1[mv1['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda vector1:vector1[1])
    rec_movie=[]
    rec_poster=[]
    for i in distance[0:11]:
        movie_id = mv1.iloc[i[0]].id
        rec_movie.append(mv1.iloc[i[0]].title)
        rec_poster.append(get_poster(movie_id))
    return rec_movie, rec_poster

#Page design

st.title("Movie Recommendation System Based On Current User Rating")

movie_selected = st.selectbox("Select a movie that you have watched", movie_list)

if st.button("Get Recommendations"):
    rec_movie_name, rec_movie_poster = recommendme(movie_selected)

    col0 = st.columns(1)
    # Display the first 5 movies in the first row and 5 movies in the second row
    cols_row1 = st.columns(5)
    cols_row2 = st.columns(5)

    
    for i in range(1,6):
        with cols_row1[i]:
            st.text(rec_movie_name[i])
            st.image(rec_movie_poster[i])
    for i in range(6, 11):
        with cols_row2[i]:
            st.text(rec_movie_name[i])
            st.image(rec_movie_poster[i])

    with col0[0]:
        st.text(rec_movie_name[0])
        st.image(rec_movie_poster[0])


