from flask_restful import Resource


class Movie(Resource):
    """Movie Api"""

    def get(self):

        return "hello"