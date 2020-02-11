from .api import DatabaseAPI
from flask import abort

class InMemoryAPI(DatabaseAPI):
    def __init__(self, app):
        self.urls = {}
        super().__init__(app)

    def create_url(self, key, long_url):
        self.urls[key] = long_url

    def read_url_or_404(self, key):
        try:
            return {'my_key': key, 'long_url': self.urls[key]}
        except KeyError:
            abort(404)

    def read_all_urls(self):
        urls = [{'my_key': key, 'long_url': long_url}
                for key, long_url in self.urls.items()]
        return list(urls)

    def update_url(self, key, long_url):
        self.urls[key] = long_url
        
    def delete_url(self, key):
        del self.urls[key]
