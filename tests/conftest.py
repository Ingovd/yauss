import os
import tempfile

import pytest

from flask import message_flashed

from yauss import create_app as create_yauss
from key_store import create_app as create_key_store


class MockKey():
    def consume_key(self):
        return 'abcdefgh'


@pytest.fixture(scope='class')
def path():
    with tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), 'tests')) as path:
        config = ("TESTING=       True\n"
                  "DB_BACKEND=    'inmemory'\n"
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
    return yauss


@pytest.fixture
def yauss_client(yauss):
    return yauss.test_client()


@pytest.fixture
def key_store(path):
    key_store = create_key_store({'INSTANCE_PATH': path})
    return key_store




