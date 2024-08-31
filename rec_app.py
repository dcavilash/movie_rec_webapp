import streamlit as st
import pickle
import requests
import pandas as pd

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

def recommendme(movie, min_rating):
    index=mv1[mv1['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda vector1:vector1[1])

    mv1_df = pd.DataFrame(mv1)
    
    # Filter by minimum rating if applicable
    if min_rating != -1:
        filtered_mv1_df = mv1_df[mv1_df['vote_average'] >= min_rating - 0.5]

        # Need to add selected movie in the dataframe if its lower than min_rating entered

        if index not in filtered_mv1_df['id'].values:
            row_to_add = mv1_df[mv1_df['id'] == index].iloc[0]
            filtered_mv1_df = pd.concat([filtered_mv1_df, row_to_add.to_frame().T], ignore_index=True)
    else:
        filtered_mv1_df = mv1_df
    
    rec_movies=[]
    rec_posters=[]
    rec_ratings=[]
    for i in distance[0:100]:
        movie_id = filtered_mv1_df.iloc[i[0]].id
        poster_address, rating = get_poster_and_rating(movie_id)
        rec_movies.append(filtered_mv1_df.iloc[i[0]].title)
        rec_posters.append(poster_address)
        rec_ratings.append(rating)
    rec_df = pd.DataFrame({
        'title': rec_movies,
        'poster path': rec_posters,
        'user rating': rec_ratings
    })
    
    return rec_df

####################        Page design      ########################################################################################################

st.title("Movie Recommendation System With Current User Rating filter")
st.header("by Avilash Barua")
st.divider()

movie_selected = st.selectbox("Select or Search a Movie", movie_list)

min_rating = -1                                        #default value
min_rating = float(st.slider("Minimun User Rating out of 10 (Optional)", min_value=0, max_value=8))


if st.button("Get Recommendations"):
    rec_df = recommendme(movie_selected, min_rating)
    
    cols_row0 = st.columns(4)
    with cols_row0[1]:
        st.image(rec_df.iloc[0]['poster path'])
        #
        #
    with cols_row0[2]:
        st.text(rec_df.iloc[0]['title'])
        st.divider()
        st.text("User Rating: ")
        st.text("{}/10".format(rec_df.iloc[0]['user rating']))


    # Display the next 10 movies in two rows of 5
    st.text("You might like:")
    
    cols_row1 = st.columns(5)
    cols_row2 = st.columns(5)
    
    for i in range(1, 6):
        with cols_row1[i - 1]:
            st.image(rec_df.iloc[i]['poster path'])
            st.text(rec_df.iloc[i]['title'])
            st.text("{}/10".format(rec_df.iloc[i]['user rating']))
    
    for i in range(6, 11):
        with cols_row2[i - 6]:
            st.image(rec_df.iloc[i]['poster path'])
            st.text(rec_df.iloc[i]['title'])
            st.text("{}/10".format(rec_df.iloc[i]['user rating']))