import functools

from flask import abort, request, redirect, url_for, g
from CodeGuard.utils.user import is_authed, is_admin


def login_required(view):
    
    @functools.wraps(view)
    def login_wrapper(*args, **kwargs):
        if is_authed():
            return view(*args, **kwargs)
        else:
            abort(403)
    return login_wrapper


def admin_required(view):

    @functools.wraps(view)
    def admin_required_wrapper(*args, **kwargs):
        if is_authed() and is_admin():
            return view(*args, **kwargs)
        else:
            abort(404)
    return admin_required_wrapper

def exams_unlocked(view):

    @functools.wraps(view)
    def exams_unlocked_wrapper(*args, **kwargs):
        if g.modulesComplete:
            return view(*args, **kwargs)
        else:
            abort(404)
    return exams_unlocked_wrapper

