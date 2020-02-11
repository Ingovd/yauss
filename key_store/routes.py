from flask import (Blueprint,
                   jsonify,
                   current_app as app)


key_store_routes = Blueprint('key_store_routes', __name__)


@key_store_routes.route('/request/<int:n>')
def handle_request_keys(n):
    keys = app.key_store.request_keys(n)
    return jsonify({'keys': keys})


@key_store_routes.route('/approve/<key>')
def approve_key(key):
    print(f"Approving key: {key}")
    approved = app.key_store.approve_key(key)
    return jsonify({'approved': approved})
