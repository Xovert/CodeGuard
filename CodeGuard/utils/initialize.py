from flask import current_app, session

def init_templates(app):
    from CodeGuard.utils.user import is_authed, is_admin
    from CodeGuard.forms import Forms
    from CodeGuard.models.enums import CompletionStatus, CourseStatus
    app.jinja_env.globals.update(is_authed=is_authed)
    app.jinja_env.globals.update(is_admin=is_admin)
    app.jinja_env.globals.update(Forms=Forms)
    app.jinja_env.globals.update(CourseStatus=CourseStatus)
    app.jinja_env.globals.update(CompletionStatus=CompletionStatus)
    
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
