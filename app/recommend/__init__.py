import os
import warnings

from flask import Blueprint, current_app
from flask_restful import Api
from joblib import load

import config

env = os.getenv("FLASK_CONFIG", "development")
DEV_MODEL_DIR = "E:/projects/python/bigdata-exam/static/model/"
PROD_MODEL_DIR = "/var/www/bigdata-exam/model/"

warnings.filterwarnings("ignore")
base_path = DEV_MODEL_DIR if env == "development" else PROD_MODEL_DIR
cosine_sim = load(base_path + "recom-cos.pkl")
indices = load(base_path + "recom-ind.pkl")
smd = load(base_path + "recom-smd.pkl")
m = 5.244896612406511
C = 576.6399999999994


def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v / (v + m) * R) + (m / (m + v) * C)


def improved_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    movies = smd.iloc[movie_indices][["id", 'title', 'vote_count', 'vote_average', 'year']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.50)
    qualified = movies[
        (movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    ori_list = qualified[["id"]].values.tolist()
    tar_list = []
    for item in ori_list:
        tar_list.append(item[0])
    return tar_list


recommand = Blueprint('recommand', __name__)
recommand_api = Api(recommand)