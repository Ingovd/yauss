from contextlib import contextmanager

from flask import message_flashed

from yauss.templates.messages import *


@contextmanager
def record_flashes(app):
    recorded = []
    def record(sender, message, category, **extra):
        recorded.append(message)
    message_flashed.connect(record, app)
    yield recorded
    message_flashed.disconnect(record, app)

def test_empty_db(yauss_client):
    response = yauss_client.get('/')
    assert b'No shortened URLs in the system, add one below.' in response.data

def test_bad_url(yauss):
    client = yauss.test_client()
    with record_flashes(yauss) as recorded:
        response = client.post('/', data=dict(long_url=""))
        assert USR_INVALID_URL in recorded

def test_read_url(yauss):
    key = 'abcdefgh'
    url = '127.0.0.1'
    yauss.urls[key] = url
    response = yauss.test_client().get(f"/{key}")
    assert url.encode() in response.data
