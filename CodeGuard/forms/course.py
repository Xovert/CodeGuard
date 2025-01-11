from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms.fields import SubmitField, SelectField, TextAreaField

photos = UploadSet('photos', IMAGES)

def init_photos(app):
    configure_uploads(app, photos)


class NewCourseForm(FlaskForm):
    type = SelectField(
        label='Type',
        choices=[
            ('Learning', 'Learning'),
            ('Challenge Code', 'Challenge Code'),
            ('Challenge Option', 'Challenge Option')
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
        render_kw={
            "placeholder":"Enter learning content here...",
        }
    )