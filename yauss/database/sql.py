from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import String, Column
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base

from .api import DatabaseAPI


Base = declarative_base()


class Url(Base):
    __tablename__ = 'urls'
    my_key = Column(String(8), primary_key=True)
    long_url = Column(String(), nullable=False)

    def __repr__(self):
        return f"<url {self.my_key}={self.long_url}>"


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
    def __init__(self, app):
        sql = SQLAlchemy()
        sql.init_app(app)
        self.db = sql
        Base.metadata.create_all(bind=self.db.engine)
        super().__init__(app)

    @with_scoped_session
    def create_url(self, key, long_url, session=None):
        new_url = Url(my_key=key, long_url=long_url)
        session.add(new_url)

    @with_scoped_session
    def read_url_or_404(self, key, session=None):
        url = session.query(Url).get_or_404(key)
        return {'my_key': url.my_key, 'long_url': url.long_url}

    @with_scoped_session
    def read_all_urls(self, session=None):
        urls = session.query(Url).all()
        urls = [{'my_key': url.my_key, 'long_url': url.long_url}
                for url in urls]
        return list(urls)

    @with_scoped_session
    def update_url(self, key, long_url, session=None):
        url = session.query(Url).get_or_404(key)
        url.long_url = long_url

    @with_scoped_session
    def delete_url(self, key, session=None):
        url = session.query(Url).get_or_404(key)
        session.delete(url)
