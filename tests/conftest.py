import os
import tempfile

import pytest

from flask import message_flashed

from yauss import (url_inits,
                   create_app as create_yauss)
from key_store import create_app as create_key_store


class MockKey():
    def consume_key(self):
        return 'abcdefgh'


@pytest.fixture(params=['sql', 'inmemory'])
def path(request):
    with tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), 'tests')) as path:
        config = ( "TESTING=       True\n"
                  f"DB_BACKEND=    '{request.param}'\n"
                   "SERVER_NAME=   'localhost:5000'\n"
                   "SECRET_KEY=    'sososecret'\n"
                   "KEY_STORE_URI= 'mock'")
        with open(os.path.join(path, 'config.py'), "w") as configpy:
            configpy.write(config)
        yield path


@pytest.fixture
def yauss(path):
    yauss = create_yauss({'INSTANCE_PATH': path})
    with yauss.app_context():
        yauss.key_gateway = MockKey()
        yield yauss


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