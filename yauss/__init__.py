import os

from flask import Flask
from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from .templates.messages import *

from .key_gateway import KeyGateway

from .database.inmemory import InMemoryUrls, InMemoryDB
from .database.sql import SqlUrls
from .database.mongo import MongoUrls


db_default =         {'backend': InMemoryDB, 'api': InMemoryUrls}
db_inits = {'mongo': {'backend': PyMongo,    'api': MongoUrls},
            'sql':   {'backend': SQLAlchemy, 'api': SqlUrls},
            'inmemory': db_default}


def create_app(config={}):
    if path := config.get('INSTANCE_PATH', None):
        app = Flask(__name__, instance_path=path)
    else:
        app = Flask(__name__, instance_relative_config=True)
    app.logger.info(f"Created Flask application in folder: {app.instance_path}")
    app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))
    app.config.update(config)

    with app.app_context():
        init_database(app)
        init_key_gateway(app)
        init_cache(app)
        init_routes(app)
    return app


def init_database(app):
    if not db_init := db_inits.get(app.config.get('DB_BACKEND')):
        app.logger.warning(APP_INVALID_DB)
        db_init = db_default
    try:
        db_backend = db_init['backend']()
        db_backend.init_app(app)
        url_api = db_init['api'](db_backend)
    except Exception as err:
        app.logger.critical(APP_DB_SETUP_1ERR.format(err))
        raise err
    app.db_backend = db_backend
    app.urls = url_api


def init_key_gateway(app):
    if 'KEY_STORE_URI' not in app.config:
        local_key_store(app)
    app.key_gateway = KeyGateway(app.config['KEY_STORE_URI'],
                                 app.config.get('CACHE_KEY_REFILL', 3))


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
    app.key_api = key_apis[app.config['DB_BACKEND']](app.db_backend)

    from key_store.routes import key_store_routes
    app.register_blueprint(key_store_routes, url_prefix='/keys')

    app.config['KEY_STORE_URI'] = f"http://{app.config['SERVER_NAME']}/keys"
    
