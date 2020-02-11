from flask import Flask
from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from key_store.gateway import GatewayKeys
from key_store.inmemory import InMemoryKeys
from key_store.sql import SqlKeys
from key_store.mongo import MongoKeys

from .database.mongo import MongoAPI
from .database.sql import SqlAPI
from .database.inmemory import InMemoryDB

cache = Cache()

db = PyMongo()
Api = MongoAPI
KeyApi = MongoKeys

# db = SQLAlchemy()
# Api = SqlAPI
# KeyApi = SqlKeys

# db = type('obj', (object,), {'init_app' : lambda app: None, 'table' : {'urls' : {}, 'keys': set()}})
# Api = InMemoryDB
# KeyApi = InMemoryKeys


def create_app():
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 86400
    app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/testdb'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\\instance\\test.db'

    with app.app_context():
        cache.init_app(app)
        app.cache = cache

        db.init_app(app)
        app.api = Api(db)

        from yauss.routes import url_crud
        app.register_blueprint(url_crud)

        if 'YAUSS_KEY_STORE_URI' not in app.config:
            local_key_store(app, db)
        app.key_api = GatewayKeys(app.config['YAUSS_KEY_STORE_URI'])
    return app

def local_key_store(app, db):
    from key_store.routes import key_store_routes
    app.register_blueprint(key_store_routes, url_prefix ='/keys')
    app.key_store = KeyApi(db)
    app.config['YAUSS_KEY_STORE_URI'] = 'http://localhost:5000/keys'
