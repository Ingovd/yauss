from flask import current_app as app

class DatabaseAPI:
    def __init__(self, app):
        app.db_api = self

    def create_url(self, key, long_url):
        raise NotImplementedError

    def read_url_or_404(self, key):
        raise NotImplementedError

    def read_all_urls(self):
        raise NotImplementedError

    def update_url(self, key, long_url):
        raise NotImplementedError
        
    def delete_url(self, key):
        raise NotImplementedError
