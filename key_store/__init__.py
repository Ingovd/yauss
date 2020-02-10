from flask import Flask
from .database.inmemory import InMemoryKeys

db = type('obj', (object,), {'init_app' : lambda app: None, 'keys' : set()})
Api = InMemoryKeys

def create_app():
    app = Flask(__name__)

    with app.app_context():
        db.init_app(app)
        app.api = Api(db)
        from key_store.routes import key_store
        app.register_blueprint(key_store)
    return app