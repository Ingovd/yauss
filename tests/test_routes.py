from yauss import create_app


def test_empty_db(client):
    response = client.get('/')
    assert b'No shortened URLs in the system, add one below.' in response.data

def test_read_url(app):
    key = 'abcdefgh'
    url = '127.0.0.1'
    app.db_backend.urls.update({key: url})
    response = app.test_client().get(f"/{key}")
    assert url.encode() in response.data