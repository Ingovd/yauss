from random import choices

class KeyAPI():
    def __init__(self):
        self._chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

    def request_keys(self, n):
        keys = []
        while len(keys) < n:
            key = self._generate_key()
            if self.approve_key(key):
                keys.append(key)
        return keys

    def approve_key(self, key):
        raise NotImplementedError

    def _generate_key(self, k=8):
        return "".join(choices(self._chars, k=k))
