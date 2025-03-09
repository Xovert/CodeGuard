from flask import Blueprint, current_app as app, render_template, url_for, request, flash, redirect, abort

from CodeGuard.utils.user import get_current_user
from CodeGuard.utils.decorators import login_required
from CodeGuard.utils.exam import check_exam
from CodeGuard.forms.profile import ProfileForm, UpdatePasswordForm
from CodeGuard.user import profile as profiles

user = Blueprint('user', __name__, template_folder='front-end')

@user.route('/profile', methods=('GET','POST'))
@login_required
def profile():
    if request.method == 'GET':
        user = get_current_user()
        form = ProfileForm()

        form.fullname.data = user.fullname
        form.username.data = user.username
        form.email.data = user.email

        return render_template(
            "user/profile.html",
            form=form,
            regis_date=user.registration_date
        )

    error = None
    success = None
    form = ProfileForm()
    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data

        error, success = profiles.update_profile(fullname, username, email)

        if error:
            flash(error)
        else:
            flash(success)
    
    else:
        error = "<br>".join(
            message for messages in form.errors.values() for message in messages
        )
        flash(error)
    
    return redirect(url_for('user.profile'))


@user.route('/update_pw' , methods=('POST',))
def update_pw():
    if request.method == 'POST':
        form = UpdatePasswordForm()
        error = success = None

        if form.validate_on_submit():
            old_password = form.old_password.data
            new_password = form.new_password.data

            error, success = profiles.update_pw(old_password, new_password)

            if error:
                flash(error)
            else:
                flash(success)
        
        else:
            error = "<br>".join(
                message for messages in form.errors.values() for message in messages
            )
            flash(error)
        return redirect(url_for('user.profile'))


@user.before_request
def check():
    url = check_exam()
    if url != None:
        return redirect(url)