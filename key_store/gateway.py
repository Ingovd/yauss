import json

from requests import get

from flask import abort

from .api import KeyAPI

class GatewayKeys(KeyAPI):
    def __init__(self, address):
        super().__init__()
        self.address = address

    def request_keys(self, n):
        response = get(f"{self.address}/request/{n}")
        if response:
            return json.loads(response.content)['keys']
        else:
            abort(response.status_code)

    def approve_key(self, key):
        response = get(f"{self.address}/{key}")
        if response:
            return json.loads(response.content)['approved']
        else:
            abort(response.status_code)
        