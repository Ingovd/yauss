from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from yauss.database.inmemory import InMemoryDB


from .inmemory import InMemoryKeys
from .sql import SqlKeys
from .mongo import MongoKeys


db_backends = {'mongo':    PyMongo,
               'sql':      SQLAlchemy,
               'inmemory': InMemoryDB}
db_apis = {'mongo':    MongoKeys,
           'sql':      SqlKeys,
           'inmemory': InMemoryKeys}


def create_app(instance_path=None):
    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
    else:
        app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    with app.app_context():
        init_database(app)
        init_routes(app)
    return app


def init_database(app):
    try:
        config_db = app.config['DB_BACKEND']
    except KeyError:
        raise Exception("No valid database configured")
    db_backend = db_backends[config_db]()
    app.db_backend = db_backend
    db_backend.init_app(app)
    db_api = db_apis[config_db](db_backend)
    app.db_api = db_api


def init_routes(app):
    from .routes import key_store_routes
    app.register_blueprint(key_store_routes)