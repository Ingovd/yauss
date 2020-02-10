from .api import KeyAPI

class MongoKeys(KeyAPI):
    def __init__(self, mongo):
        super().__init__()
        self.db = mongo.db

    def approve_key(self, key):
        if self.db.keys.find_one({'my_key': key}):
            return False
        else:
            self.db.keys.insert_one({'my_key': key})
            return True
