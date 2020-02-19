import os

# Domain the service is running at
SERVER_NAME = 'localhost:5000'

# Supports: sql, mongo
# Leave blank for testing with in memory database
# DB_BACKEND = 'mongo'

# Setup SQLite database URI if DB_BACKEND='sql'
# Will set SQLALCHEMY_DATABASE_URI to 'dialect:///relative/path/to/database.db'
SQLALCHEMY_DATABASE_URI = os.path.join(f"sqlite:///", '..', 'instance', 'url.db')

# flask_pymongo URI to MongoDB if DB_BACKEND='mongo
MONGO_URI = 'mongodb://127.0.0.1:27017/urldb'

# Yauss key store URI
# If left blank starts local key store with DB_BACKEND
# KEY_STORE_URI = 'http://keystore.com'
# Number of keys to request from store if cache is empty
CACHE_KEY_REFILL = 10

# flask_caching configuration
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 86400


# flask sesssion
SECRET_KEY = b'replacewithsecret'
