from contextlib import contextmanager

from flask import message_flashed

from yauss import create_app

from yauss.templates.messages import *


@contextmanager
def record_flashes(app):
    recorded = []
    def record(sender, message, category, **extra):
        recorded.append(message)
    message_flashed.connect(record, app)
    yield recorded
    message_flashed.disconnect(record, app)

def test_empty_db(client):
    response = client.get('/')
    assert b'No shortened URLs in the system, add one below.' in response.data

def test_bad_url(app):
    client = app.test_client()
    with record_flashes(app) as recorded:
        response = client.post('/', data=dict(long_url=""))
        assert USR_INVALID_URL in recorded

def test_read_url(app):
    key = 'abcdefgh'
    url = '127.0.0.1'
    app.db_backend.urls.update({key: url})
    response = app.test_client().get(f"/{key}")
    assert url.encode() in response.data
