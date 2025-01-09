from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from CodeGuard.utils.user import is_authed

views = Blueprint('views', __name__, template_folder='front-end')

@views.route('/')
def index():
    return render_template('index.html')


# @views.route('/login', methods=('GET',))
# def login():
#     return render_template('login.html')

