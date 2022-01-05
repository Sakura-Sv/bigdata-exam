import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    cfg = config[config_name]
    app.config.from_object(cfg)
    cfg.init_app(app)
    logging_conf(app)
    db.init_app(app)
    return app


def logging_conf(app):
    formatter = logging.Formatter(app.config['LOGGING_FORMATTER'])
    debug_log = os.path.join(app.config['BASE_DIR'],
                             app.config['LOGGING_ERROR_FILE'])
    debug_handler = RotatingFileHandler(debug_log)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    app.logger.addHandler(debug_handler)

    error_log = os.path.join(app.config['BASE_DIR'],
                             app.config['LOGGING_ERROR_FILE'])
    error_handler = RotatingFileHandler(error_log)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    app.logger.addHandler(error_handler)

    if app.config['DEBUG']:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
