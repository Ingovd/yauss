import sys
from flask import (Blueprint,
                   render_template,
                   request,
                   redirect)

from yauss.database import (create_url,
                      read_url_or_404,
                      read_all_urls,
                      update_url,
                      delete_url,
                      )

url_crud = Blueprint('url_crud', __name__, template_folder='templates')

@url_crud.route('/', methods=['POST'])
def handle_create_url():
    create_url(request.form['long_url'])
    return redirect('/')

@url_crud.route('/<my_key>')
def handle_read_url(my_key):
    url_to_redirect = read_url_or_404(my_key)
    return redirect("http://" + url_to_redirect['long_url'])

@url_crud.route('/update/<my_key>', methods=['POST'])
def handle_update_url(my_key):
    update_url(my_key, request.form['long_url'])
    return redirect('/')

@url_crud.route('/delete/<my_key>')
def handle_delete_url(my_key):
    delete_url(my_key)
    return redirect('/')

@url_crud.route('/update/<my_key>', methods=['GET'])
def show_update_view(my_key):
    url = read_url_or_404(my_key)
    return render_template('update.html', url=url)

@url_crud.route('/', methods=['GET'])
def show_index_view():
    urls = read_all_urls()
    return render_template('index.html', urls=urls)


