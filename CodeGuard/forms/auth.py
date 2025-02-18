from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo, Regexp
from wtforms.fields import PasswordField, EmailField, StringField

class LoginForm(FlaskForm):
    email = EmailField(
        label='Your E-mail',
        name='email',
        validators=[
            Email(message='Enter a valid email address'),
            DataRequired(message='Input your email address'),    
        ],
        render_kw={
            "placeholder":"Your email here",
        }
    )
    password = PasswordField(
        label='Your Password',
        name='password',
        validators=[
            DataRequired(message="Password Required"),
        ],
        render_kw={
            "placeholder":"Your password here",
        }
    )

class RegisterForm(FlaskForm):
    email = EmailField(
        label='Email',
        # name='email',
        validators=[
            Email(message='Enter a valid email address'),
            DataRequired(message='Input your email address'),
        ],
        render_kw={
            'placeholder':"Please enter your email",
        }
    )
    fullname = StringField(
        label='Full Name',
        # name='fullname',
        validators=[
            DataRequired(message='Input your full name'),
            Regexp(
                '^[a-zA-Z ]+$',
                message="Full name can only contain letters and spaces"
            ),
        ],
        render_kw={
            "placeholder":"Please enter your full name",
        }
    )
    username = StringField(
        label='Username',
        # name='username',
        validators=[
            DataRequired(message='Input your username'),
            Regexp(
                '^[a-zA-Z0-9._-]{3,20}$',
                message="Username can only contain letters, numbers, dots, underscores, or hyphens (3-20 characters)"
            )
        ],
        render_kw={
            "placeholder":"Please enter your username",
        }
    )
    password = PasswordField(
        label='Password',
        # name='password',
        validators=[
            DataRequired(message='Input your password'),
            EqualTo('rpt_password', message='Passwords does not match'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,40}$',
                message="Password must contain at least one uppercase, one lowercase, and one number (8-40 characters)"
            )
        ],
        render_kw={
            "placeholder":"Please enter your password",
        }
    )
    rpt_password = PasswordField(
        label='Repeat your password',
        # name='password',
        validators=[
            DataRequired(message='Re-input your password'),
        ],
        render_kw={
            "placeholder":"Please re-enter your password",
        }

    )

class ForgotForm(FlaskForm):
    email = EmailField(
        # label='Email',
        name='email',
        validators=[
            Email(message='Enter a valid email address'),
            DataRequired(message='Input your email address'),
        ],
        render_kw={
            'placeholder':"example@gmail.com",
            'autocomplete':'off',
        }
    )

class ChangePass(FlaskForm):
    password = PasswordField(
        # label='Password',
        name='password',
        validators=[
            DataRequired(message='Input your password'),
            EqualTo('rpt_password', message='Passwords does not match'),
            # Length(min=8, max=40, message=None)
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,40}$',
                message="Password must contain at least one uppercase, one lowercase, and one number (8-40 characters)"
            )

            
        ],
        render_kw={
            "placeholder":"New Password",
            "autocomplete":"off"
        }
    )
    rpt_password = PasswordField(
        # label='Repeat your password',
        name='rpt-password',
        validators=[
            DataRequired(message='Re-input your password'),
        ],
        render_kw={
            "placeholder":"Confirm Password",
            "autocomplete":"off"
        }

    )