from typing import Optional

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   abort,
                   flash,
                   current_app as app)

from urllib.parse import urlparse

from .templates.messages import *


url_crud = Blueprint('url_crud', __name__, template_folder='templates')


def format_url(long_url: str) -> Optional[str]:
    parsed_url = urlparse(long_url)
    if not parsed_url.scheme:
        parsed_url = urlparse(f"http://{long_url}")
    if parsed_url.netloc:
        return parsed_url.geturl()
    return None


@url_crud.route('/', methods=['POST'])
def handle_create_url():
    if not (long_url := request.form.get('long_url', '')):
        flash(USR_INVALID_URL)
        return redirect('/')
    try:
        key = app.key_gateway.consume_key()
        app.urls[key] = long_url
        short = f"{app.config['SERVER_NAME']}/{key}"
        flash(USR_HTML_URL_ADD_1URL.format(short))
    except KeyStoreError as err:
        app.logger.warning(APP_KEY_1ERR.format(err))
        flash(USR_UNEXPECTED)
    except Exception as err:
        app.logger.warning(APP_UNEXPECTED_1ERR.format(err))
        flash(USR_UNEXPECTED)
    finally:
        return redirect('/')


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


@url_crud.route('/update/<key>', methods=['POST'])
def handle_update_url(key):
    try:
        new_url = request.form['long_url']
    except KeyError:
        flash(USR_INVALID_URL)
        return redirect(f"/update/{key}")
    if url := app.urls[key]:
        app.urls.update_url(key, new_url)
        flash(USR_UPDATE_1URL_2URL.format(url, new_url))
        return redirect('/')
    abort(404)


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
