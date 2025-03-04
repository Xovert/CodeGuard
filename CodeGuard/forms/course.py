from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms import Form
from wtforms.validators import DataRequired, Regexp, Length, ValidationError
from wtforms.fields import SubmitField, SelectField, TextAreaField, StringField, TimeField, FormField, FieldList, RadioField, HiddenField

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
    
class OrderForm(FlaskForm):
    order = HiddenField(
        validators=[DataRequired()]
    )



class ChoicesForm(Form):
    choices = StringField(
        validators=[
            DataRequired(message='Please specify the options!')
        ]
    )

class ChallengeLearningForm(Form):
    # order = FormField(OrderForm)
    # image = FormField(ImageForm)
    # content_body = FormField(ContentBodyForm)
    order = HiddenField(
        validators=[DataRequired()]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            # FileRequired(message='You need to upload a file!')
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


class ChallengeCodeForm(Form):
    # order = FormField(OrderForm)
    # question_code = FormField(QuestionCodeForm)
    order = HiddenField(
        validators=[DataRequired()]
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
        validators=[
            DataRequired(message='You need to specify the code for the challenge!')
        ],
        render_kw={
            "placeholder":"Enter challenge code here...",
            "rows":'10',
        }
    )

class ChallengeOptionsForm(Form):
    # order = FormField(OrderForm)
    # question_code = FormField(QuestionCodeForm)
    # options = FormField(OptionsForm)
    order = HiddenField(
        validators=[DataRequired()]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            # FileRequired(message='You need to upload a file!')
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
        # validators=[
        #     DataRequired(message='You need to specify the code for the challenge!')
        # ],
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


class ExamCodeForm(Form):
    # order = FormField(OrderForm)
    # timer = FormField(TimerForm)
    # question_code = FormField(QuestionCodeForm)
    order = HiddenField(
        validators=[DataRequired()]
    )
    timer = TimeField(
        label='Timer',
        format='%H:%M:%S',
        validators=[
            DataRequired(message='You need to specify the exam completion time!')
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
        # validators=[
        #     DataRequired(message='You need to specify the code for the challenge!')
        # ],
        render_kw={
            "placeholder":"Enter challenge code here...",
            "rows":'10',
        }
    )

class ExamOptionsForm(Form):
    # order = FormField(OrderForm)
    # timer = FormField(TimerForm)
    # question_code = FormField(QuestionCodeForm)
    # options = FormField(OptionsForm)
    order = HiddenField(
        validators=[DataRequired()]
    )
    timer = TimeField(
        label='Timer',
        format='%H:%M:%S',
        validators=[
            DataRequired(message='You need to specify the exam completion time!')
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
        validators=[
            DataRequired(message='You need to specify the code for the challenge!')
        ],
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
    challenge_code = FieldList(FormField(ChallengeCodeForm), min_entries=0)
    challenge_options = FieldList(FormField(ChallengeOptionsForm), min_entries=0)
    exam_code = FieldList(FormField(ExamCodeForm), min_entries=0)
    exam_options = FieldList(FormField(ExamOptionsForm), min_entries=0)


class ExistingContentForm(Form):
    order = HiddenField(
        validators=[DataRequired()]
    )
    content_type = StringField()
    content_id = HiddenField(
        # validators=[
        #     DataRequired(message="Please specify the content id!")
        # ]
    )
    image = FileField(
        label='Picture',
        validators=[
            FileAllowed(photos, 'Only images are allowed!'),
            # FileRequired(message='You need to upload a file!')
        ],
    )
    new_filename = StringField()
    original_filename = StringField()
    content_body = TextAreaField(
        label='Content',
        # validators=[
        #     DataRequired(message='You need to specify the content!')
        # ],
        render_kw={
            "placeholder":"Enter learning content here...",
            "rows":'4',
        }
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
        validators=[
            DataRequired(message='You need to specify the code for the challenge!')
        ],
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
    choices = FieldList(FormField(ChoicesForm), min_entries=10)
    correct = StringField()
    

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
