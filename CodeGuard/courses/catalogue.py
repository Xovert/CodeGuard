from flask import session, current_app as app

from CodeGuard.models import (
    db, 
    Courses, 
    Enrollments,
    Users
)
from CodeGuard.courses import courses


def get_catalogue():
    user_uuid = session.get('uuid')
    courses = db.session.scalars(
        db.select(Courses)
        .outerjoin(Courses.enrollment)
        .outerjoin(Enrollments.user.and_(Users.uuid == user_uuid))
        .where(Users.id.is_(None))
    ).all()
    return courses


def get_enrolled():
    user_uuid = session.get('uuid')
    courses = db.session.scalars(
        db.select(Courses)
        .join(Courses.enrollment)
        .join(Enrollments.user)
        .where(Users.uuid == user_uuid)
    ).all()
    return courses
