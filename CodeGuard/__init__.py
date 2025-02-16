import os
from flask import Flask
from flask_wtf import CSRFProtect
from CodeGuard.utils.initialize import init_templates
from CodeGuard.models import db
from CodeGuard.utils.migrations import migration
from flask_migrate import upgrade
from datetime import timedelta
from flask_mail import Mail

def create_app(config="CodeGuard.config.config", test_config=None, instance_path=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path, static_folder='front-end/static')
    # app.config.from_mapping(
    #     SECRET_KEY='devtesthings',
    #     DATABASE=os.path.join(app.instance_path, 'imgwebapp.sqlite'),
    #     MAX_CONTENT_LENGTH = 1024 * 1024,
    #     UPLOADED_PHOTOS_DEST='uploads',
    #     PERMANENT_SESSION_LIFETIME = timedelta(days=2),
    #     SECURITY_PASSWORD_SALT = '474e09ff10b75e34dc1745b1890339f2ee93355b892266590adac68ad84849bc',
    #     MAIL_DEFAULT_SENDER = "",
    #     MAIL_SERVER = "smtp.gmail.com",
    #     MAIL_PORT = 465,
    #     MAIL_USE_TLS = False,
    #     MAIL_USE_SSL = True,
    #     MAIL_DEBUG = False,
    #     MAIL_USERNAME = "",
    #     MAIL_PASSWORD = "",
    #     AWS_S3_ENDPOINT_URL = "http://127.0.0.1:9000",
    #     AWS_S3_BUCKET = "codeguard",
    #     AWS_ACCESS_KEY_ID = "minioadmin",
    #     AWS_SECRET_ACCESS_KEY = "minioadmin",
    #     AWS_S3_REGION = "us-east-1",
    #     UPLOAD_PROVIDER = "minio",
    #     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://codeguard:codeguard@127.0.0.1:7306/CodeGuard?charset=utf8mb4",
    #     SEMGREP_PATH = 'semgrep_rules',
    #     SEMGREP_APP_TOKEN = '2a749583386f06e68ba6a754ce773af03e0a55044567342a703802fdd9c9645b'
    # )

    if test_config is not None:
        app.config.from_object(test_config)
    else:
        app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(os.path.join(app.instance_path, app.config['UPLOADED_PHOTOS_DEST']))
    except OSError:
        pass


    with app.app_context():
        db.init_app(app)
        migration.init_app(app, db)

        init_templates(app)

        from CodeGuard.utils.email import mail
        mail.init_app(app)

        from CodeGuard.forms.course import init_photos
        from CodeGuard.seed import init_seed
        init_seed(app)
        init_photos(app)

        
        from CodeGuard.views import views
        from CodeGuard.auth import auth
        from CodeGuard.courses import courses
        from CodeGuard.user import user
        from CodeGuard.admin import admin
        
        app.register_blueprint(views)
        app.register_blueprint(auth)
        app.register_blueprint(courses)
        app.register_blueprint(user)
        
        app.register_blueprint(admin)

        
    return app
