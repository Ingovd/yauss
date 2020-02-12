import os

# Set server name and port
SERVER_NAME = 'localhost:5000'

# Supports: inmemory, sql, mongo
DB_BACKEND = 'inmemory'

# Setup SQLite database URI OS agnostic

# Will set SQLALCHEMY_DATABASE_URI to 'dialect:///relative/path/to/database.db'
relative_url_db = ['..', 'instance', 'url.db']
SQLALCHEMY_DATABASE_URI = os.path.join(f"sqlite:///", *relative_url_db)

# Key store database if no external key store is used
relative_key_db = ['..', 'instance', 'key.db']
SQLALCHEMY_BINDS = {
  'key_store' :  os.path.join(f"sqlite:///", *relative_key_db)
}


# flask_pymongo URI to MongoDB
MONGO_URI = 'mongodb://127.0.0.1:27017/urldb'

# Yauss key store URI
# If left blank starts local key store with DB_BACKEND
# KEY_STORE_URI = 'http://localhost:5000/keys'

# flask_caching configuration
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 86400
CACHE_KEY_REFILL = 10