import pandas as pd
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def createSimilarity():
    data = pd.read_csv('main_data.csv')
    ratings = pd.read_csv('ratings.csv')

    # create pivot table of ratings data
    ratings_pivot = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)

    # convert pivot table to sparse matrix
    ratings_matrix = csr_matrix(ratings_pivot.values)

    # compute cosine similarities between items
    similarities = np.dot(ratings_matrix.T, ratings_matrix)
    norm = np.array([np.sqrt(np.diagonal(similarities))])
    similarity = similarities / norm / norm.T

    # create DataFrame with movie titles as index and columns
    movie_titles = data['movie_title'].tolist()
    similarity_df = pd.DataFrame(similarity, index=movie_titles, columns=movie_titles)

    return (data, similarity_df)


def getAllMovies():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())

user_ratings = pd.DataFrame(columns=['user_id', 'movie_id', 'rating'])

def Recommend(user_id, movie, rating):
    movie = movie.lower()
    try:
        data.head()
        similarity.shape
    except:
        (data, similarity) = createSimilarity()

    if movie not in data['movie_title'].unique():
        return 'Sorry! The movie you requested is not present in our database.'
    else:
        movie_id = data.loc[data['movie_title'] == movie, 'movie_id'].iloc[0]
        user_ratings.loc[len(user_ratings)] = [user_id, movie_id, rating]
        user_data = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
        user_row = user_data.loc[user_id]
        user_most_liked_movie_id = user_row.idxmax()
        user_most_liked_movie_title = data.loc[data['movie_id'] == user_most_liked_movie_id, 'movie_title'].iloc[0]
        sim_scores = similarity.loc[user_most_liked_movie_title].values
        sim_indices = sim_scores.argsort()[::-1][1:20]
        movieList = data.iloc[sim_indices]['movie_title'].tolist()
        return movieList



app = Flask(__name__, static_folder='Kenyaflix/build',
            static_url_path='/')
CORS(app)

@app.route('/api/movies/<user_id>', methods=['GET'])
@cross_origin()
def movies(user_id):
    # returns all the movies in the dataset and the user's most liked movie
    movies = getAllMovies()
    user_data = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
    user_row = user_data.loc[user_id]
    user_most_liked_movie_id = user_row.idxmax()
    user_most_liked_movie_title = data.loc[data['movie_id'] == user_most_liked_movie_id, 'movie_title'].iloc[0]
    result = {'arr': movies, 'most_liked_movie': user_most_liked_movie_title}
    return jsonify(result)



@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/similarity/<user_id>/<name>/<int:rating>')
@cross_origin()
def similarity(user_id, name, rating):
    movie = name
    recommendations = Recommend(user_id, movie, rating)
    if type(recommendations) == type('string'):
        resultArray = recommendations.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)
    else:
        movieString = '---'.join(recommendations)
        resultArray = movieString.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)



@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
