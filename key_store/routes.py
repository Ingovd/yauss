from flask import (Blueprint,
                   jsonify,
                   current_app as app)

key_store = Blueprint('key_store', __name__)

@key_store.route('/request/<int:n>')
def handle_request_keys(n):
    keys = app.api.request_keys(n)
    return jsonify({'keys': keys})

@key_store.route('/<key>')
def approve_key(key):
    approved = app.api.approve_key(key)
    return jsonify({'approved': approved})