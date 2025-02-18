from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask import current_app as app

mail = Mail()


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except Exception:
        return None
    return email

def send_email(to, subject, template):
    sender = app.config["MAIL_DEFAULT_SENDER"]
    message = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=sender,
    )
    mail.send(message)
