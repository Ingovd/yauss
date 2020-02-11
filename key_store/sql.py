from sqlalchemy import String, Column
from sqlalchemy.ext.declarative import declarative_base

from yauss.database.sql import with_scoped_session

from .api import KeyAPI


Base = declarative_base()


class Key(Base):
    __tablename__ = 'keys'
    my_key = Column(String(8), primary_key=True)

    def __repr__(self):
        return f"<key {self.my_key}>"


class SqlKeys(KeyAPI):
    def __init__(self, sql):
        super().__init__()
        Base.metadata.create_all(bind=sql.engine)
        self.db = sql

    @with_scoped_session
    def approve_key(self, key, session=None):
        if session.query(Key).get(key):
            return False
        else:
            session.add(Key(my_key=key))
            return True
