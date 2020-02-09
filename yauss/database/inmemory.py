from .api import DatabaseAPI
from flask import abort

class InMemoryDB(DatabaseAPI):
    def __init__(self, database):
        super().__init__()
        self.db = database.db

    def create_url(self, long_url, key=None):
        key = self.consume_key(key)
        self.db[key] = long_url

    def read_url_or_404(self, key):
        try:
            return {'my_key': key, 'long_url': self.db[key]}
        except KeyError:
            abort(404)

    def read_all_urls(self):
        urls = [{'my_key': key, 'long_url': long_url} for key, long_url in self.db.items()]
        return list(urls)

    def update_url(self, key, long_url):
        self.db[key] = long_url
        
    def delete_url(self, key):
        del self.db[key]

    def bulk_generate_keys(self, n=10):
        pass

    def insert_key(self, key):
        pass

    def consume_key(self, key):
        return self.generate_key()