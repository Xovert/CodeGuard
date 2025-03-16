class _FormsWrapper:
    pass

Forms = _FormsWrapper()

from CodeGuard.forms import auth
from CodeGuard.forms import course
from CodeGuard.forms import profile
from CodeGuard.forms import exam

Forms.auth = auth
Forms.course = course
Forms.profile = profile
Forms.exam = exam