from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms import Form
from wtforms.validators import DataRequired, Regexp, Length, ValidationError
from wtforms.fields import SelectField, TextAreaField, StringField, TimeField, FormField, FieldList, RadioField, HiddenField

photos = UploadSet('photos', IMAGES)

def init_photos(app):
    configure_uploads(app, photos)

class NewCourseForm(FlaskForm):
    title = StringField(
        label='Title',
        name='course-title',
        id='course-title',
        validators=[
            DataRequired(message='You need to specify the title of the course!'),
            Length(max=255, message='The title is too long!')
        ],
        render_kw={
            "placeholder":"Enter course title here..."
        }
    )
    logo = FileField(
        label='Course Image',
        name='course-logo',
        id='course-logo',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            FileRequired(message='You need to upload a file!'),
        ]
    )
    description = TextAreaField(
        label='Description',
        name='desc',
        id='desc',
        validators=[
            DataRequired(message='You need to specify the description of the course!')
        ],
        render_kw={
            'placeholder':'Enter course description here...',
            'rows':'4'
        }
    )

class CourseForm(FlaskForm):
    title = StringField(
        label='Title',
        name='course-title',
        id='course-title',
        validators=[
            DataRequired(message='You need to specify the title of the course!'),
            Length(max=255, message='The title is too long!')
        ],
        render_kw={
            "placeholder":"Enter course title here..."
        }
    )
    logo = FileField(
        label='Course Image',
        name='course-logo',
        id='course-logo',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
        ]
    )
    description = TextAreaField(
        label='Description',
        name='desc',
        id='desc',
        validators=[
            DataRequired(message='You need to specify the description of the course!')
        ],
        render_kw={
            'placeholder':'Enter course description here...',
            'rows':'4'
        }
    )
    visibility = SelectField(
        label='Visibility',
        name='visibility',
        id='visibility',
        choices=[
            ('draft', 'Draft'),
            ('archived', 'Archived'),
            ('published', 'Published')
        ],
        validate_choice=True,
        validators=[
            DataRequired(message="You need to specify the visibility of the course!")
        ]
    )


class ChoicesForm(Form):
    choices = StringField(
        validators=[
            DataRequired(message='Please specify the options!')
        ]
    )

# choices for ExistingContentForm()
class ChoicesFormNotRequired(Form):
    choices = StringField()

class ChallengeLearningForm(Form):
    order = HiddenField(
        validators=[DataRequired()]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
        ],
    )
    content_body = TextAreaField(
        label='Content',
        validators=[
            DataRequired(message='You need to specify the content!')
        ],
        render_kw={
            "placeholder":"Enter learning content here...",
            "rows":'4',
        }
    )

class ChallengeOptionsForm(Form):
    order = HiddenField(
        validators=[DataRequired()]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
        ],
    )
    question = TextAreaField(
        label='Question',
        validators=[
            DataRequired(message='You need to specify the question for the challenge!')
        ],
        render_kw={
            "placeholder":"Enter challenge question here...",
            "rows":'2',
        }
    )
    code = TextAreaField(
        label='Code',
        render_kw={
            "placeholder":"Enter challenge code here...",
            "rows":'10',
        }
    )
    options = RadioField(
        label='Options',
        choices=[
            ('value-1', 'Option 1'),
        ],
        validators=[
            DataRequired(message="You need to specify the options for the challenge!")
        ],
        validate_choice=False
    )
    choices = FieldList(FormField(ChoicesForm), min_entries=1)

class ChallengeInputForm(Form):
    order = HiddenField(
        validators=[DataRequired()]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
        ],
    )
    question = TextAreaField(
        label='Question',
        validators=[
            DataRequired(message='You need to specify the question for the challenge!')
        ],
        render_kw={
            "placeholder":"Enter challenge question here...",
            "rows":'2',
        }
    )
    code = TextAreaField(
        label='Code',
        render_kw={
            "placeholder":"Enter challenge code here...",
            "rows":'10',
        }
    )
    answer = StringField(
        label="Answer",
        validators=[
            DataRequired(message='You need to specify the answer for the challenge!')
        ],
        render_kw={
            "placeholder":"Enter the answer here..."
        }
    )

class NewModuleForm(FlaskForm):
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
    learning = FieldList(FormField(ChallengeLearningForm), min_entries=1)
    challenge_options = FieldList(FormField(ChallengeOptionsForm), min_entries=0)
    challenge_input = FieldList(FormField(ChallengeInputForm), min_entries=0)


class ExistingContentForm(Form):
    order = HiddenField()
    content_type = StringField()
    content_id = HiddenField()
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
        ],
    )
    new_filename = StringField()
    original_filename = StringField()
    content_body = TextAreaField(
        label='Content',
        render_kw={
            "placeholder":"Enter learning content here...",
            "rows":'4',
        }
    )
    question = TextAreaField(
        label='Question',
        render_kw={
            "placeholder":"Enter challenge question here...",
            "rows":'2',
        }
    )
    code = TextAreaField(
        label='Code',
        render_kw={
            "placeholder":"Enter challenge code here...",
            "rows":'10',
        }
    )
    options = RadioField(
        label='Options',
        choices=[
            ('value-1', 'Option 1'),
        ],
        validate_choice=False
    )
    choices = FieldList(FormField(ChoicesFormNotRequired), min_entries=10)
    correct = StringField()
    answer = StringField(
        label="Answer",
        render_kw={
            "placeholder":"Enter the answer here..."
        }
    )
    

class ModuleForm(FlaskForm):
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
    content = FieldList(FormField(ExistingContentForm), min_entries=15)
