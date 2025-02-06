import functools
from flask import Blueprint, flash, g, redirect, render_template
from flask import current_app, request, session, url_for
from sqlalchemy import exc
from flask_bcrypt import Bcrypt
from uuid import uuid4, UUID
from datetime import datetime, timezone, timedelta

from CodeGuard.forms.auth import LoginForm, RegisterForm, ForgotForm, ChangePass
from CodeGuard.models import db, Users
from CodeGuard.utils.user import is_authed, is_admin, login_session, logout_session, get_current_user
from CodeGuard.utils.email import generate_token, confirm_token, send_email
from CodeGuard.utils.decorators import login_required

bcrypt = Bcrypt()

auth = Blueprint('auth', __name__, template_folder='front-end')


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        if is_authed():
            flash('You already logged in!')
            return redirect(url_for('courses.dashboard'))
        return render_template('register.html')
    
    form = RegisterForm()
    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        rpt_password = form.rpt_password.data
        
        error = None
        success = None

        usernames = db.session.scalars(
            db.select(Users.username)
            .where(Users.username == username)
        ).first()


        emails = db.session.scalars(
            db.select(Users.email)
            .where(Users.email == email)
        ).first()


        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != rpt_password:
            error = 'Password is not the same'
        elif usernames is not None:
            error = 'Username is taken!'
        elif emails is not None:
            error = 'Email has already been registered!'

        if error is None:
            user = Users(
                uuid=uuid4(),
                role='user',
                fullname=fullname,
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(password),
                registration_date=datetime.now(timezone(timedelta(hours=7)))
            )
            db.session.add(user)
            try:
                success = f'Registration for {username} is successful!'
                db.session.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
                flash(error)
                db.session.rollback()
                return redirect(url_for('auth.register'))
            
            token = generate_token(email)
            confirm_url = url_for('auth.verify', token=token, _external=True)
            html = render_template("user/confirmation.html", url=confirm_url)
            subject = "Please confirm your email account"
            send_email(user.email, subject, html)

            login_session(user)
            db.session.close()

            flash(success)
            return redirect(url_for('courses.dashboard'))
    
    error = "<br>".join(
        message for messages in form.errors.values() for message in messages
    )
    flash(error)
    return redirect(url_for('auth.register'))


@auth.route('/verify/<token>', methods=('GET',))
@login_required
def verify(token):
    current_user = get_current_user()
    if current_user.is_confirmed:
        return redirect(url_for("courses.dashboard"))
    
    email = confirm_token(token)
    if current_user.email == email:
        current_user.is_confirmed = True
        current_user.confirmed_on = datetime.now(timezone(timedelta(hours=7)))
        db.session.commit()
        db.session.close()
        flash("You have confirmed your email, thank you!")
    else:
        flash("The confirmation link is invalid or has expired.")

    return redirect(url_for("courses.dashboard"))


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if is_authed():
        flash('You already logged in!')
        return redirect(url_for('courses.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        error = None
        user = Users.query.filter_by(email=email).first()

        if user is None:
            error = 'Your email or password is incorrect.'
        elif not bcrypt.check_password_hash(user.password, password):
            error = 'Your email or password is incorrect.'

        if error is None:
            session.clear()
            login_session(user)
            redir = 'courses'
            if is_admin():
                redir = 'admin'
            return redirect(url_for(f'{redir}.dashboard', errors=error))
        flash(error)
    return render_template('login.html')

@auth.route('/forgot_pass', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_pass.html')
    
    elif request.method == 'POST':
        form = ForgotForm()

        if form.validate_on_submit():
            email = form.email.data
            user = Users.query.filter_by(email=email).first()

            if user:
                uuid = str(user.uuid)
                token = generate_token(uuid)
                print(token)
                change_url = url_for('auth.change_password', token=token, _external=True)
                html = render_template("change_pass_email.html", url=change_url, fullname=user.fullname)
                subject = "Reset Your Password"
                send_email(user.email, subject, html)
            flash("An email has been sent to your account!")           

        else:
            error = "<br>".join(
                message for messages in form.errors.values() for message in messages
            )
            flash(error)
        return redirect(url_for('auth.forgot_password'))
    
@auth.route('/change_pass/<token>', methods=('GET', 'POST'))
def change_password(token):
    if request.method == "GET":
        return render_template('change_pass.html', token=token)
    
    elif request.method == 'POST':
        form = ChangePass()

        error = None
        if form.validate_on_submit():
            new_pw = form.password.data
            print(new_pw)

            uuid = confirm_token(token)
            if uuid:
                uuid = UUID(uuid)
                user = Users.query.filter_by(uuid=uuid).first()

                try:
                    user.password = bcrypt.generate_password_hash(new_pw)
                    db.session.commit()
                    success = "Your password has been successfully reset"
                    flash(success)
                except db.IntegrityError:
                    error = f"Reset password failed"
                    db.session.rollback()
            
                return redirect(url_for('auth.logout'))
            else:
                flash("The link is invalid or has expired")
                return redirect(url_for('auth.forgot_password'))
        
        error = "<br>".join(
            message for messages in form.errors.values() for message in messages
        )
        flash(error)
        return redirect(url_for('auth.change_password', token=token, _external=True))

@auth.route('/logout')
def logout():
    if is_authed():
        logout_session()
    return redirect(url_for('views.index'))


@auth.before_app_request
def load_logged_in_user():
    current_user = get_current_user()
    if current_user is None:
        g.user_id = None
    else:
        g.user_id = current_user.id

@auth.after_app_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response


