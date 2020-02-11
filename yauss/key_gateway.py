import json

from requests import get

from flask import abort


class KeyGateway():
    def __init__(self, address, cache_refill=10):
        super().__init__()
        self.key_cache = set()
        self.address = address
        self.cache_refill = cache_refill

    def _request_keys(self, n):
        response = get(f"{self.address}/request/{n}")
        if response:
            return json.loads(response.content)['keys']
        else:
            abort(response.status_code)

    def _approve_key(self, key):
        response = get(f"{self.address}/{key}")
        if response:
            return json.loads(response.content)['approved']
        else:
            abort(response.status_code)

    def _get_cached_key(self):
        key = None
        while key is None:
            try:
                key = self.key_cache.pop()
                return key
            except KeyError:
                self._refill_key_cache()

    def _refill_key_cache(self):
        keys = self._request_keys(self.cache_refill)
        self.key_cache.update(keys)

    def consume_key(self, key=None):
        if key is None:
            return self._get_cached_key()
        elif self._approve_key(key):
            return key
        raise KeyError(f"{key} already in use.")
