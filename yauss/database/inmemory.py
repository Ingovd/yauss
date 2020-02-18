from .api import *
from flask import abort

class InMemoryDB():
    def __init__(self, urldict={}, keyset=set()):
        self.urls = urldict
        self.keys = keyset
    
    def init_app(self, app):
        pass

class InMemoryUrls(UrlAPI):
    def __init__(self, memdb):
        super().__init__(memdb)
        self.urls = memdb.urls

    def insert_url(self, key: str, long_url: str) -> None:
        self.urls[key] = long_url

    def read_url(self, key: str) -> Optional[str]:
        return self.urls.get(key)

    def read_all_urls(self) -> List[KeyUrl]:
        return [KeyUrl(key, long_url)
                for key, long_url in self.urls.items()]

    def update_url(self, key: str, long_url: str) -> None:
        self.urls[key] = long_url

    def delete_url(self, key: str) -> None:
        del self.urls[key]
    
    def count(self) -> int:
        return self.urls.count
