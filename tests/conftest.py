import os
import tempfile

import pytest

from flask import message_flashed

from yauss import create_app


class MockKey():
    def consume_key(self):
        return 'abcdefgh'


@pytest.fixture
def app():
    with tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), 'tests')) as path:
        create_config(path)
        app = create_app({'INSTANCE_PATH': path})
        with app.app_context():
            create_mock_key_gateway(app)
        yield app

def create_mock_key_gateway(app):
    app.key_gateway = MockKey()

def create_config(path):
    config = ("TESTING=       True\n"
              "DB_BACKEND=    'inmemory'\n"
              "SERVER_NAME=   'localhost:5000'\n"
              "SECRET_KEY=    'sososecret'\n"
              "KEY_STORE_URI= 'mock'")
    with open(os.path.join(path, 'config.py'), "w") as configpy:
        configpy.write(config)

@pytest.fixture
def client(app):
    return app.test_client()