from flask import request
from flask_restful import Resource

from app import db
from app.movie.models.movie import MovieInfo, Keyword, Credit


class MovieInfoApi(Resource):
    """ 电影信息相关 """

    # 根据电影id获取电影具体信息
    def get(self):
        movid_id = request.args.get("movie_id")
        movie = db.session.query(MovieInfo).filter(MovieInfo.id.__eq__(movid_id)).first()
        if movie is not None:
            data = movie.to_json()
            keywords = db.session.query(Keyword).filter(Keyword.movie_id.__eq__(movie.id)).first()
            credits = db.session.query(Credit).filter(Credit.movie_id.__eq__(movie.id)).first()
            data["keywords"] = keywords.to_json() if keywords is not None else keywords
            data["credits"] = credits.to_json() if credits is not None else credits
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
