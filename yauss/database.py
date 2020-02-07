import sys

from random import choices
from flask import current_app
from . import mongo

_chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

def create_url(long_url, key_string=None):
    if key_string is None:
        new_key = consume_key()
    else:
        new_key = insert_key(key_string)

    mongo.db.urls.insert_one({'my_key': new_key['my_key'],'long_url': long_url})

def read_url_or_404(my_key):
    return mongo.db.urls.find_one_or_404({'my_key': my_key})

def read_all_urls():
    return mongo.db.urls.find()

def update_url(my_key, long_url):
    mongo.db.urls.update_one({'my_key': my_key}, {'$set': {'long_url': long_url}})
    
def delete_url(my_key):
    url = mongo.db.urls.find_one_or_404({'my_key': my_key})
    mongo.db.urls.delete_one(url)

def generate_key(k=8):
    return "".join(choices(_chars, k=k))

def bulk_generate_keys(n=10):
    new_keys = []
    for i in range(n):
        new_keys.append({'my_key': generate_key(), 'used': False})

    mongo.db.keys.insert_many(new_keys)

def insert_key(new_key):
    new_key = {'my_key': new_key,'used': True}
    mongo.db.keys.insert_one(new_key)
    return new_key

def consume_key():
    new_key = mongo.db.keys.find_one({'used': False})
    if new_key is None:
        bulk_generate_keys()
        new_key = mongo.db.keys.find_one_or_404({'used': False})
    mongo.db.keys.update_one({'my_key': new_key['my_key']}, {'$set': {'used': True}})
    return new_key