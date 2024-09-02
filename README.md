# Dynamic Movie Recommendation System
Project Description:

Developed a movie recommendation system to provide personalized movie suggestions based on user ratings and similarity metrics. This interactive web application leverages Python, Streamlit, and various data science techniques to deliver a seamless user experience.

**Tools Used:**

Jupyter Notebook (analysis.ipynb) : Data Cleaning, testing codes on raw csv data(not included due to file size) from kaggle.com and generating cosine similarity matrix file.
Python: For data processing and algorithm implementation.
Streamlit: For creating an interactive and user-friendly web application interface.
scikit-learn: For calculating movie similarity and generating recommendations.
pandas: For data manipulation and filtering.
requests: For fetching real-time movie data from the TMDb API.
kaggle.com: for downloading latest tmdb dataset.
Key Features:

Data Integration: Utilized pickle to load and manage movie data and similarity matrices, ensuring efficient data handling.
Recommendation Engine: Implemented a recommendation algorithm using scikit-learn to calculate movie similarities based on user preferences. The system utilizes cosine similarity and sparse matrices for accurate recommendations.
API Integration: Integrated with The Movie Database (TMDb) API to fetch movie posters and ratings dynamically, enhancing the user interface with real-time data.
Interactive UI: Designed an intuitive interface using Streamlit, allowing users to search and select movies, adjust rating filters, and view recommendations with posters and ratings.
Optimized Data Handling: Reduced redundant API calls by caching movie poster and rating data, improving performance and user experience.
Responsive Layout: Implemented a flexible layout to display recommendations in rows with up to 5 columns, adapting dynamically to the number of available suggestions.


