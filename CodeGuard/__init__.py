import os
from flask import Flask
from flask_wtf import CSRFProtect
from CodeGuard.utils.initialize import init_templates
from CodeGuard.models import db
from CodeGuard.utils.migrations import migration
from flask_migrate import upgrade
from datetime import timedelta
from flask_mail import Mail

def create_app(config="CodeGuard.config.production", instance_path=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path, static_folder='front-end/static')
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
