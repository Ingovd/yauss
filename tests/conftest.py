import os
import tempfile

import pytest

from flask import message_flashed

from key_store import create_app as create_key_store

from yauss import (url_inits,
                   create_app as create_yauss)
from yauss.key_gateway import KeyStoreError



class MockKey():
    def __init__(self, fail=False):
        self.fail = fail

    def consume(self):
        if self.fail:
            raise KeyStoreError("Mock error")
        return 'abcdefgh'


@pytest.fixture(params=['sql', ''])
def path(request):
    with tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), 'tests')) as path:
        sqldb = 'sqlite:///' + os.path.join(path, 'url.db')
        config = '\n'.join([
                       "TESTING=       True",
                      f"DB_BACKEND=    '{request.param}'",
                      f"SQLALCHEMY_DATABASE_URI = {repr(sqldb)}",
                       "SERVER_NAME=   'localhost:5000'",
                       "SECRET_KEY=    'sososecretn'",
                       "CACHE_TYPE=    'simple'"])
        with open(os.path.join(path, 'config.py'), "w") as configpy:
            configpy.write(config)
        yield path


@pytest.fixture
def yauss(path):
    yauss = create_yauss({'INSTANCE_PATH': path, 'KEY_STORE_URI': 'mock'})
    with yauss.app_context():
        yauss.keys = MockKey()
        yield yauss


@pytest.fixture
def yauss_key(path):
    yauss = create_yauss({'INSTANCE_PATH': path})
    yauss.keys.get = yauss.test_client().get
    yauss.keys.json = lambda response : response.json
    with yauss.app_context():
        yield yauss


@pytest.fixture
def key_client(yauss_key):
    return yauss_key.test_client()


@pytest.fixture
def yauss_client(yauss):
    return yauss.test_client()


@pytest.fixture
def key_store(path):
    key_store = create_key_store({'INSTANCE_PATH': path})
    return key_store

# @pytest.fixture(params=['sql', 'inmemory'])
# def urls(request):
#     print(request.param)
#     url_init = url_inits[request.param]
#     db_backend = url_init['backend']()
#     urls = url_init['api'](db_backend)
#     return urls