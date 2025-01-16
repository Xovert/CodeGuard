from flask import session, current_app as app
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from CodeGuard.models import (
    db, 
    Contents,
    ContentsChallenges,
    ChallengeQuestions,
    Courses, 
    Enrollments,
    Users,
    CourseImages,
    Modules,
    EnrollmentsModules,
    Options,
    ChallengeOptions,
    UsersChallenges
)
from CodeGuard.courses import courses
from CodeGuard import courses as course
from CodeGuard.utils.user import get_uuid
from datetime import datetime, timezone, timedelta
from urllib.parse import quote


def get_module_id(module_name):
    return db.session.scalar(
        db.select(Modules.id)
        .where(Modules.module_name == module_name)
    )


def get_course_id(course_name):
    return db.session.scalar(
        db.select(Courses.id)
        .where(Courses.course_name == course_name)
    )

def get_challenge_id(option_id):
    return db.session.scalar(
        db.select(ChallengeQuestions.content_id)
        .join(Options)
        .where(Options.id == option_id)
    )

def get_contents(course_name, module_name, page):
    module_id = get_module_id(module_name)
    course_id = get_course_id(course_name)
    query = (
        db.select(Contents)
        .join(Modules)
        .where(Contents.module_id == module_id)
        .where(Modules.course_id == course_id)
        .order_by(Contents.order.asc())
    )
    pagination = db.paginate(query, page=page, per_page=1, error_out=False)
    return pagination

def get_enrollment_module_id(course_name, module_name):
    user_uuid = get_uuid()
    course_id = get_course_id(course_name)
    module_id = get_module_id(module_name)
    return db.session.scalar(
        db.select(EnrollmentsModules.id)
        .where(EnrollmentsModules.module_id == module_id)
        .where(EnrollmentsModules.enrollment_id.in_(
            db.select(Enrollments.id)
            .join(Courses)
            .join(Users)
            .where(Users.uuid == user_uuid)
            .where(Courses.id == course_id)
        ))
    )

def check_option(option_id):
    option = db.session.scalar(
        db.select(ChallengeOptions.is_correct)
        .where(ChallengeOptions.id == option_id)
    )
    return bool(option)

def get_correct(content_id) -> str:
    return db.session.scalar(
        db.select(ChallengeOptions.option_text)
        .join(ChallengeQuestions)
        .where(ChallengeQuestions.content_id == content_id)
    )

def get_attempts(course_name, module_name, content_id) -> tuple | None:
    enrollment_module_id = get_enrollment_module_id(course_name, module_name)
    results = db.session.execute(
        db.select(UsersChallenges.attempts, UsersChallenges.isComplete, UsersChallenges.option_selected)
        .where(UsersChallenges.enrollment_module_id == enrollment_module_id)
        .where(UsersChallenges.challenge_id == content_id)
    ).first()
    if results[2]:
        options = db.session.scalar(
            db.select(func.count(ChallengeOptions.id))
            .join(ChallengeQuestions)
            .where(ChallengeQuestions.id.in_(
                db.select(ChallengeOptions.question_id)
                .where(ChallengeOptions.id == results[2])
            ))
        )
        if options == 1:
            option_text = db.session.scalar(
                db.select(ChallengeOptions.option_text)
                .where(ChallengeOptions.id == results[2])
            )
            results = (results[0], results[1], option_text)
    print(results)
    return results

def check_attempts(course_name, module_name, option_id=None, content_id=None):
    if option_id:
        challenge_id = get_challenge_id(option_id)
    if content_id:
        challenge_id = content_id
    enrollment_module_id = get_enrollment_module_id(course_name, module_name)
    attempts = db.session.scalar(
        db.select(UsersChallenges.attempts)
        .where(UsersChallenges.enrollment_module_id == enrollment_module_id)
        .where(UsersChallenges.challenge_id == challenge_id)
    )
    return bool(attempts > 0)

def update_attempts(course_name, module_name, option_id=None, content_id=None):
    if option_id:
        challenge_id = get_challenge_id(option_id)
    if content_id:
        challenge_id = content_id
    enrollment_module_id = get_enrollment_module_id(course_name, module_name)
    userchallenge = db.session.scalar(
        db.select(UsersChallenges)
        .where(UsersChallenges.enrollment_module_id == enrollment_module_id)
        .where(UsersChallenges.challenge_id == challenge_id)
    )
    userchallenge.attempts -= 1
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

def get_option(content_id):
    return db.session.scalar(
        db.select(ChallengeOptions.id)
        .join(ChallengeQuestions)
        .join(ContentsChallenges)
        .where(ContentsChallenges.id == content_id)
    )
    

def update_complete(course_name, module_name, option_id=None, content_id=None):
    if option_id:
        challenge_id = get_challenge_id(option_id)
    if content_id:
        challenge_id = content_id
    enrollment_module_id = get_enrollment_module_id(course_name, module_name)
    userchallenge = db.session.scalar(
        db.select(UsersChallenges)
        .where(UsersChallenges.enrollment_module_id == enrollment_module_id)
        .where(UsersChallenges.challenge_id == challenge_id)
    )
    userchallenge.isComplete = True
    if content_id:
        userchallenge.option_selected = get_option(content_id)
    if option_id:
        userchallenge.option_selected = option_id
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

def update_progress(course_name, module_name, page):
    module_id = get_module_id(module_name)
    enrollment_id = course.detail.get_enrollment_id(get_uuid(), course_name)
    enrollment_module = db.session.scalars(
        db.select(EnrollmentsModules)
        .join(Enrollments)
        .join(Modules)
        .where(Modules.id == module_id)
        .where(Enrollments.id == enrollment_id)
    ).first()
    
    if page == -1:
        enrollment_module.progress = -1
    elif page > enrollment_module.progress:
        enrollment_module.progress += 1
    elif page < enrollment_module.progress:
        enrollment_module.progress -= 1
    else:
        return
    
    try:
        db.session.commit()
    except Exception as e:
        print(f'Error: {e}')
        db.session.rollback()
    return

def unlock_next_module(course_name, module_name):
    enrollment_id = course.detail.get_enrollment_id(get_uuid(), course_name)
    order = db.session.scalar(
        db.select(Modules.order)
        .where(Modules.module_name == module_name)
    )
    next_module = db.session.scalars(
        db.select(EnrollmentsModules)
        .join(Modules)
        .where(EnrollmentsModules.enrollment_id == enrollment_id)
        .where(Modules.id.in_(
            db.select(Modules.id)
            .where(Modules.order == order+1)
        ))
    ).first()
    next_module.progress = 1
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Error: {e}')

def sanitize_input(input_text):
    input_text = input_text.strip()

    if len(input_text) > 255:
        return input_text, 'Input too large'
    if len(input_text) == 0 :
        return input_text, 'Input is empty'
    if b'\x00' in input_text.encode('utf-8'):
        return input_text, 'Null byte detected'

    return input_text, None
    