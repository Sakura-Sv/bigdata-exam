from ast import literal_eval

from flask import request
from flask_restful import Resource

from app import db
from app.movie.models.movie import Keyword, Credit


class TitleGuess(Resource):

    def get(self):
        keyword = request.args.get("keyword")
        guess = db.session.execute(
            "select id, title from movies_metadata where match(title) against(:KEYWORD) LIMIT 20",
            {"KEYWORD": keyword}).all()
        data = set()
        for item in guess:
            if len(data) == 10:
                break
            data.add(item["title"])
        data = list(data)
        data.sort()
        return {
            "status": 1,
            "message": "success",
            "data": data
        }


class MovieMatch(Resource):

    def get(self):
        keyword = request.args.get("keyword")
        match = db.session.execute(
            "select genres, id, imdb_id, overview, poster_path, title, vote_average, vote_count from movies_metadata where match(title, overview) against(:KEYWORD)",
            {"KEYWORD": keyword}).all()
        data = []
        for row in match:
            genres = []
            production_companies = []
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
            data.append(movie)
        return {
            "status": 1,
            "message": "success",
            "data": data
        }