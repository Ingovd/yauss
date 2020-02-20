import abc

from typing import Optional, List

from collections import namedtuple
from collections.abc import MutableMapping


KeyUrl = namedtuple('KeyUrl', ['key', 'url'])


class UrlAPI(MutableMapping):
    def __init__(self, db_backend):
        self.db_backend = db_backend

    @abc.abstractmethod
    def insert_url(self, key: str, long_url: str) -> None:
        """ Insert long_url in the database backend with new key """

    @abc.abstractmethod
    def read_url(self, key: str) -> Optional[str]:
        """ Retrieve url with key, returns None if key does not exist. """

    @abc.abstractmethod
    def read_all_urls(self) -> List[KeyUrl]:
        """ Returns *all* url-key pairs in the database backend"""

    @abc.abstractmethod
    def update_url(self, key: str, long_url: str) -> None:
        """ Updates existing key with new url """

    @abc.abstractmethod
    def delete_url(self, key: str) -> None:
        """ Deletes key from database backend if it exists"""

    @abc.abstractmethod
    def count(self) -> int:
        """ Returns the number of key-url pairs in the database backend """

    def __getitem__(self, key):
        return self.read_url(key)

    def __setitem__(self, key, val):
        if self[key]:
            return self.update_url(key, val)
        else:
            return self.insert_url(key, val)

    def __delitem__(self, key):
        return self.delete_url(key)

    def __iter__(self):
        yield from self.read_all_urls()

    def __len__(self):
        return self.count()
