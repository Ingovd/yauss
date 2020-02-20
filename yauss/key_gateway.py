from requests import get
from requests.exceptions import ConnectionError

from flask import abort


class KeyStoreError(Exception):
    def __init__(self, message='Generic key store error'):
        super().__init__(message)


class KeyGateway():
    def __init__(self, address, cache_refill=10):
        super().__init__()
        self.key_cache = set()
        self.address = address
        self.refill = cache_refill

    def _request_keys(self, n):
        response = get(f"{self.address}/request/{n}")
        if response:
            return response.json()['keys']
        else:
            msg = f"Requesting {n} keys response: {response.status_code}"
            raise KeyStoreError(msg)

    def _approve_key(self, key):
        response = get(f"{self.address}/{key}")
        if response:
            return response.json()['approved']
        else:
            msg = f"Approving {key} response: {response.status_code}"
            raise KeyStoreError(msg)

    def _get_key(self):
        try:
            key = self.key_cache.pop()
        except KeyError:
            key = self._get_remote_key()
        return key

    def _get_remote_key(self):
        if keys := self._request_keys(self.refill):
            self.key_cache.update(keys[1:])
            return keys[0]
        raise KeyStoreError("Received zero keys from store")
        

    def consume(self, key=None):
        try:
            if key is None:
                return self._get_key()
            elif self._approve_key(key):
                return key
        except ConnectionError as err:
            app.logger.error(APP_KEY_1ERR.format(err))
            raise KeyStoreError("Connection error with key store")
        return None
