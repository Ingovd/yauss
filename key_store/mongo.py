from .api import KeyAPI


class MongoKeys(KeyAPI):
    def __init__(self, mongodb):
        super().__init__()
        self.keys = mongodb.db.keys

    def approve_key(self, key):
        if self.keys.find_one({'my_key': key}):
            return False
        else:
            self.keys.insert_one({'my_key': key})
            return True
