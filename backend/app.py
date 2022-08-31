from flask import Flask, jsonify, request
from db import select_movies
from utils import load
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
app = Flask (__name__)

model = load ("model.pkl")

@app.route("/summary", methods=["GET"])
def get_movie_endpoint ():
    # request parameters
    summary = request.json["summary"]
    K = int(request.args.get("k") or 10)
    minYear = int(request.args.get("minYear") or 0)
    maxYear = int(request.args.get("maxYear") or 999999999)

    df = select_movies (min_year=minYear, max_year=maxYear)

    # evaluate cosine similarity from sentence encoding to all summary encodings
    df['values'] = pd.DataFrame(cosine_similarity(model.encode (summary).reshape(1, -1), df['encodings'].to_list())[0], columns=['values'])

    return jsonify (df.nlargest (K, columns=['values'])['title'].to_list())

if __name__ == "__main__":
    app.run(debug=True)
