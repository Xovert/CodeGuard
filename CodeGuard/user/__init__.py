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

@user.route('/profile/save' , methods=('PATCH',))
def update():
    return redirect(url_for('profile'))
# intended: utk save changes of updates
# NOW KEGUNAANNYA UNTUK:
# update profile + pw, if any attr is empty, flash
# flash('Apa field cannot be empty!')

# @user.route('/profile/change', methods=('PATCH', 'GET'))
# def change():
#     if request.method == 'GET':
#         return render_template('change_pass.html')
    # redirect(url_for('change_pass.html'))
# intended: utk GET change_pass
# DOES NOT NEED THIS ANYMORE
