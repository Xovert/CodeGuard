class _FormsWrapper:
    pass

Forms = _FormsWrapper()

from CodeGuard.forms import auth
from CodeGuard.forms import course
from CodeGuard.forms import challenges
from CodeGuard.forms import profile

Forms.auth = auth
Forms.course = course
Forms.challenges = challenges
Forms.profile = profile
