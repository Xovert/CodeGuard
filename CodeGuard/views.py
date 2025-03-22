from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from flask import send_file, abort
from mimetypes import guess_type

from CodeGuard.utils.user import is_authed, is_admin
from CodeGuard.utils.files import get_file
from CodeGuard.utils.decorators import login_required
from CodeGuard.utils.exam import check_exam

views = Blueprint('views', __name__, template_folder='front-end')

@views.route('/')
def index():
    url = check_exam()
    if url != None:
        return redirect(url)

    if is_admin():
        return redirect(url_for('admin.dashboard'))
    
    return render_template('index.html')


@views.route('/image/<path:filename>', methods=("GET",))
def image(filename):
    file = get_file(filename)
    mime_type = guess_type(filename)[0] or 'aplication/octet-stream'
    if file:
        return send_file(file, mimetype=mime_type)
    
    abort(404)



