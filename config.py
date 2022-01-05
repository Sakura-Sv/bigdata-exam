# coding: utf-8
"""Config file."""

import os


class Config:
    """Basic config."""

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    LOGGING_FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' \
                        ' [in %(pathname)s:%(lineno)d]'
    LOGGING_ERROR_FILE = 'data/app_error.log'
    LOGGING_DEBUG_FILE = 'data/app_debug.log'

    @staticmethod
    def init_app(app):
        """Nothing."""
        pass


class DevelopmentConfig(Config):
    """Dev config."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PYMYSQL_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MODEL_DIR = "E:/projects/python/bigdata-exam/static/model/"


class ProductionConfig(Config):
    """Production config."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('PYMYSQL_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MODEL_DIR = "/var/www/bigdata-exam/model/"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
