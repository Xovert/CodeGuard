from flask import current_app as app
from flask import session

from CodeGuard.models import Users, db

def get_current_user():
    if is_authed():
        user = db.session.scalars(
            db.select(Users).where(Users.uuid == session["uuid"])
        ).first()
        return user
    else:
        return None

def is_authed():
    return bool(session.get("uuid", False))


def is_admin():
    return session.get("role") == "admin"

def get_uuid():
    return session.get('uuid', None)

def login_session(user):
    session["uuid"] = user.uuid
    session["username"] = user.username
    session["role"] = user.role
    session.permanent = True


def logout_session():
    session.clear()