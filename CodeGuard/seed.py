import time
import click
import os
from flask import session, current_app as app
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from werkzeug.datastructures.file_storage import FileStorage
from sqlalchemy.exc import IntegrityError as sqlerror
from freezegun import freeze_time

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
            username='john',
            password=hash_pass('j0hn#'),
            email='john@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Jane Doe',
            username='jane',
            password=hash_pass('j@ne#'),
            email='jane@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Amandoos',
            username='scaramochi',
            password=hash_pass('sc@ram0ch!'),
            email='nathania@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Greyson',
            username='grey',
            password=hash_pass('tokora'),
            email='kora@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Sir Ian Fleming',
            username='fl3ming_hot',
            password=hash_pass('007b!nd'),
            email='bond007@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        # Add more users as needed
    ]

    for user in users:
        db.session.add(user)
        try:
            db.session.flush()
            print(f'User {user.username} has succesfully been seeded')
        except sqlerror:
            print(f"User {user.username} already seeded")
            db.session.rollback()
        else:
            db.session.commit()
    print("Seeded Users.")

def seed_courses():
    courses = [ 
        {
            "course": Courses(
            course_name='PHP',
            duration=timedelta(days=30).total_seconds(),  # in hours
            duration=timedelta(days=30).total_seconds(),  # in hours
            description='PHP Secure Coding',
            status=CourseStatus.DRAFT # Assuming 1 means active,
            ),
            "image": "php.png"
        },
        {
            "course": Courses(
                course_name='JS',
                duration=timedelta(days=30).total_seconds(),
                description='JS Secure Coding',
                status=CourseStatus.DRAFT
            ),
            "image": "js.png"
        },
        {
            "course": Courses(
                course_name='Python',
                duration=timedelta(days=30).total_seconds(),
                description='Hmm yes yes snake~',
                status=CourseStatus.PUBLISHED
            ),
            "image": "nyahiru.png"
        },
        {
            "course": Courses(
                course_name='C/C++',
                duration=timedelta(days=30).total_seconds(),
                description='How to shoot yourself in the foot',
                status=CourseStatus.ARCHIVED
            ),
            "image": "powerful.jpg"
        }
        # Add more courses as needed
    ]

    for course in courses:
        db.session.add(course["course"])
        try:
            db.session.flush()
            print(f'Course {course["course"].course_name} has succesfully been seeded')
            upload_image(
                ref_id=course["course"].id,
                filename=course["image"], 
                usage="course"
            )
        except sqlerror:
            print(f"Course {course["course"].course_name} already seeded")
            db.session.rollback()
        else:
            db.session.commit()

    print("Seeded Courses.")
    return courses


def seed_modules(module_names):
    existing_course = db.session.scalars(
        db.select(Courses)
        .where(Courses.course_name == "PHP")
    ).first()

    modules = []

    for i in range(len(module_names)):
        module = Modules(
            course_id=existing_course.id,
            course_id=existing_course.id,
            order=i+1,
            module_name=module_names[i]
        )
        db.session.add(module)
        try:
            db.session.flush()
            print(f'Module {module.module_name} has succesfully been seeded')
        except sqlerror:
            print(f"Module {module.module_name} already seeded")
            db.session.rollback()
        else:
            db.session.commit()

    print("Seeded Modules.")


def seed_contents(module_names):
    modules = db.session.scalars(db.select(Modules)).all()
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
                "image": "powerful.jpg"
            },
        },
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "image": "memories.jpg"
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
        db.session.commit()
        return

    if filename:
        upload_image(content.id, filename, "content")
    
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
        else:
            db.session.commit()
    
    return



def upload_image(ref_id, filename, usage=None):
    from CodeGuard.utils.files import upload_file
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

    upload_file(
        file=file_storage, 
        id=ref_id, 
        usage=usage
    )


def seed_enrollments():
    courses = db.session.scalars(db.select(Courses)).all()
    users = db.session.scalars(
        db.select(Users)
        .where(Users.role != 'admin')
    ).all()

    if not users or not courses:
        print("No users or courses found. Cannot seed enrollments.")
        return

    enrollments = []
    import random
    for _ in range(10):
        # Pick a random user and a random course
        user = random.choice(users)
        course = random.choice(courses)

        # Create an Enrollment object
        tz = timezone(timedelta(hours=7))
        curr_time = datetime.now(tz=tz)
        enrollment = Enrollments(
            user_id=user.id,
            course_id=course.id,
            enrollment_date=curr_time,  # Localized datetime
            progress=0,
            last_enrolled_time=curr_time.timetz() # Time only, extracted from datetime
        )
        db.session.add(enrollment)
        try:
            db.session.flush()
            print(f"Enrollment for User {enrollment.user_id}; Course {enrollment.course_id} success")
        except sqlerror:
            db.session.rollback()
            print(f"Enrollment for User {enrollment.user_id}; Course {enrollment.course_id} failed")
        else:
            db.session.commit()

    return


def seed_exams():
    pass


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
    seed_enrollments()
    seed_exams()
    db.session.close()
    click.echo('Seeded the database')


@click.command('query')
@click.argument('id', type=int)
def test_query(id):
    user_uuid = db.session.scalar(db.select(Users.uuid).where(Users.id == id))
    # stmt = (
    #     db.select(Courses)
    #     .outerjoin(Enrollments)
    #     .outerjoin(Users)
    #     .where(Users.uuid == user_uuid)
    #     .where(Enrollments.user_id == None)
    # )
    stmt = (
        db.select(Courses)
        .outerjoin(Courses.enrollment)
        .outerjoin(Enrollments.user.and_(Users.uuid == user_uuid))
        .where(Users.id == None)  # Filter for unenrolled courses
    )
    courses = db.session.scalars(
        stmt
    ).all()
    print(stmt)
    print(courses)

def init_seed(app):
    app.cli.add_command(seed_all)
    app.cli.add_command(test_query)