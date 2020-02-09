from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from .database.mongo import MongoAPI
from .database.sql import SqlAPI
from .database.inmemory import InMemoryDB

mongo = PyMongo()
sql = SQLAlchemy()

# db = mongo
# Api = MongoAPI

# db = sql
# Api = SqlAPI

db = type('obj', (object,), {'init_app' : lambda app: None, 'db' : {}})
Api = InMemoryDB


def create_app():
    app = Flask(__name__)
    # app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/testdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\\instance\\test.db'

    with app.app_context():
        db.init_app(app)
        app.api = Api(db)
        from yauss.routes import url_crud
        app.register_blueprint(url_crud)
    return app