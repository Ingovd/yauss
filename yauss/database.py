from random import choices

_chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

class MongoAPI:
    def __init__(self, mongo):
        self.mongo = mongo
        self.db = mongo.db

    def create_url(self, long_url, key_string=None):
        if key_string is None:
            new_key = self.consume_key()
        else:
            new_key = self.insert_key(key_string)

        self.db.urls.insert_one({'my_key': new_key['my_key'],'long_url': long_url})

    def read_url_or_404(self, my_key):
        return self.db.urls.find_one_or_404({'my_key': my_key})

    def read_all_urls(self):
        return self.db.urls.find()

    def update_url(self, my_key, long_url):
        self.db.urls.update_one({'my_key': my_key}, {'$set': {'long_url': long_url}})
        
    def delete_url(self, my_key):
        url = self.db.urls.find_one_or_404({'my_key': my_key})
        self.db.urls.delete_one(url)

    def generate_key(self, k=8):
        return "".join(choices(_chars, k=k))

    def bulk_generate_keys(self, n=10):
        new_keys = []
        for i in range(n):
            new_keys.append({'my_key': generate_key(), 'used': False})

        self.db.keys.insert_many(new_keys)

    def insert_key(self, new_key):
        new_key = {'my_key': new_key,'used': True}
        self.db.keys.insert_one(new_key)
        return new_key

    def consume_key(self):
        new_key = self.db.keys.find_one({'used': False})
        if new_key is None:
            self.bulk_generate_keys()
            new_key = self.db.keys.find_one_or_404({'used': False})
        self.db.keys.update_one({'my_key': new_key['my_key']}, {'$set': {'used': True}})
        return new_key