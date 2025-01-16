import math
from flask import session, current_app as app
from sqlalchemy import func

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
from CodeGuard import courses as course
from CodeGuard.utils.user import get_uuid
from datetime import datetime, timezone, timedelta
from urllib.parse import quote


def update_time(id):
    enrollment = db.session.scalars(
        db.select(Enrollments)
        .where(Enrollments.id == id)
    ).first()
    enrollment.last_accessed_time = datetime.now(tz=timezone(timedelta(hours=7)))
    try:
        db.session.commit()
    except:
        db.session.rolback()


def get_enrollment_id(user_uuid, course_name):
    enrollment_id = db.session.scalars(
        db.select(Enrollments.id)
        .join(Users)
        .join(Courses)
        .where(Users.uuid == user_uuid)
        .where(Courses.course_name == course_name)
    ).first()
    return enrollment_id


def get_modules(course_name):
    user_uuid = get_uuid()
    enrollment_id = get_enrollment_id(user_uuid, course_name)
    if enrollment_id:
        modules = db.session.execute(
            db.select(Modules.module_name, Modules.order, EnrollmentsModules.progress)
            .join(EnrollmentsModules, Modules.id == EnrollmentsModules.module_id)
            .where(EnrollmentsModules.enrollment_id == enrollment_id)
            .order_by(Modules.order.asc())
        ).all()
    else:
        modules = db.session.execute(
            db.select(Modules.module_name, Modules.order, 0)
            .join(Courses)
            .where(Courses.course_name == course_name)
            .order_by(Modules.order.asc())
        ).all()
    return modules, enrollment_id


def get_course_fields(course_name):
    course = db.session.execute(
        db.select(Courses.course_name, Courses.description, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.course_name == course_name)
    ).first()
    return course

def get_percentage(course_name):
    user_uuid = get_uuid()
    enrollment_id = get_enrollment_id(user_uuid, course_name)
    course_id = course.content.get_course_id(course_name)
    total_modules = db.session.scalar(
        db.select(func.count(Modules.id))
        .where(Modules.course_id == course_id)
    )
    if enrollment_id and total_modules:
        finished = db.session.scalar(
            db.select(func.count(EnrollmentsModules.id))
            .join(Modules, Modules.id == EnrollmentsModules.module_id)
            .where(EnrollmentsModules.enrollment_id == enrollment_id)
            .where(EnrollmentsModules.progress == -1)
        )
    else:
        return -1
    return math.ceil((finished/total_modules) * 100)