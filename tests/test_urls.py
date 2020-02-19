def test_crud(yauss):
    key = 'abcdefgh'
    url = 'http://127.0.0.1'
    assert len(yauss.urls) == 0
    yauss.urls[key] = url
    assert yauss.urls[key] == url
    url += '/'
    yauss.urls[key] = url
    assert yauss.urls[key] == url
    del yauss.urls[key]
    assert not yauss.urls[key]

def test_add_scheme(yauss):
    key = 'abcdefgh'
    url = '127.0.0.1'
    yauss.urls[key] = url
    assert yauss.urls[key] == 'http://' + url