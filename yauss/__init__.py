from flask import Flask
from flask_caching import Cache

from .key_gateway import KeyGateway

from .database.inmemory import InMemoryAPI
from .database.sql import SqlAPI
from .database.mongo import MongoAPI


initialise_db_backend = {'mongo':    MongoAPI,
                         'sql':      SqlAPI,
                         'inmemory': InMemoryAPI}


def create_app(instance_path=None):
    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
    else:
        app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    with app.app_context():
        init_database(app)
        init_key_gateway(app)
        init_cache(app)
        init_routes(app)
    return app


def init_database(app):
    try:
        initialise_db_backend[app.config['DB_BACKEND']](app)
    except KeyError:
        raise Exception("No valid database configured")


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
    from key_store.inmemory import InMemoryKeys
    from key_store.sql import SqlKeys
    from key_store.mongo import MongoKeys
    key_api = {'mongo': MongoKeys, 'sql': SqlKeys, 'inmemory': InMemoryKeys}
    app.key_store = key_api[app.config['DB_BACKEND']](app.db_api.db)

    from key_store.routes import key_store_routes
    app.register_blueprint(key_store_routes, url_prefix='/keys')

    app.config['KEY_STORE_URI'] = f"http://{app.config['SERVER_NAME']}/keys"
