from flask import g

from CodeGuard.models import (
    db, 
    Courses, 
    Enrollments,
    Users,
    CourseImages,
)


def get_catalogue():
    courses = db.session.execute(
        db.select(Courses.course_name, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.id.not_in(
            db.select(Courses.id)
            .join(Enrollments)
            .join(Users)
            .where(Users.id == g.user_id)
        ))
    ).all()
    return courses


def get_enrolled():
    courses = db.session.execute(
        db.select(Courses.course_name, CourseImages.new_filename)
        .join(CourseImages)
        .join(Enrollments)
        .join(Users)
        .where(Users.id == g.user_id)
        .order_by(Enrollments.last_accessed_time.desc())
    ).all()
    return courses
