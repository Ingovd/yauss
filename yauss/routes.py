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
    except KeyError:
        flash('Please specify a valid url to be shortened.')
        return redirect('/')
    try:
        key = app.key_gateway.consume_key()
    except TimeoutError:
        flash('Could not acquire a unique key for your url. Please try again later.')
        return redirect('/')
    except ValueError:
        flash('Your key is already in use. Please try a different custom key.')
        return redirect('/')
    short = f"{app.config['SERVER_NAME']}/{key}"
    try:
        app.db_api.create_url(key, long_url)
        flash(Markup(f"Successfully added your url. Here is your link <a href='http://{short}'>{short}</a>"))
    except Exception:
        flash('Encountered an error while adding your url to the database. Please try again later.')
        redirect('/')
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
