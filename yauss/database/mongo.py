from .api import DatabaseAPI

class MongoAPI(DatabaseAPI):
    def __init__(self, mongo):
        super().__init__()
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
        self.db.urls.update_one(
            {'my_key': key}, {'$set': {'long_url': long_url}})
        
    def delete_url(self, key):
        url = self.db.urls.find_one_or_404({'my_key': key})
        self.db.urls.delete_one(url)
