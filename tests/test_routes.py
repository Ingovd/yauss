from flask import message_flashed

from yauss import create_app

from yauss.templates.messages import *

recorded = []
def record(sender, message, category, **extra):
    recorded.append(message)

def record_flashes(func):
    recorded = []
    def wrapper(app, *args, **kwargs):
        message_flashed.connect(record, app)
        with app.test_client().session_transaction():
            return func(app, *args, **kwargs)
    return wrapper

def test_empty_db(client):
    response = client.get('/')
    assert b'No shortened URLs in the system, add one below.' in response.data

@record_flashes
def test_bad_url(app):
    client = app.test_client()
    with client.session_transaction():
        response = client.post('/', data=dict(long_url=""))
        assert USR_INVALID_URL in recorded

def test_read_url(app):
    key = 'abcdefgh'
    url = '127.0.0.1'
    app.db_backend.urls.update({key: url})
    response = app.test_client().get(f"/{key}")
    assert url.encode() in response.data
