from random import choices

class KeyAPI():
    def __init__(self):
        self._chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

    def _generate_key(self, k=8):
        return "".join(choices(self._chars, k=k))

    def request_keys(self, n):
        raise NotImplementedError

    def approve_key(self, key):
        raise NotImplementedError