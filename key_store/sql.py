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
    def __init__(self, sqldb):
        super().__init__()
        self.db = sqldb
        Base.metadata.create_all(bind=self.db.engine)

    @with_scoped_session
    def approve_key(self, key):
        if session.query(Key).get(key):
            return False
        else:
            session.add(Key(my_key=key))
            return True
