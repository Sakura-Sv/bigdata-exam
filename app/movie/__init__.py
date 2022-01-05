from flask import Blueprint
from flask_restful import Api

from app.movie.resources.movie import MovieInfoApi, MovieListApi

movie = Blueprint('movie', __name__)
movie_api = Api(movie)

movie_api.add_resource(MovieInfoApi, "/info")
movie_api.add_resource(MovieListApi, "/list")
