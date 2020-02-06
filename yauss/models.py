from contextlib import contextmanager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Url(db.Model):
    my_key = db.Column(db.String(8), primary_key=True)
    long_url = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<url {self.my_key}={self.long_url}>"

class Key(db.Model):
    my_key = db.Column(db.String(8), primary_key=True)
    used = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<key {self.my_key}={self.used}>"


def with_scoped_session(func):
    def wrapper(*args, **kwargs):
        with scoped_session() as session:
            return func(*args, **dict(kwargs, session=session))
    return wrapper

@contextmanager
def scoped_session():
    session = db.create_scoped_session()
    try:
        yield session
        session.commit()
    except Exception as err:
        print(f"Error in scoped session: {err}")
        session.rollback()
    finally:
        session.close()