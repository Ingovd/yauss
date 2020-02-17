from .api import *


class MongoAPI(DatabaseAPI):
    def __init__(self, mongodb):
        super().__init__(mongodb)
        self.urls = mongodb.db.urls

    def insert_url(self, key, long_url):
        self.urls.insert_one({'my_key': key, 'long_url': long_url})

    def read_url(self, key):
        if url := self.urls.find_one({'my_key': key}):
            return url['long_url']

    def read_all_urls(self):
        return [KeyUrl(url['my_key'], url['long_url'])
                for url in self.urls.find()]

    def update_url(self, key, long_url):
        self.urls.update_one(
            {'my_key': key}, {'$set': {'long_url': long_url}})

    def delete_url(self, key):
        if url := self.urls.find_one({'my_key': key}):
            self.urls.delete_one(url)
