from typing import Optional, List

from collections import namedtuple
from collections.abc import MutableMapping

from urllib.parse import urlparse


KeyUrl = namedtuple('KeyUrl', ['key', 'url'])


def format_url(long_url: str) -> Optional[str]:
    parsed_url = urlparse(long_url)
    if not parsed_url.scheme:
        parsed_url = urlparse(f"http://{long_url}")
    if parsed_url.netloc:
        return parsed_url.geturl()
    return None


class UrlAPI(MutableMapping):
    def __init__(self, db_backend):
        self.db_backend = db_backend

    def create_url(self, key: str, long_url: str) -> None:
        if long_url := format_url(long_url):
            self.insert_url(key, long_url)
        else:
            raise ValueError("Invalid URL.")

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
            return self.create_url(key, val)

    def __delitem__(self, key):
        return self.delete_url(key)

    def __iter__(self):
        yield from self.read_all_urls()

    def __len__(self):
        return self.count()
