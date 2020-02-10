from .api import KeyAPI
from flask import abort

class InMemoryKeys(KeyAPI):
    def __init__(self, data):
        super().__init__()
        self.keys = data.keys

    def request_keys(self, n):
        keys = []
        while len(keys) < n:
            key = self._generate_key()
            if self.approve_key(key):
                keys.append(key)
        return keys

    def approve_key(self, key):
        if key in self.keys:
            return False
        else:
            self.keys.add(key)
            return True