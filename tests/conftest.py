import os
import tempfile

import pytest

from yauss import create_app


@pytest.fixture
def app():
    with tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), 'tests')) as path:
        create_config(path)
        app = create_app({'INSTANCE_PATH': path})
        yield app

def create_config(path):
    config = ("TESTING=       True\n"
              "DB_BACKEND=    'inmemory'\n"
              "SERVER_NAME=   'localhost:5000'\n")
    with open(os.path.join(path, 'config.py'), "w") as configpy:
        configpy.write(config)

@pytest.fixture
def client(app):
    return app.test_client()