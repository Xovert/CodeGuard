from flask import Blueprint, current_app as app, render_template, url_for, request, flash, redirect, abort
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError as sqlerror

from CodeGuard.utils.user import get_current_user
from CodeGuard.models import (
    db, 
    Users,
)

bcrypt = Bcrypt()

def update_profile(fullname, username, email):
    error = success = None
    user = get_current_user()

    try:
        user.fullname = fullname
        user.username = username
        user.email = email
    except sqlerror as e:
        db.session.rollback()
        error = "An error occurred while updating user profile, please try again"
        print(e)
    else:
        db.session.commit()
        success = "Profile successfully updated"
    
    return error, success

def update_pw(old_password, new_password):
    error = success = None
    user = get_current_user()
    
    same = bcrypt.check_password_hash(user.password, old_password)
    if not same:
        error = "Old password does not match with current user's password"

    if error is None:
        try:
            user.password = bcrypt.generate_password_hash(new_password)
            db.session.flush()
        except sqlerror as e:
            db.session.rollback()
            error = "An error occurred while updating the user's password, please try again"
            print(e)
        else:
            db.session.commit()
            success = "Password successfully updated"
    
    return error, success