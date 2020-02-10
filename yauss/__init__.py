from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from key_store.gateway import GatewayKeys

from .database.mongo import MongoAPI
from .database.sql import SqlAPI
from .database.inmemory import InMemoryDB

mongo = PyMongo()
sql = SQLAlchemy()

# db = mongo
# Api = MongoAPI

db = sql
Api = SqlAPI

# db = type('obj', (object,), {'init_app' : lambda app: None, 'db' : {}})
# Api = InMemoryDB


def create_app():
    app = Flask(__name__)
    # app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/testdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\\instance\\test.db'

    with app.app_context():
        db.init_app(app)
        app.api = Api(db)

        from yauss.routes import url_crud
        app.register_blueprint(url_crud)

        if 'YAUSS_KEY_STORE_URI' not in app.config:
            default_key_store(app)
        app.key_api = GatewayKeys(app.config['YAUSS_KEY_STORE_URI'])
    return app

def default_key_store(app):
    from key_store.inmemory import InMemoryKeys
    from key_store.routes import key_store_routes
    app.register_blueprint(key_store_routes, url_prefix ='/keys')
    app.key_store = InMemoryKeys(set())
    app.config['YAUSS_KEY_STORE_URI'] = 'http://localhost:5000/keys'