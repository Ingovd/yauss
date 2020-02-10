from flask import current_app as app

class DatabaseAPI:
    def __init__(self):
        self.key_cache = set()

    def consume_key(self, key):
        if key is None:
            return self.get_cached_key()
        elif app.key_api.approve_key(key):
            return key
        raise Exception(f"Could not consume key: {key}")

    def get_cached_key(self):
        key = None
        while key is None:
            try:
                key = self.key_cache.pop()
                return key
            except KeyError:
                self.refill_key_cache()

    def refill_key_cache(self):
        keys = app.key_api.request_keys(3)
        self.key_cache.update(keys)

    def create_url(self, long_url, key=None):
        raise NotImplementedError

    def read_url_or_404(self, key):
        raise NotImplementedError

    def read_all_urls(self):
        raise NotImplementedError

    def update_url(self, key, long_url):
        raise NotImplementedError
        
    def delete_url(self, key):
        raise NotImplementedError