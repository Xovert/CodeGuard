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
        .order_by(Enrollments.last_accessed_time.asc())
    ).all()
    return courses


def update_time():
    pass


def get_modules(course_name):
    user_uuid = get_uuid()
    modules = db.session.execute(
        db.select(Modules.module_name, Modules.order, EnrollmentsModules.progress)
        .join(EnrollmentsModules, Modules.id == EnrollmentsModules.module_id)
        .join(Enrollments, Enrollments.id == EnrollmentsModules.enrollment_id)
        .join(Users, Users.id == Enrollments.user_id)
        .join(Courses, Courses.id == Modules.course_id)
        .where(Users.uuid == user_uuid)
        .where(Courses.course_name == course_name)
        .order_by(Modules.order.asc())
    ).all()
    return modules


def get_course_fields(course_name):
    course = db.session.execute(
        db.select(Courses.course_name, Courses.description, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.course_name == course_name)
    ).first()
    return course
