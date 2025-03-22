from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask import current_app as app

mail = Mail()

def use_mail_service() -> bool:
    return bool(app.config.get('MAIL_SERVER', False))

def generate_token(data):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(data, salt=app.config["SECURITY_PASSWORD_SALT"])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        data = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except Exception:
        return None
    return data

def send_email(to, subject, template):
    if use_mail_service():
        sender = app.config["MAIL_DEFAULT_SENDER"]
        message = Message(
            subject=subject,
            recipients=[to],
            html=template,
            sender=sender,
        )
        mail.send(message)
