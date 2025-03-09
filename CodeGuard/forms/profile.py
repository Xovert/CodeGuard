from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo, Regexp
from wtforms.fields import PasswordField, EmailField, StringField

class ProfileForm(FlaskForm):
    fullname = StringField(
        label='Full Name',
        name='fullname',
        id='fullname',
        validators=[
            DataRequired(message='Full name cannot be empty!'),
            Regexp(
                '^[a-zA-Z ]+$',
                message="Full name can only contain letters and spaces"
            ),
        ]
    )
    username = StringField(
        label='Username',
        name='username',
        id='username',
        validators=[
            DataRequired(message='Username cannot be empty!'),
            Regexp(
                '^[a-zA-Z0-9._-]{3,20}$',
                message="Username can only contain letters, numbers, dots, underscores, or hyphens (3-20 characters)"
            )
        ],
    )
    email = EmailField(
        label='Email',
        name='email',
        id='email',
        validators=[
            Email(message='Enter a valid email address'),
            DataRequired(message='Input your email address'),
        ],
    )


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField(
        label='Old Password',
        name='old-password',
        id='old-password',
        validators=[
            DataRequired(message="Old password cannot be empty!"),
        ],
        render_kw={
            "placeholder":"Enter your old password...",
        }
    )
    new_password = PasswordField(
        label='New Password',
        name='new-password',
        id='new-password',
        validators=[
            DataRequired(message="New password cannot be empty!"),
            EqualTo('rpt_password', message='Passwords does not match'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,40}$',
                message="Password must contain at least one uppercase, one lowercase, and one number (8-40 characters)"
            )
        ],
        render_kw={
            "placeholder":"Enter your new password...",
        }
    )
    rpt_password = PasswordField(
        label='Confirm Password',
        name='rpt-password',
        id='rpt-password',
        validators=[
            DataRequired(message="Confirm your new password!"),
        ],
        render_kw={
            "placeholder":"Confirm your new password...",
        }
    )