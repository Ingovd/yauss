from contextlib import contextmanager

from sqlalchemy import String, Column
from sqlalchemy.ext.declarative import declarative_base

from .api import KeyAPI


Base = declarative_base()


@contextmanager
def scoped_session(db):
    session = db.create_scoped_session()
    try:
        yield session
        session.commit()
    except DatabaseError as err:
        print(f"Error in scoped session: {err}")
        session.rollback()
    finally:
        session.close()


def with_scoped_session(func):
    def wrapper(self, *args, **kwargs):
        with scoped_session(self.db) as session:
            return func(self, *args, **dict(kwargs, session=session))
    return wrapper


class Key(Base):
    __tablename__ = 'keys'
    key = Column(String(8), primary_key=True)

    def __repr__(self):
        return f"<key {self.key}>"


class SqlKeys(KeyAPI):
    def __init__(self, sqldb):
        super().__init__()
        Base.metadata.create_all(bind=sqldb.engine)
        self.db = sqldb

    @with_scoped_session
    def approve_key(self, key, session=None):
        if session.query(Key).get(key):
            return False
        else:
            session.add(Key(key=key))
            return True
