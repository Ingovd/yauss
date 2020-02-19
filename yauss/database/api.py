from typing import Optional, List

from collections import namedtuple
from collections.abc import MutableMapping


KeyUrl = namedtuple('KeyUrl', ['key', 'url'])


class UrlAPI(MutableMapping):
    def __init__(self, db_backend):
        self.db_backend = db_backend

    def insert_url(self, key: str, long_url: str) -> None:
        raise NotImplementedError

    def read_url(self, key: str) -> Optional[str]:
        raise NotImplementedError

    def read_all_urls(self) -> List[KeyUrl]:
        raise NotImplementedError

    def update_url(self, key: str, long_url: str) -> None:
        raise NotImplementedError

    def delete_url(self, key: str) -> None:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

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
