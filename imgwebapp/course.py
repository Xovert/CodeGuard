import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
from imgwebapp.db import get_db

bp = Blueprint('course', __name__)

@bp.route('/catalogue')
def catalogue():
    #login required
    return render_template('user_catalogue.html')

@bp.route('/course_details')
def course_details():
    #login required
    return render_template('course_details.html')

@bp.route('/learning') # temporary only, nnti diganti
def learning():
    #login required
    return render_template('learning.html')

@bp.route('/challenge_option')
def challenge_option():
    return render_template('challenge_option.html')

@bp.route('/exam')
def exam():
    return render_template('exam.html')
