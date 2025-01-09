from flask import current_app as app
from flask import session

from CodeGuard.models import Users

def get_current_user():
    if is_authed():
        user = Users.query.filter_by(id=session["id"]).first()
        return user
    else:
        return None

def is_authed():
    return bool(session.get("uuid", False))


def is_admin():
    return session.get("role") == "admin"


def login_session(user):
    session["id"] = user.id
    session["uuid"] = user.uuid
    session["username"] = user.username
    session["role"] = user.role
    session.permanent = True


def logout_session():
    session.clear()