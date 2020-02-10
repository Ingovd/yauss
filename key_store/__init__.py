from flask import Flask
from .inmemory import InMemoryKeys

Api = InMemoryKeys

def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.api = Api(set())
        from key_store.routes import key_store
        app.register_blueprint(key_store)
    return app
