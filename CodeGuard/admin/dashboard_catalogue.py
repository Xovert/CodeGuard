from flask import session, current_app as app

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

def get_courses(status):
    courses = db.session.execute(
        db.select(Courses.course_name, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.status == status)
    ).all()
    
    return courses