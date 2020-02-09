from .api import DatabaseAPI

class MongoAPI(DatabaseAPI):
    def __init__(self, mongo):
        super().__init__()
        self.mongo = mongo
        self.db = mongo.db

    def create_url(self, long_url, key=None):
        key = self.consume_key(key)
        self.db.urls.insert_one({'my_key': key,'long_url': long_url})

    def read_url_or_404(self, key):
        url_object = self.db.urls.find_one_or_404({'my_key': key})
        return url_object

    def read_all_urls(self):
        urls = self.db.urls.find()
        return list(urls)

    def update_url(self, key, long_url):
        self.db.urls.update_one({'my_key': key}, {'$set': {'long_url': long_url}})
        
    def delete_url(self, key):
        url = self.db.urls.find_one_or_404({'my_key': key})
        self.db.urls.delete_one(url)

    def bulk_generate_keys(self, n=10):
        new_keys = []
        for i in range(n):
            new_keys.append({'my_key': generate_key(), 'used': False})

        self.db.keys.insert_many(new_keys)

    def insert_key(self, key):
        new_key = {'my_key': key,'used': True}
        self.db.keys.insert_one(new_key)
        return new_key

    def consume_key(self, key):
        if key is None:
            new_key = self.db.keys.find_one({'used': False})
        else:
            new_key = self.insert_key(key)
        if new_key is None:
            self.bulk_generate_keys()
            new_key = self.db.keys.find_one_or_404({'used': False})
        self.db.keys.update_one({'my_key': new_key['my_key']}, {'$set': {'used': True}})
        return new_key['my_key']