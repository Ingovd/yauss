from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   abort,
                   flash,
                   Markup,
                   current_app as app)


url_crud = Blueprint('url_crud', __name__, template_folder='templates')


USR_INVALID_URL = 'Please specify a valid url to be shortened'
USR_USED_KEY = 'Your key is already in use, lease try a different custom key'
USR_UNEXPECTED = ('Unexpected error while handling your request, '
                  'please try again later')
USR_HTML_URL_ADD_1URL = Markup(
                         ("Successfully added your url. "
                          "Here is your link <a href='http://{0}'>{0}</a>")
                        )

APP_KEY_TIMOUT_1ERR = "Key store timed out during url creation: {}"
APP_UNEXPECTED_1ERR = "Unexpected error when handling url creation: {}"


@url_crud.route('/', methods=['POST'])
def handle_create_url():
    try:
        long_url = request.form['long_url']
        key = app.key_gateway.consume_key()
        app.urls[key] = long_url
    except KeyError:
        flash(USR_INVALID_URL)
    except ValueError:
        flash(USR_USED_KEY)
    except TimeoutError as err:
        app.logger.warning(APP_KEY_TIMOUT_1ERR.format(err))
        flash(USR_UNEXPECTED)
    except Exception as err:
        app.logger.warning(APP_UNEXPECTED_1ERR.format(err))
        flash(USR_UNEXPECTED)
    else:
        short = f"{app.config['SERVER_NAME']}/{key}"
        flash(USR_HTML_URL_ADD_1URL.format(short))
    finally:
        return redirect('/')


@url_crud.route('/<key>')
def handle_read_url(key):
    if response := app.cache.get(key):
        return response
    if url := app.urls[key]:
        response = redirect(url)
        app.cache.set(key, response)
        return response
    abort(404)


@url_crud.route('/update/<key>', methods=['POST'])
def handle_update_url(key):
    if app.urls[key]:
        app.urls.update_url(key. request.form['long_url'])
        return redirect('/')
    abort(404)


@url_crud.route('/delete/<key>')
def handle_delete_url(key):
    del app.urls[key]
    return redirect('/')


@url_crud.route('/update/<key>', methods=['GET'])
def show_update_view(key):
    if url := app.urls[key]:
        return render_template('update.html', key=key, url=url)
    abort(404)


@url_crud.route('/', methods=['GET'])
def show_index_view():
    urls = list(app.urls)
    return render_template('index.html', urls=urls)
