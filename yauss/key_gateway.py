import json

from requests import get
from requests.exceptions import ConnectionError

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
            keys = json.loads(response.content)['keys']
        else:
            abort(response.status_code)
        if len(keys) > 0:
            return keys
        else:
            abort(503)

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
            except KeyError:
                key = self._refill_key_cache()
        return key

    def _refill_key_cache(self):
        keys = self._request_keys(self.cache_refill)
        self.key_cache.update(keys[1:])
        return keys[0]

    def consume_key(self, key=None):
        try:
            if key is None:
                return self._get_cached_key()
            elif self._approve_key(key):
                return key
        except ConnectionError:
            raise TimeoutError("Could not get a valid response from key store")
        raise ValueError("Could not validate the key")
