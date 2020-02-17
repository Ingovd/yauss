from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   flash,
                   Markup,
                   current_app as app)


url_crud = Blueprint('url_crud', __name__, template_folder='templates')


@url_crud.route('/', methods=['POST'])
def handle_create_url():
    try:
        long_url = request.form['long_url']
        key = app.key_gateway.consume_key()
        short = f"{app.config['SERVER_NAME']}/{key}"
        app.db_api.create_url(key, long_url)
    except KeyError:
        flash('pPlease specify a valid url to be shortened')
    except ValueError:
        flash('Your key is already in use, lease try a different custom key')
    except TimeoutError as err:
        app.logger.warning(f"Key store timed out during url creation: {err}")
        flash('Unexpected error while handling your request, please try again later')
    except Exception as err:
        app.logger.warning(f"Unexpected error when handling url creation: {err}")
        flash('Unexpected error while handling your request, please try again later')
    else:
        flash(Markup(f"Successfully added your url. Here is your link <a href='http://{short}'>{short}</a>"))
    finally:
        return redirect('/')


@url_crud.route('/<key>')
@app.cache.cached()
def handle_read_url(key):
    url = app.db_api.read_url_or_404(key)
    return redirect("http://" + url['long_url'])


@url_crud.route('/update/<key>', methods=['POST'])
def handle_update_url(key):
    print(request.form['long_url'])
    app.db_api.update_url(key, request.form['long_url'])
    return redirect('/')


@url_crud.route('/delete/<key>')
def handle_delete_url(key):
    app.db_api.delete_url(key)
    return redirect('/')


@url_crud.route('/update/<key>', methods=['GET'])
def show_update_view(key):
    url = app.db_api.read_url_or_404(key)
    return render_template('update.html', url=url)


@url_crud.route('/', methods=['GET'])
def show_index_view():
    urls = app.db_api.read_all_urls()
    return render_template('index.html', urls=urls)
