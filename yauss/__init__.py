from flask import Flask
from flask_pymongo import PyMongo
from .database import MongoAPI

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/testdb'

    with app.app_context():
        mongo.init_app(app)
        app.api = MongoAPI(mongo)
        from yauss.routes import url_crud
        app.register_blueprint(url_crud)
    return app