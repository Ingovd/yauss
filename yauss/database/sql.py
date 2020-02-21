from contextlib import contextmanager

from sqlalchemy import String, Column
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base

from .api import *


Base = declarative_base()


class Url(Base):
    """ SQLAlchemy schema """

    __tablename__ = 'urls'
    key = Column(String(8), primary_key=True)
    long_url = Column(String(), nullable=False)


@contextmanager
def scoped_session(db):
    """ Creates a SQLAlchemy database transaction """

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
    """ Decorator to add a scoped session 
    
    The decorated function must be a class method of a class with access
    to an SQLAlchemy database object, as well as take a session parameter.
    """

    def wrapper(self, *args, **kwargs):
        with scoped_session(self.db) as session:
            return func(self, *args, **dict(kwargs, session=session))
    return wrapper


class SqlUrls(UrlAPI):
    """ SQLAlchemy backed implementation or the URL API """
    
    def __init__(self, sqldb):
        super().__init__(sqldb)
        self.db = sqldb
        Base.metadata.create_all(bind=self.db.engine)

    @with_scoped_session
    def insert_url(self, key: str, long_url: str, session=None) -> None:
        new_url = Url(key=key, long_url=long_url)
        session.add(new_url)

    @with_scoped_session
    def read_url(self, key: str, session=None) -> Optional[str]:
        if url := session.query(Url).get(key):
            return url.long_url
        return None

    @with_scoped_session
    def read_all_urls(self, session=None):
        return [KeyUrl(url.key, url.long_url)
                for url in session.query(Url).all()]

    @with_scoped_session
    def update_url(self, key: str, long_url: str, session=None) -> None:
        if url := session.query(Url).get(key):
            url.long_url = long_url

    @with_scoped_session
    def delete_url(self, key: str, session=None) -> None:
        if url := session.query(Url).get(key):
            session.delete(url)

    @with_scoped_session
    def count(self, session=None) -> int:
        return session.query(Url).count()
