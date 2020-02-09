from contextlib import contextmanager
from .api import DatabaseAPI
from flask import current_app
from sqlalchemy import String, Boolean, Column
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Url(Base):
    __tablename__ = 'urls'
    my_key = Column(String(8), primary_key=True)
    long_url = Column(String(), nullable=False)

    def __repr__(self):
        return f"<url {self.my_key}={self.long_url}>"

class Key(Base):
    __tablename__ = 'keys'
    my_key = Column(String(8), primary_key=True)
    used = Column(Boolean(), default=False)

    def __repr__(self):
        return f"<key {self.my_key}={self.used}>"

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

class SqlAPI(DatabaseAPI):
    def __init__(self, sqldb):
        super().__init__()
        self.db = sqldb
        Base.metadata.create_all(bind=self.db.engine)

    @with_scoped_session
    def create_url(self, long_url, key=None, session=None):
        key = self.consume_key(key)
        new_url = Url(my_key=key, long_url=long_url)
        session.add(new_url)

    @with_scoped_session
    def read_url_or_404(self, key, session=None):
        url_object = session.query(Url).get_or_404(key)
        return {'my_key': url_object.my_key, 'long_url': url_object.long_url}

    @with_scoped_session
    def read_all_urls(self, session=None):
        urls = session.query(Url).all()
        urls = list(map(lambda url: {'my_key': url.my_key, 'long_url': url.long_url}, urls))
        return list(urls)

    @with_scoped_session
    def update_url(self, key, long_url, session=None):
        url_object = session.query(Url).get_or_404(key)
        url_object.long_url = long_url
      
    @with_scoped_session  
    def delete_url(self, key, session=None):
        url_object = session.query(Url).get_or_404(key)
        session.delete(url_object)

    @with_scoped_session
    def bulk_generate_keys(self, n=10, session=None):
        new_keys = []
        for i in range(n):
            new_keys.append(Key(my_key=self.generate_key()))

        session.bulk_save_objects(new_keys)

    @with_scoped_session
    def insert_key(self, key, session=None):
        new_key = Key(my_key=key, used=True)
        session.add(new_key)
        return new_key

    @with_scoped_session
    def consume_key(self, key, session=None):
        if key is None:
            new_key = session.query(Key).filter_by(used=False).first()
        else:
            new_key = self.insert_key(key)
        if new_key is None:
            self.bulk_generate_keys()
            new_key = session.query(Key).filter_by(used=False).first()
        new_key.used = True
        return new_key.my_key