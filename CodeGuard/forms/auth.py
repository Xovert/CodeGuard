from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired
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
            DataRequired(message='Input your full'),
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
