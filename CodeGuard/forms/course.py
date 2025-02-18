from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms.validators import DataRequired, Regexp, Length, ValidationError
from wtforms.fields import SubmitField, SelectField, TextAreaField, StringField, TimeField, FormField, FieldList, RadioField

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
            # FileRequired(message='You need to upload a file!'),
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

# class TypeForm(FlaskForm):
#     types = SelectField(
#         label='Type',
#         choices=[
#             ('Learning', 'Learning'),
#             ('Challenge Code', 'Challenge Code'),
#             ('Challenge Options', 'Challenge Options')
#         ],
#         validate_choice=True,
#         validators=[
#             DataRequired(message="You need to specify the type of the type of the page!")
#         ]
#     )

class ImageForm(FlaskForm):
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            FileRequired(message='You need to upload a file!')
        ],
    )

class ContentBodyForm(FlaskForm):
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

class QuestionCodeForm(FlaskForm):
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
        validators=[
            DataRequired(message='You need to specify the code for the challenge!')
        ],
        render_kw={
            "placeholder":"Enter challenge code here...",
            "rows":'10',
        }
    )

class OptionsForm(FlaskForm):
    options = RadioField(
        label='Options',
        choices=[
            ('value-1', 'Option 1'),
            ('value-2', 'Option 2'),
            ('value-3', 'Option 3')
        ],
        validators=[
            DataRequired(message="You need to specify the options for the challenge!")
        ]
    )

class TimerForm(FlaskForm):
    timer = TimeField(
        label='Timer',
        format='%H:%M:%S',
        validators=[
            DataRequired(message='You need to specify the exam completion time!')
        ],
    )
    

class ChallengeLearningForm(FlaskForm):
    image = FormField(ImageForm)
    content_body = FormField(ContentBodyForm)


class ChallengeCodeForm(FlaskForm):
    question_code = FormField(QuestionCodeForm)

class ChallengeOptionsForm(FlaskForm):
    question_code = FormField(QuestionCodeForm)
    options = FormField(OptionsForm)

class ExamCodeForm(FlaskForm):
    timer = FormField(TimerForm)
    question_code = FormField(QuestionCodeForm)

class ExamOptionsForm(FlaskForm):
    timer = FormField(TimerForm)
    question_code = FormField(QuestionCodeForm)
    options = FormField(OptionsForm)

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
    challenge_code = FieldList(FormField(ChallengeCodeForm), min_entries=1)
    challenge_options = FieldList(FormField(ChallengeOptionsForm), min_entries=1)
    exam_code = FieldList(FormField(ExamCodeForm), min_entries=1)
    exam_options = FieldList(FormField(ExamOptionsForm), min_entries=1)


