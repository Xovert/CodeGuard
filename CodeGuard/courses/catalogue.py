from flask import session, current_app as app

from CodeGuard.models import (
    db, 
    Courses, 
    Enrollments,
    Users,
    CourseImages,
    Modules,
    EnrollmentsModules,
)
from CodeGuard.courses import courses
from CodeGuard.utils.user import get_uuid


def get_catalogue():
    user_uuid = get_uuid()
    courses = db.session.execute(
        db.select(Courses.course_name, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.id.not_in(
            db.select(Courses.id)
            .join(Enrollments)
            .join(Users)
            .where(Users.uuid == user_uuid)
        ))
    ).all()
    return courses


def get_enrolled():
    user_uuid = get_uuid()
    courses = db.session.execute(
        db.select(Courses.course_name, CourseImages.new_filename)
        .join(CourseImages)
        .join(Enrollments)
        .join(Users)
        .where(Users.uuid == user_uuid)
        .order_by(Enrollments.last_accessed_time.desc())
    ).all()
    return courses
