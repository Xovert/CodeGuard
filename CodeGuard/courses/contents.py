from flask import g, current_app as app
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
    UsersContents
)
from CodeGuard.models.enums import CompletionStatus
from CodeGuard.courses import courses
from CodeGuard import courses as course
from CodeGuard.utils.user import get_uuid
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
log = app.logger

def get_status(id):
    return db.session.scalar(
        db.select(UsersContents.status)
        .where(UsersContents.enrollment_module_id == g.enrollment_module_id)
        .where(UsersContents.content_id == id)
    )


def get_progress():
    return db.session.scalar(
        db.select(EnrollmentsModules.progress)
        .where(EnrollmentsModules.module_id == g.module_id)
        .where(EnrollmentsModules.enrollment_id == g.enrollment_id)
    )


def update_progress(page):
    enrollment_module = db.session.scalar(
        db.select(EnrollmentsModules)
        .where(EnrollmentsModules.id == g.enrollment_module_id)
    )
    enrollment_module.progress = page

    try:
        db.session.commit()
    except Exception as e:
        log.error(f'Error: {e}')
        db.session.rollback()
    return


def get_content_status(page):
    if page <= 0:
        return UsersContents(status=CompletionStatus.COMPLETE)
    return db.session.scalar(
        db.select(UsersContents)
        .join(Contents)
        .where(UsersContents.enrollment_module_id == g.enrollment_module_id)
        .where(Contents.order == page)
    )


def get_contents(page):
    if page < 0: 
        return None
    query = (
        db.select(Contents)
        .join(UsersContents)
        .where(UsersContents.enrollment_module_id == g.enrollment_module_id)
        .order_by(Contents.order.asc())
    )
    pagination = db.paginate(query, page=page, per_page=1, error_out=False)
    return pagination


def get_user_content(content_id):
    users_contents = db.session.scalar(
        db.select(UsersContents)
        .where(UsersContents.enrollment_module_id == g.enrollment_module_id)
        .where(UsersContents.content_id == content_id)
    )
    return users_contents


def set_status(content: UsersContents, status:CompletionStatus=None):
    content.status = status if status else content.status.next_status
    try:
        db.session.commit()
    except Exception as e:
        log.error(f"Error {e}")
        db.session.rollback()

    
def check() -> CompletionStatus:
    enrollment_module = db.session.scalar(
        db.select(EnrollmentsModules)
        .where(EnrollmentsModules.id == g.enrollment_module_id)
    )
    if enrollment_module.status == CompletionStatus.COMPLETE:
        return None

    users_contents = enrollment_module.users_contents
    for user_content in users_contents:
        if user_content.status != CompletionStatus.COMPLETE:
            return None
        
    enrollment_module.status = CompletionStatus.COMPLETE

    try:
        db.session.commit()
    except Exception as e:
        log.error(f'Fails for whatever reason: {e}')
        db.session.rollback()

    return CompletionStatus.COMPLETE


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


def update_user_content(user_content: UsersContents):
    try:
        db.session.commit()
    except Exception as e:
        log.error(f'error: {e}')
        db.session.rollback()


def sanitize_input(input_text):
    input_text = input_text.strip()

    if len(input_text) > 255:
        return input_text, 'Input too large'
    if len(input_text) == 0 :
        return input_text, 'Input is empty'
    if b'\x00' in input_text.encode('utf-8'):
        return input_text, 'Null byte detected'

    return input_text, None
    