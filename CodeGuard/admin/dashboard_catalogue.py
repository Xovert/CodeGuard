from flask import session, current_app as app
from sqlalchemy.exc import IntegrityError as sqlerror

from CodeGuard.models import (
    db, 
    Courses, 
    Enrollments,
    Users,
    CourseImages,
    CourseStatus,
    Modules,
    EnrollmentsModules,
)
from CodeGuard.admin import details as detail

def get_courses(status):
    courses = db.session.execute(
        db.select(Courses.course_name, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.status == status)
    ).all()
    
    return courses

def delete_course(course_name):
    success = None
    error = None
    course = detail.get_course(course_name)
    
    if not course:
        error = f"Course not found!"
        return error, success
    
    try:
        db.session.delete(course)
        db.session.flush()
    except sqlerror as e:
        db.session.rollback()
        error = 'An error occured while deleting a course, please try again'
    else:
        db.session.commit()
        success = f'"{course_name}" successfully deleted'
    return error, success