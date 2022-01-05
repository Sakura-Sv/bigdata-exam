from flask import request
from flask_restful import Resource

from app import db


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
        guess = db.session.execute(
            "select id, title from movies_metadata where match(title, overview) against(:KEYWORD)",
            {"KEYWORD": keyword}).all()
        data = list()
        for item in guess:
            data.add(item["title"])
        return {
            "status": 1,
            "message": "success",
            "data": data
        }