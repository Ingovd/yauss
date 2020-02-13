import os

from flask import Flask
from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from .key_gateway import KeyGateway

from .database.inmemory import InMemoryAPI, InMemoryDB
from .database.sql import SqlAPI
from .database.mongo import MongoAPI


db_backends = {'mongo':    PyMongo,
               'sql':      SQLAlchemy,
               'inmemory': InMemoryDB}
db_apis = {'mongo':    MongoAPI,
           'sql':      SqlAPI,
           'inmemory': InMemoryAPI}


def create_app(instance_path=None):
    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
    else:
        app = Flask(__name__, instance_relative_config=True)
    print(f"Created Flask application in folder: {app.instance_path}")
    app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))

    with app.app_context():
        init_database(app)
        init_key_gateway(app)
        init_cache(app)
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


def init_key_gateway(app):
    if 'KEY_STORE_URI' not in app.config:
        local_key_store(app)
    app.key_gateway = KeyGateway(app.config['KEY_STORE_URI'],
                                 app.config['CACHE_KEY_REFILL'])


def init_cache(app):
    cache = Cache()
    cache.init_app(app)
    app.cache = cache


def init_routes(app):
    from yauss.routes import url_crud
    app.register_blueprint(url_crud)


def local_key_store(app):
    from key_store import key_apis
    from key_store.inmemory import InMemoryKeys
    from key_store.sql import SqlKeys
    from key_store.mongo import MongoKeys
    app.key_api = key_apis[app.config['DB_BACKEND']](app.db_api.db_backend)

    from key_store.routes import key_store_routes
    app.register_blueprint(key_store_routes, url_prefix='/keys')

    app.config['KEY_STORE_URI'] = "localhost/keys"
