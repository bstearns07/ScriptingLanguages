#Movie ratings code
import pandas as pd
import numpy as np

#Load data
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

#Create a pivot table
user_movie_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')

#Calculate the similarity between users using Pearson correlation
user_similarity = user_movie_matrix.corr(method='pearson')


def recommend_movies(user_id, user_movie_matrix, movies, user_similarity, num_recommendations=5):
    """
    Recommend movies for a specific user based on the ratings of similar users.

    Parameters:
        user_id (int): The ID of the user for whom to recommend movies.
        user_movie_matrix (DataFrame): The user-movie rating matrix.
        movies (DataFrame): The movies metadata containing movieId and title.
        user_similarity (DataFrame): The matrix of user similarities.
        num_recommendations (int): The number of recommendations to return.

    Returns:
        DataFrame: A list of recommended movie titles.
    """

    #Get the ratings
    user_ratings = user_movie_matrix.loc[user_id]

    #Find users similar to the target user
    similar_users = user_similarity[user_id].dropna().sort_values(ascending=False)

    #Initialize arrays to keep track of weighted sums and similarity sums for ratings
    weighted_sum = np.zeros(user_movie_matrix.shape[1])
    similarity_sum = np.zeros(user_movie_matrix.shape[1])

    #Loop similar users
    for similar_user, similarity in similar_users.items():
        if similar_user != user_id:  #skip the user itself
            similar_user_ratings = user_movie_matrix.loc[similar_user]
            valid_ratings = similar_user_ratings.dropna().index  #movies that the similar user has rated
            weighted_sum[valid_ratings] += similar_user_ratings[valid_ratings] * similarity
            similarity_sum[valid_ratings] += similarity

    #Avoid division by zero
    similarity_sum = np.where(similarity_sum == 0, 1, similarity_sum)

    #Compute the predicted ratings
    predicted_ratings = weighted_sum / similarity_sum

    #Get the movies
    unrated_movies = user_ratings[user_ratings.isna()].index
    recommendations = pd.Series(predicted_ratings[unrated_movies], index=unrated_movies).dropna()

    #Sort the recommendations
    top_recommendations = recommendations.sort_values(ascending=False).head(num_recommendations)

    #Get the movie titles
    recommended_movie_titles = movies[movies['movieId'].isin(top_recommendations.index)][['title']]

    return recommended_movie_titles


#Test
user_id = 1  # Example: recommend movies for user with ID 1
recommended_movies = recommend_movies(user_id, user_movie_matrix, movies, user_similarity)

print("Recommended movies for user {}:".format(user_id))
print(recommended_movies)
