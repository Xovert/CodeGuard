import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
from imgwebapp.db import get_db

bp = Blueprint('course', __name__)

@bp.route('/learning') # temporary only, nnti diganti
def learning():
    #login required
    return render_template('learning.html')