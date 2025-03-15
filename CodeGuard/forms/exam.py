from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms import Form
from wtforms.validators import (
    DataRequired,
    Regexp,
    Length,
    ValidationError,
    NumberRange,
    ReadOnly
)
from wtforms.fields import (
    SubmitField,
    SelectField,
    TextAreaField,
    StringField,
    TimeField,
    FormField,
    FieldList,
    RadioField,
    HiddenField,
    IntegerField
)

class DurationForm(Form):
    hours = IntegerField(
        label="H",
        name='hours',
        validators=[
            NumberRange(min=0, max=99, message="Number must at least be 0")
        ],
        render_kw={
            "placeholder": "HH"
        },
    )

    minutes = IntegerField(
        label="M",
        name='minutes',
        validators=[
            NumberRange(min=0, max=59, message='Minutes are between 0 to 59')
        ],
        render_kw={
            "placeholder": "MM"
        },
    )

    def validate(self):
    # First let WTForms run the default validators
        initial_validation = super().validate()
        if not initial_validation:
            return False

        # If both hours and minutes are zero, that's invalid
        if (self.hours.data or 0) == 0 and (self.minutes.data or 0) == 0:
            self.hours.errors.append("Duration cannot be zero.")
            return False

        return True

class ExamForm(FlaskForm):
    exam = StringField(
        label='Exam Name',
        name='exam-name',
        validators=[
            DataRequired(message='You need to specify the exam name!'),
            ReadOnly()
        ],
        render_kw={
            "placeholder": "Enter the exam name here..."
        }
    )
    duration = FormField(
        form_class=DurationForm,
        label='Duration',
    )
    todo = IntegerField(
        label='Todo',
        validators=[
            NumberRange(min=1, max=10, message='Todo must be between 1 and 10!'),
            DataRequired(message='You need to specify how much todo there is in the exam!'),
        ],
        render_kw={
            "placeholder": "0"
        }
    )
    question = TextAreaField(
        label='Question',
        validators=[
            DataRequired(message='You need to specify the question for the exam!'),
            Length(min=1, max=500, message="Question must be between 1 to 500 characters!")
        ],
        render_kw={
            "placeholder":"Enter exam question here...",
            "rows":'2',
        },
        filters=[str.strip,],
        default=''
    )
    code = TextAreaField(
        label='Code',
        validators=[
            DataRequired(message='You need to specify the code for the exam!'),
        ],
        render_kw={
            "placeholder":"Enter exam code here...",
            "rows":'10',
        }
    )
