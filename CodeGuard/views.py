from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from flask import send_file, abort
from mimetypes import guess_type

from CodeGuard.utils.user import is_authed
from CodeGuard.utils.files import get_file
from CodeGuard.utils.decorators import login_required

views = Blueprint('views', __name__, template_folder='front-end')

@views.route('/')
def index():
    return render_template('index.html')


@views.route('/image/<path:filename>', methods=("GET",))
def image(filename):
    file = get_file(filename)
    mime_type = guess_type(filename)[0] or 'aplication/octet-stream'
    if file:
        return send_file(file, mimetype=mime_type)
    
    abort(404)

# @views.route('/login', methods=('GET',))
# def login():
#     return render_template('login.html')

