import os

from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from yauss.database.inmemory import InMemoryDB


from .inmemory import InMemoryKeys
from .sql import SqlKeys
from .mongo import MongoKeys


key_default =           {'backend': InMemoryDB, 'api': InMemoryKeys}
key_inits   = {'mongo': {'backend': PyMongo,    'api': MongoKeys},
               'sql':   {'backend': SQLAlchemy, 'api': SqlKeys},
               'inmemory': key_default}


def create_app(instance_path=None):
    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
    else:
        app = Flask(__name__, instance_relative_config=True)
    app.logger.info(f"Created Flask application in folder: {app.instance_path}")
    app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))

    with app.app_context():
        init_database(app)
        init_routes(app)
    return app


def init_database(app):
    configured_db = app.config.get('DB_BACKEND')
    if not (key_init := key_inits.get(configured_db)):
        app.logger.warning(APP_INVALID_DB)
        app.config['DB_BACKEND'] = 'inmemory'
        key_init = key_default
    try:
        db_backend = key_init['backend']()
        db_backend.init_app(app)
        key_api = key_init['api'](db_backend)
    except Exception as err:
        app.logger.critical(APP_DB_SETUP_1ERR.format(err))
        raise err
    app.db_backend = db_backend
    app.key_api = key_api


def init_routes(app):
    from .routes import key_store_routes
    app.register_blueprint(key_store_routes)