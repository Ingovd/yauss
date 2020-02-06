from random import choices
from models import Key

_chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

def generate(k=8):
    return "".join(choices(_chars, k=k))

def bulk_insert(session, n=10):
    new_keys = []
    for i in range(n):
        new_keys.append(Key(my_key=generate()))

    session.bulk_save_objects(new_keys)

def consume_key(session):
    new_key = session.query(Key).filter_by(used=False).first()
    if new_key is None:
        bulk_insert(session)
        new_key = session.query(Key).filter_by(used=False).first()
    new_key.used = True
    return new_key