from flask import Blueprint, current_app, render_template, url_for
from flask import redirect, url_for

from CodeGuard.utils.user import get_current_user
from CodeGuard.utils.decorators import login_required

user = Blueprint('user', __name__, template_folder='front-end')

@user.route('/profile', methods=('GET',))
@login_required
def profile():
    user = get_current_user()
    return render_template("user/profile.html", username=user.username, email=user.email, fullname=user.fullname, regis_date=user.registration_date)

@user.route('/profile/edit', methods=('GET',))
def settings():
    return render_template("user/editprofile.html")

@user.route('/profile/save' , methods=('PATCH',))
def update():
    return redirect(url_for('profile'))

@user.route('/profile/change', methods=('PATCH',))
def change():
    return redirect(url_for('change_pass.html'))
