import json
from ast import literal_eval

from app import db


class MovieInfo(db.Model):
    __tablename__ = 'movies_metadata'
    adult = db.Column(db.Boolean())
    belongs_to_collection = db.Column(db.Text())
    budget = db.Column(db.Integer())
    genres = db.Column(db.Text())
    homepage = db.Column(db.VARCHAR(256))
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    imdb_id = db.Column(db.VARCHAR(16))
    original_language = db.Column(db.VARCHAR(8))
    original_title = db.Column(db.VARCHAR(128))
    overview = db.Column(db.Text())
    popularity = db.Column(db.FLOAT())
    poster_path = db.Column(db.VARCHAR(256))
    production_companies = db.Column(db.Text())
    production_countries = db.Column(db.Text())
    release_date = db.Column(db.VARCHAR(32))
    revenue = db.Column(db.Integer())
    runtime = db.Column(db.FLOAT())
    spoken_languages = db.Column(db.Text())
    status = db.Column(db.VARCHAR(16))
    tagline = db.Column(db.Text())
    title = db.Column(db.VARCHAR(256))
    video = db.Column(db.Boolean())
    vote_average = db.Column(db.FLOAT())
    vote_count = db.Column(db.Integer())

    def to_json(self):
        genres = []
        production_companies = []
        for item in literal_eval(self.genres):
            genres.append(item["name"])
        for item in literal_eval(self.production_companies):
            production_companies.append(item["name"])
        return {
            "adult": self.adult,
            "belongs_to_collection": literal_eval(
                self.belongs_to_collection) if self.belongs_to_collection is not None else self.belongs_to_collection,
            "budget": self.budget,
            "genres": genres,
            "id": self.id,
            "imdb_id": self.imdb_id,
            "original_title": self.original_title,
            "original_language": self.original_language,
            "overview": self.overview,
            "popularity": self.popularity,
            "poster_path": "https://image.tmdb.org/t/p/original" + self.poster_path,
            "production_countries": literal_eval(
                self.production_countries) if self.production_countries is not None else self.production_countries,
            "production_companies": production_companies,
            "release_date": self.release_date,
            "revenue": self.revenue,
            "runtime": self.runtime,
            "spoken_languages": literal_eval(
                self.spoken_languages) if self.spoken_languages is not None else self.spoken_languages,
            "status": self.status,
            "tagline": self.tagline,
            "title": self.title,
            "video": self.video,
            "vote_average": self.vote_average,
            "vote_count": self.vote_count,
        }

    def to_overview_json(self):
        genres = []
        for item in literal_eval(self.genres):
            genres.append(item["name"])
        return {
            "id": self.id,
            "imdb_id": self.imdb_id,
            "poster_path": "https://image.tmdb.org/t/p/original" + str(self.poster_path),
            "title": self.title,
            "genres": genres,
            "vote_average": self.vote_average,
            "vote_count": self.vote_count,
            "overview": self.overview
        }


class Credit(db.Model):
    __tablename__ = "credits"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    movie_id = db.Column(db.Integer(), db.ForeignKey("movies_metadata.id"), unique=True, index=True, nullable=False)
    cast = db.Column(db.TEXT())
    crew = db.Column(db.Text())
    credit_to_movie = db.relationship("MovieInfo", backref=db.backref("credits", lazy="dynamic"))

    def to_json(self):
        cast = []
        crew = []
        for item in literal_eval(self.cast):
            cast.append({
                "character": item["character"],
                "name": item["name"],
                "order": item["order"],
                "gender": "male" if item["gender"] == 2 else "female",
                "profile_path":
                    "https://image.tmdb.org/t/p/original" + item["profile_path"] if item[
                                                                                        "profile_path"] is not None else ""
            })
        for item in literal_eval(self.crew):
            crew.append({
                "department": item["department"],
                "job": item["job"],
                "name": item["name"],
                "gender": "male" if item["gender"] == 2 else "female",
                "profile_path":
                    "https://image.tmdb.org/t/p/original" + item["profile_path"] if item[
                                                                                        "profile_path"] is not None else ""
            })
        return {
            "cast": cast,
            "crew": crew,
        }


class Keyword(db.Model):
    __tablename__ = "keywords"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    movie_id = db.Column(db.Integer(), db.ForeignKey("movies_metadata.id"), unique=True, index=True, nullable=False)
    keywords = db.Column(db.TEXT())
    keyword_to_movie = db.relationship("MovieInfo", backref=db.backref("keywords", lazy="dynamic"))

    def to_json(self):
        keywords = []
        for item in literal_eval(self.keywords):
            keywords.append(item["name"])
        return keywords
