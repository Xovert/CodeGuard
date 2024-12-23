import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
from imgwebapp.db import get_db

bcrypt = Bcrypt()

bp = Blueprint('auth', __name__)

@bp.route('/')
def loginnew():
    if g.user is None:
        return render_template('login.html')
    else:
        return redirect(url_for('gallery'))

@bp.route('/admin')
def admin():
    return render_template('admin.html')

@bp.route('/admin_course_detail')
def admin_course_detail():
    return render_template('admin_course_detail.html')

@bp.route('/admin_course_content')
def admin_course_content():
    return render_template('admin_course_content.html')

@bp.route('/challengePHP')
def challengePHP():
    return render_template('challengePHP.html')

@bp.route('/examPHP')
def examPHP():
    return render_template('examPHP.html')

@bp.route('/challengeJS')
def challengeJS():
    return render_template('challengeJS.html')

@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/profile')
def profile():
    return render_template('profile.html')

@bp.route('/editprofile')
def editprofile():
    return render_template('editprofile.html')

@bp.route('/saveProfile')
def saveProfile():
    return redirect(url_for('profile'))

@bp.route('/forgotPass')
def forgotPass():
    return render_template('ForgotPass.html')

@bp.route('/testcodeMirror')
def testcodeMirror():
    return render_template('testcodeMirror.html')

@bp.route('/changePass', methods=('GET', 'POST'))
def changePass():
    if request.method == "GET":
        return render_template('changePass.html')

    # else:
    #     oldpassword = request.form[]
    #     password = request.form[]
    #     rpt_password = request.form[]
        
    #     if oldpassword
        
    #     elif password != rpt_password:
    #         error = 'Password is not the same'
        

@bp.route('/cancelPass')
def cancelPass():
    # if cancel tapi changepass dari forgot password
    if g.user is None:
        return render_template('login.html')
    # elif cancel tapi changepass dari edit profile
    else:
        return render_template('profile.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        username = request.form['reg-username']
        password = request.form['reg-password']
        rpt_password = request.form['rpt-password']
        db = get_db()
        error = None
        success = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != rpt_password:
            error = 'Password is not the same'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, bcrypt.generate_password_hash(password)),
                )
                db.commit()
                success = f'Registration for {username} is successful!'
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash(success)
                return redirect(url_for('index'))

        flash(error)

    return redirect(url_for('index'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if g.user is not None:
            error = "You already logged in!"
        elif user is None:
            error = 'Your username or password is incorrect.'
        elif not bcrypt.check_password_hash(user['password'], password):
            error = 'Your username or password is incorrect.'

        if error is None:
            session.clear()
            session['uid'] = user['id']
            return redirect(url_for('gallery'))

        flash(error)

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    uid = session.get('uid')

    if uid is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (uid,)
        ).fetchone()

@bp.after_app_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
