from flask import session, current_app as app
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from werkzeug.datastructures.file_storage import FileStorage
import click
import os

from CodeGuard.auth import bcrypt
from CodeGuard.models import (
    Users,
    CourseStatus,
    Courses,
    Enrollments,
    Modules,
    Images,
    Contents,
    ContentsLearning,
    ContentsChallenges,
    Exams,
    ExamQuestions,
    ChallengeQuestions,
    Options,
    ExamOptions,
    ChallengeOptions,
    db
)


def hash_pass(passes):
    return bcrypt.generate_password_hash(passes)

def seed_users():
    users = [
        Users(
            uuid=uuid4(),
            role='admin',
            fullname='Admin User',
            username='admin',
            password=hash_pass('4dm!n'),  # Ensure you hash passwords appropriately
            email='admin@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='John Doe',
            username='testing',
            password=hash_pass('t3st!ng'),
            email='testing@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        # Add more users as needed
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Seeded Users.")

def seed_courses():
    courses = [
        Courses(
            course_name='PHP',
            duration=30,  # in hours
            description='PHP Secure Coding',
            status="draft" # Assuming 1 means active,
        ),
        Courses(
            course_name='JS',
            duration=30,
            description='JS Secure Coding',
            status="draft"
        ),
        # Add more courses as needed
    ]
    db.session.bulk_save_objects(courses)
    db.session.commit()
    print("Seeded Courses.")

def seed_modules(module_names):
    course = Courses.query.filter_by(id=5).first()
    modules = []

    for i in range(len(module_names)):
        module = Modules(
            course_id=course.id,
            order=i+1,
            module_name=module_names[i]
        )
        modules.append(module)
    db.session.bulk_save_objects(modules)
    db.session.commit()
    print("Seeded Modules.")

contents = {}

def seed_contents(module_names):
    modules = Modules.query.all()
    module_map = {module.module_name: module for module in modules}
    
    all_contents = []
    module = module_map["Broken Access Control"]
    content_module = [
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "<INPUT HERE>",
                "image": 'powerful.jpg'
            },
        },
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 2,
            }
        },
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "<INPUT HERE>",
                "image": None
            },
        }
    ]
    all_contents.append(content_module)

    module = module_map["Cryptographic Failures"]
    content_module = [
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "<INPUT HERE>",
                "image": None
            },
        },
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "image": None
            }
        },
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "<QUESTION HERE>",
                    "code": "<CODE HERE>",
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "option A", "is_correct": True},
                        {"option_text": "option B", "is_correct": False},
                        {"option_text": "option C", "is_correct": False},
                        {"option_text": "option D", "is_correct": False},
                    ]
                }
            }
        }
    ]
    all_contents.append(content_module)
    
    for module_contents in all_contents:
        for content in module_contents:
            add_content(**content)

    print("Seeded Contents.")


def add_content(model, attributes: dict, questions=None):
    filename = None
    if attributes.get("image"):
        filename = attributes.pop("image")

    content = model(**attributes)
    db.session.add(content)
    db.session.flush()

    if filename:
        upload_image(content.id, filename)

    
    if questions:
        questions["attributes"]["content_id"] = content.id
        add_questions(**questions)
        return


def add_questions(model, attributes: dict, options=None):
    question = model(**attributes)

    db.session.add(question)
    db.session.flush()
    if options:
        for option in options["rows"]:
            option["question_id"] = question.id
        add_options(**options)
        return
    db.session.commit()

    
def add_options(model, rows):
    new_rows = []
    for row in rows:
        new_row = model(**row)
        new_rows.append(new_row)

    db.session.bulk_save_objects(new_rows)
    db.session.commit()

def upload_image(content_id, filename):
    from CodeGuard.utils.uploads import upload_file
    import mimetypes
    base = app.root_path
    path = os.path.join(base, 'images', filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f'No such file: {path}')
    
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        # Default to binary stream if MIME type cannot be determined
        mime_type = 'application/octet-stream'

    file_stream = open(path, 'rb')
    file_storage = FileStorage(
        stream=file_stream,
        filename=filename,
        content_type=mime_type
    )

    upload_file(file_storage, content_id)

    

@click.command('seed')
def seed_all():
    module_names = [
        "Broken Access Control",
        "Cryptographic Failures",
    ]
    seed_users()
    seed_courses()
    seed_modules(module_names)
    seed_contents(module_names)
    # seed_images()
    # seed_exams()
    # seed_questions()
    # seed_options()
    # seed_enrollments()
    db.session.close()
    click.echo('Seeded the database')

def init_seed(app):
    app.cli.add_command(seed_all)