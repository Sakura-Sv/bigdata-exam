from ast import literal_eval
from random import random

from flask import request
from flask_restful import Resource

from app import db
from app.movie.models.movie import MovieInfo, Keyword, Credit
from app.utils.restful_add_args import add_args
from app.recommend import improved_recommendations


class MovieInfoApi(Resource):
    """ 电影信息相关 """

    # 根据电影id获取电影具体信息
    def get(self):
        movie_id = request.args.get("movie_id")
        movie = db.session.query(MovieInfo).filter(MovieInfo.id.__eq__(movie_id)).first()
        if movie is not None:
            data = movie.to_json()
            keywords = db.session.query(Keyword).filter(Keyword.movie_id.__eq__(movie.id)).first()
            credits = db.session.query(Credit).filter(Credit.movie_id.__eq__(movie.id)).first()
            data["keywords"] = keywords.to_json() if keywords is not None else keywords
            data["credits"] = credits.to_json() if credits is not None else credits
            try:
                recommend_ids = improved_recommendations(movie.title)
                recommend_rows = db.session.execute("SELECT * FROM movies_metadata WHERE id in :IDS",
                                                    {"IDS": recommend_ids}).all()
                recommend_list = []
                for row in recommend_rows:
                    genres = []
                    for item in literal_eval(row["genres"]):
                        genres.append(item["name"])
                    movie = {
                        "genres": genres,
                        "id": row["id"],
                        "imdb_id": row["imdb_id"],
                        "overview": row["overview"],
                        "poster_path": "https://image.tmdb.org/t/p/original" + row["poster_path"],
                        "title": row["title"],
                        "vote_average": row["vote_average"],
                        "vote_count": row["vote_count"],
                    }
                    recommend_list.append(movie)
                data["recommand_list"] = recommend_list
            except Exception as e:
                data["recommand_list"] = []
            return {
                "status": 1,
                "message": "success",
                "data": data
            }
        else:
            return {
                "status": 0,
                "message": "Movie not be found!"
            }


class MovieListApi(Resource):
    """ 电影列表相关 """

    # 根据电影类别获取电影列表
    def get(self):
        genres = request.args.get("genres")
        ori_movie_list = db.session.query(MovieInfo).filter(MovieInfo.genres.like("%" + genres + "%")).all()
        res_movie_list = [movie.to_overview_json() for movie in ori_movie_list]
        return {
            "status": 1,
            "message": "success",
            "data": res_movie_list
        }


class MovieStar(Resource):

    def post(self):
        args = add_args([
            "movie_id", int, True, "movie id",
            "score", int, True, "score",
        ]).parse_args()
        destiny = random.randint(0, 100)
        if destiny > 98:
            return {
                "status": 0,
                "message": "There are some errors!"
            }
        else:
            return {
                "status": 1,
                "message": "success",
            }
