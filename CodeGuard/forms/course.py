from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms.validators import DataRequired
from wtforms.fields import SubmitField, SelectField, TextAreaField, StringField

photos = UploadSet('photos', IMAGES)

def init_photos(app):
    configure_uploads(app, photos)


class NewCourseForm(FlaskForm):
    module = StringField(
        label='Module Name',
        name='module-name',
        validators=[
            DataRequired(message='You need to specify the module name!')
        ],
        render_kw={
            "placeholder":"Enter the module name here...",
        }
    )
    type = SelectField(
        label='Type',
        choices=[
            ('Learning', 'Learning'),
            ('Challenge Code', 'Challenge Code'),
            ('Challenge Options', 'Challenge Options')
        ]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            FileRequired(message='You need to upload a file!')
        ],
        name='learning-pic',
    )
    content_body = TextAreaField(
        label='Content',
        name="content-learning",
        validators=[
            DataRequired(message='You need to specify the content!')
        ],
        render_kw={
            "placeholder":"Enter learning content here...",
        }
    )