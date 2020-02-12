import os

# Set server name and port
SERVER_NAME = 'localhost:5539'

# Supports: inmemory, sql, mongo
DB_BACKEND = 'sql'

# Setup SQLite database URI OS agnostic

# Will set SQLALCHEMY_DATABASE_URI to 'dialect:///relative/path/to/database.db'
SQLALCHEMY_DATABASE_URI = os.path.join(f"sqlite:///", '..', 'instance', 'key.db')

# flask_pymongo URI to MongoDB
MONGO_URI = 'mongodb://127.0.0.1:27017/keydb'

# Yauss key store URI
# If left blank starts local key store with DB_BACKEND
# KEY_STORE_URI = 'http://localhost:5000/keys'
