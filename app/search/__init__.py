from flask import Blueprint
from flask_restful import Api

from app.search.resources.search import TitleGuess, MovieMatch

search = Blueprint('search', __name__)
search_api = Api(search)

search_api.add_resource(TitleGuess, "/guess")
search_api.add_resource(MovieMatch, "/match")
