from .api import KeyAPI


class InMemoryKeys(KeyAPI):
    def __init__(self, memdb):
        super().__init__()
        self.keys = memdb.keys

    def approve_key(self, key):
        if key in self.keys:
            return False
        else:
            self.keys.add(key)
            return True
