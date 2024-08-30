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

def get_poster_and_rating(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    #print(url)
    data = requests.get(url, headers=headers)
    data = data.json()
    poster_address = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    rating = data['vote_average']
    #print(data)
    return poster_address, rating

def recommendme(movie):
    index=mv1[mv1['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda vector1:vector1[1])
    rec_movie=[]
    rec_poster=[]
    rec_rating=[]
    for i in distance[0:100]:
        movie_id = mv1.iloc[i[0]].id
        poster_address, rating = get_poster_and_rating(movie_id)
        rec_movie.append(mv1.iloc[i[0]].title)
        rec_poster.append(poster_address)
        rec_rating.append(rating)
    return rec_movie, rec_poster, rec_rating

#Page design

st.title("Movie Recommendation System Based On Current User Rating")

movie_selected = st.selectbox("Select a movie that you have watched", movie_list)

if st.button("Get Recommendations"):
    rec_movie_name, rec_movie_poster,rec_movie_rating = recommendme(movie_selected)
    print(rec_movie_name)
    cols_row0 = st.columns(5)
    with cols_row0[2]:
        #st.text(rec_movie_name[0])
        st.image(rec_movie_poster[0])


    # Display the first 5 movies in the first row and 5 movies in the second row
    st.text("You might like")
    cols_row1 = st.columns(5)
    st.text("                              ")
    cols_row2 = st.columns(5)

    
    for i in range(1,6):
        with cols_row1[i-1]:
            st.image(rec_movie_poster[i])
            st.text(rec_movie_name[i])
            st.text("{}/10".format(rec_movie_rating[i]))

    for i in range(6, 11):
        with cols_row2[i-6]:
            st.image(rec_movie_poster[i])
            st.text(rec_movie_name[i])
            st.text("{}/10".format(rec_movie_rating[i]))

    


