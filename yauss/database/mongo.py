from flask_pymongo import PyMongo

from .api import DatabaseAPI


class MongoAPI(DatabaseAPI):
    def __init__(self, app):
        self.db = PyMongo()
        self.db.init_app(app)
        super().__init__(app)
        self.urls = self.db.db.urls

    def create_url(self, key, long_url):
        self.urls.insert_one({'my_key': key, 'long_url': long_url})

    def read_url_or_404(self, key):
        url_object = self.urls.find_one_or_404({'my_key': key})
        return url_object

    def read_all_urls(self):
        urls = self.urls.find()
        return list(urls)

    def update_url(self, key, long_url):
        self.urls.update_one(
            {'my_key': key}, {'$set': {'long_url': long_url}})

    def delete_url(self, key):
        url = self.urls.find_one_or_404({'my_key': key})
        self.urls.delete_one(url)
