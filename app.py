from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Load the saved model and data
with open("movie_similarity.pkl", "rb") as f:
    similarity_matrix = pickle.load(f)

with open("movie_indices.pkl", "rb") as f:
    movie_indices = pickle.load(f)

# Load the dataset (to fetch movie names)
df = pd.read_csv("imdb_top_1000.csv")

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "IMDB Movie Recommendation API is Running!"

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.json
        movie_name = data.get("movie_name")

        # Check if the movie exists in our dataset
        if movie_name not in movie_indices:
            return jsonify({"error": "Movie not found in dataset!"}), 400

        # Get the movie index
        movie_idx = movie_indices[movie_name]

        # Get similarity scores and sort
        similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get top 10 similar movies
        top_movies = [df.iloc[i[0]]["Series_Title"] for i in similarity_scores[1:11]]

        return jsonify({"recommended_movies": top_movies})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
