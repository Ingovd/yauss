from contextlib import contextmanager

from flask import message_flashed

from yauss.templates.messages import *


_key = 'abcdefgh'
_url = '127.0.0.1'


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


def test_bad_key_store(yauss):
    yauss.keys.fail = True
    with record_flashes(yauss) as recorded:
        r = yauss.test_client().post('/', data=dict(long_url=_url))
        assert USR_UNEXPECTED in recorded


def test_insert_url(yauss):
    with record_flashes(yauss) as recorded:
        response = yauss.test_client().post('/', data=dict(long_url=_url), follow_redirects=True)
        assert _url.encode() in response.data
        assert yauss.format_url(_url) in [ku.url for ku in yauss.urls]


def test_del_url(yauss):
    client = yauss.test_client()
    with record_flashes(yauss) as recorded:
        response = client.post('/', data=dict(long_url=""))
        assert USR_INVALID_URL in recorded
    yauss.urls[_key] = _url
    response = client.get(f"/delete/{_key}")
    assert _url not in [ku.url for ku in yauss.urls]


def test_read_url_success(yauss):
    yauss.urls[_key] = _url
    response = yauss.test_client().get(f"/{_key}")
    assert _url.encode() in response.data


def test_update_url(yauss):
    client = yauss.test_client()
    yauss.urls[_key] = _url
    response = client.get(f"/update/{_key}")
    assert _url.encode() in response.data
    new_url = _url + '/'
    client.post(f"/update/{_key}", data=dict(long_url=new_url))
    assert yauss.format_url(new_url) == yauss.urls[_key]
    with record_flashes(yauss) as recorded:
        client.post(f"/update/{_key}", data=dict(long_url=''))
        assert USR_INVALID_URL in recorded


def test_read_url_cached(yauss):
    client = yauss.test_client()
    yauss.urls[_key] = _url
    client.get(f"/{_key}")
    del yauss.urls[_key]
    response = client.get(f"/{_key}")
    assert _url.encode() in response.data

def test_404(yauss):
    client = yauss.test_client()
    response = client.get(f"/{_key}")
    assert response.status_code == 404
    response = client.get(f"/update/{_key}")
    assert response.status_code == 404
    response = client.post(f"/update/{_key}")
    assert response.status_code == 404
    respone = client.get(f"/delete/{_key}")
    assert response.status_code == 404