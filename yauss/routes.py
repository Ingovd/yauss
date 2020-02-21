from typing import Callable, Optional

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   abort,
                   flash,
                   current_app as app)

from .key_gateway import KeyStoreError

from .templates.messages import *


url_crud = Blueprint('url_crud', __name__, template_folder='templates')


def commit_url(get_key: Callable[...,str], unsafe_url: str) -> Optional[str]:
    if not (long_url := app.format_url(unsafe_url)):
        flash(USR_INVALID_URL)
        return None
    try:
        key = get_key()
        app.urls[key] = long_url
        return long_url
    except Exception as err:
        app.logger.warning(APP_UNEXPECTED_1ERR.format(err))
        flash(USR_UNEXPECTED)
    return None

@url_crud.route('/', methods=['POST'])
def handle_create_url(key=None):
    form_url = request.form.get('long_url', '')
    if new_url := commit_url(app.keys.consume, form_url):
        flash(USR_HTML_URL_ADD_1URL.format(app.short_url(key)))
        return redirect('/')
    else:
        return redirect(request.url_rule)


@url_crud.route('/update/<key>', methods=['POST'])
def handle_update_url(key=None):
    if not (url := app.urls[key]):
        abort(404)
    form_url = request.form.get('long_url', '')
    if new_url := commit_url(lambda : key, form_url):
        flash(USR_UPDATE_1URL_2URL.format(url, new_url))
        return redirect('/')
    else:
        return redirect(request.url_rule)


@url_crud.route('/<key>')
def handle_read_url(key):
    try:
        if response := app.cache.get(key):
            return response
    except Exception as err:
        app.logger.warning(APP_CACHE_1ERR.format(err))
    if url := app.urls[key]:
        response = redirect(url)
    else:
        abort(404)
    try:
        app.cache.set(key, response)
    except Exception as err:
        app.logger.warning(APP_CACHE_1ERR.format(err))
    return response


@url_crud.route('/delete/<key>')
def handle_delete_url(key):
    if url := app.urls[key]:
        del app.urls[key]
        flash(USR_URL_DEL_1URL.format(url))
        return redirect('/')
    abort(404)


@url_crud.route('/update/<key>', methods=['GET'])
def show_update_view(key):
    if url := app.urls[key]:
        return render_template('update.html', key=key, url=url)
    abort(404)


@url_crud.route('/', methods=['GET'])
def show_index_view():
    urls = list(app.urls)
    return render_template('index.html', urls=urls)
