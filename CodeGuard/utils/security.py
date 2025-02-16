from flask import session
import secrets


def generate_token() -> str:
    token = secrets.token_urlsafe(16)
    session['token'] = token
    return token


def verify_token(token) -> bool:
    if session['token'] and session['token'] == token:
        return True
    else:
        return False