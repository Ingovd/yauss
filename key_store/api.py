import abc
from random import choices


_chars = list(("abcdefghijklmnopqrstuvwxyz"
               "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               "0123456789-_"))


class KeyAPI():
    def request_keys(self, n):
        keys = []
        while len(keys) < n:
            key = self._generate_key()
            if self.approve_key(key):
                keys.append(key)
        return keys

    @abc.abstractmethod
    def approve_key(self, key: str):
        """ Check if key is present in the store """

    def _generate_key(self, k: int=8):
        return "".join(choices(_chars, k=k))
