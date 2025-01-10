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
from sqlalchemy.exc import IntegrityError as sqlerror


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
    try:
        db.session.bulk_save_objects(users)
    except sqlerror:
        print("Users already seeded")
        db.session.rollback()
    else:
        db.session.commit()
    print("Seeded Users.")

def seed_courses():
    courses = [
        Courses(
            course_name='PHP',
            duration=timedelta(days=30).total_seconds(),  # in hours
            description='PHP Secure Coding',
            status=CourseStatus.DRAFT # Assuming 1 means active,
        ),
        Courses(
            course_name='JS',
            duration=timedelta(days=30).total_seconds(),
            description='JS Secure Coding',
            status=CourseStatus.DRAFT
        ),
        # Add more courses as needed
    ]
    try:
        db.session.bulk_save_objects(courses)
    except sqlerror:
        print("Courses already seeded")
        db.session.rollback()
    else:
        db.session.flush()
    print("Seeded Courses.")
    return courses

def seed_modules(module_names, course):
    existing_course = Courses.query.filter_by(course_name = course.course_name).first()
    modules = []

    for i in range(len(module_names)):
        module = Modules(
            course_id=existing_course.id,
            order=i+1,
            module_name=module_names[i]
        )
        modules.append(module)

    try:
        db.session.bulk_save_objects(modules)
    except sqlerror:
        print("Modules already seeded")
        db.session.rollback()
    else:
        db.session.commit()
    print("Seeded Modules.")


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
                "image": "powerful.jpg"
            },
        },
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "image": "memories.jpg"
            }
        },
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "<INPUT HERE>",
                "image": "nyahiru.png"
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": None,
                    "code": "<?php echo('hello world') ?>",
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "The only correct answer", "is_correct": True},
                    ]
                }
            }
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
                "content_body": None,
                "image": None
            },
        },
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "image": "sleeping_shaq.jpg"
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
                    "code": None,
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

    
    for i, module_contents in enumerate(all_contents):
        print(f'Seeding {module_names[i]}...')
        for content in module_contents:
            add_content(**content)

    print("Seeded Contents.")


def add_content(model, attributes: dict, questions=None):
    filename = None
    if attributes.get("image"):
        filename = attributes.pop("image")

    content = model(**attributes)
    try:
        db.session.add(content)
        db.session.flush()
    except sqlerror:
        print(f'Content number:{content.order} already added')
        db.session.rollback()

    if filename:
        upload_image(content.id, filename)
    
    if questions:
        questions["attributes"]["content_id"] = content.id
        add_questions(**questions)
        return
    
    db.session.commit()


def add_questions(model, attributes: dict, options=None):
    question = model(**attributes)

    try:
        db.session.add(question)
        db.session.flush()
    except sqlerror:
        print(f'Question for {question.content_id} already added')
        db.session.rollback()
    
    if options:
        for option in options["rows"]:
            option["question_id"] = question.id
        add_options(**options)
        return
    db.session.commit()

    
def add_options(model, rows):

    for row in rows:
        new_row = model(**row)
        try:
            db.session.add(new_row)
            db.session.flush()
        except sqlerror:
            print(f'Option {new_row.option_text} for {new_row.question_id} already added')
            db.session.rollback()
            return
        
    db.session.commit()
    return



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
    courses = seed_courses()
    seed_modules(module_names, courses[0])
    seed_contents(module_names)
    db.session.close()
    click.echo('Seeded the database')

def init_seed(app):
    app.cli.add_command(seed_all)