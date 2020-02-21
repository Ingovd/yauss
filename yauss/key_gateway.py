from typing import Optional, List

from requests import get as http_get

from requests.exceptions import ConnectionError

from flask import abort


class KeyStoreError(Exception):
    """ Exception to be caught by users of KeyGateway """

    def __init__(self, message='Generic key store error'):
        super().__init__(message)


class KeyGateway():
    """ Gateway to receive keys from a key store and cache for later use.
    
    The members get and json are used to send requests and parse the response.

    TODO: Implement thread safe circular buffer for key_cache.
    TODO: Make exception handling consistent with the rest of the project
    """

    def __init__(self, address, cache_refill=10):
        super().__init__()
        self.key_cache = set()
        self.get = http_get
        self.json = lambda response: response.json()
        self.address = address
        self.refill = cache_refill

    def consume(self, key: Optional[str]=None) -> Optional[str]:
        """ Only method of the key gateway api: used to acquire a unique key

        Will either check the key store for key, or consume a key from cache.
        If the cache is empty, it will request more keys from the external
        store and refill the cache with the any superfluous keys received.
        """

        try:
            if key is None:
                return self._get_key()
            elif self._approve_key(key):
                return key
        except ConnectionError as err:
            app.logger.error(APP_KEY_1ERR.format(err))
            raise KeyStoreError("Connection error with key store")
        return None

    def _get_key(self) -> str:
        try:
            key = self.key_cache.pop()
        except KeyError:
            key = self._get_remote_key()
        return key

    def _get_remote_key(self) -> str:
        if keys := self._request_keys(self.refill):
            self.key_cache.update(keys[1:])
            return keys[0]
        raise KeyStoreError("Received zero keys from store")

    def _request_keys(self, n: int) -> List[str]:
        response = self.get(f"{self.address}/request/{n}")
        if response:
            return self.json(response)['keys']
        else:
            msg = f"Requesting {n} keys response: {response.status_code}"
            raise KeyStoreError(msg)

    def _approve_key(self, key: str) -> bool:
        response = self.get(f"{self.address}/approve/{key}")
        if response:
            return self.json(response)['approved']
        else:
            msg = f"Approving {key} response: {response.status_code}"
            raise KeyStoreError(msg)
