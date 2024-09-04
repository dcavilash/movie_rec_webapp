# Dynamic Movie Recommendation System
### Project Description:

Developed a movie recommendation system to provide personalized movie suggestions based on user ratings and similarity metrics. This interactive web application leverages Python, Streamlit, and various data science techniques to deliver a seamless user experience.

### Tools Used:
**kaggle.com:** for downloading the daily updated tmdb dataset in CSV format (august 2024). [Link](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)</br>
**Jupyter Notebook (analysis.ipynb):** Data Cleaning, testing codes on raw csv data and generating cosine similarity matrix file.</br>
**Python:** For data processing and algorithm implementation.</br>
**Streamlit:** For creating an interactive and user-friendly web application interface.</br>
**scikit-learn:** For calculating movie similarity and generating recommendations.</br>
**pandas:** For data manipulation and filtering.</br>
**requests:** For fetching real-time movie data from the TMDb API.</br>


### Key Features:

**Data Integration:** Utilized pickle to load and manage movie data and similarity matrices, ensuring efficient data handling.</br>
**Recommendation Engine:** Implemented a recommendation algorithm using scikit-learn to calculate movie similarities based on user preferences. The system utilizes cosine similarity and sparse matrices for accurate recommendations.</br>
**Memory Efficiency:** Implemented chunked computation of cosine similarity for large-scale vectors by leveraging sparse matrices (via csr_matrix) and processing in smaller batches, significantly reducing memory consumption and optimizing performance.</br>
**API Integration:** Integrated with The Movie Database (TMDb) API to fetch movie posters and ratings dynamically, enhancing the user interface with real-time data.</br>
**Interactive UI:** Designed an intuitive interface using Streamlit, allowing users to search and select movies, adjust rating filters, and view recommendations with posters and ratings.</br>
**Optimized Data Handling:** Reduced redundant API calls by caching movie poster and rating data, improving performance and user experience.</br>
**Responsive Layout:** Implemented a flexible layout to display recommendations in rows with up to 5 columns, adapting dynamically to the number of available suggestions.</br>


