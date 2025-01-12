from flask import session, current_app as app
from sqlalchemy.orm import joinedload

from CodeGuard.models import (
    db, 
    Contents,
    Courses, 
    Enrollments,
    Users,
    CourseImages,
    Modules,
    EnrollmentsModules,
)
from CodeGuard.courses import courses
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


def get_contents(course_name, module_name, page):
    module_id = get_module_id(module_name)
    course_id = get_course_id(course_name)
    query = (
        db.select(Contents)
        .options(joinedload(Contents.image))
        .where(Contents.module_id == module_id)
    )
    pagination = db.paginate(query, page=page, per_page=1, error_out=False)
    return pagination