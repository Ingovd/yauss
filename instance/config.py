import os


## Domain the service is running at

SERVER_NAME = 'localhost:5000'


## Supports: mongo, sql, inmemory(default)

DB_BACKEND = 'sql'


## Setup SQLite database URI if DB_BACKEND='sql'

# Will set SQLALCHEMY_DATABASE_URI to 'dialect:///relative/path/to/database.db'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join('..', 'instance', 'url.db')


## flask_pymongo URI to MongoDB if DB_BACKEND='mongo

MONGO_URI = 'mongodb://127.0.0.1:27017/urldb'


## Yauss key store URI

# If left blank starts local key store with DB_BACKEND
# KEY_STORE_URI = 'http://keystore.com'

# Number of keys to request from store if cache is empty
CACHE_KEY_REFILL = 10


## flask_caching configuration

# Supports: simple, redis (UNTESTED)
CACHE_TYPE = 'simple'

# Set if CACHE_TYPE=redis
# CACHE_REDIS_URL = redis://user:password@localhost:6379/2

# Default time key-URL pairs are cached
CACHE_DEFAULT_TIMEOUT = 86400


## flask sesssion

# Change to your own secret to support secure sessions
SECRET_KEY = b'replacewithsecret'
