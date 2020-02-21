from .api import *


class MongoUrls(UrlAPI):
    """ MongoDB backed implemementation of the URL API
    
    TODO: Catch errors thrown by PyMongo and propagate as custom Exception
    """
    
    def __init__(self, mongodb):
        super().__init__(mongodb)
        self.urls = mongodb.db.urls

    def insert_url(self, key: str, long_url: str) -> None:
        self.urls.insert_one({'key': key, 'long_url': long_url})

    def read_url(self, key: str) -> Optional[str]:
        if url := self.urls.find_one({'key': key}):
            return url['long_url']
        return None

    def read_all_urls(self) -> List[KeyUrl]:
        return [KeyUrl(url['key'], url['long_url'])
                for url in self.urls.find()]

    def update_url(self, key: str, long_url: str) -> None:
        self.urls.update_one(
            {'key': key}, {'$set': {'long_url': long_url}})

    def delete_url(self, key: str) -> None:
        if url := self.urls.find_one({'key': key}):
            self.urls.delete_one(url)

    def count(self) -> int:
        return self.urls.count_documents()
