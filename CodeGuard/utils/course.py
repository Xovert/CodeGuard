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


def get_enrollment_id(course_id, user_id):
    if course_id is None or user_id is None:
        return None
    return db.session.scalar(
        db.select(Enrollments.id)
        .join(Users)
        .join(Courses)
        .where(Courses.id == course_id)
        .where(Users.id == user_id)
    )

def get_module_id_from_name(module_name):
    if module_name is None:
        return None
    return db.session.scalar(
        db.select(Modules.id)
        .where(Modules.module_name == module_name)
    )

def get_course_id_from_name(course_name):
    if course_name is None:
        return None
    return db.session.scalar(
        db.select(Courses.id)
        .where(Courses.course_name == course_name)
    )

def get_challenge_id_from_option(option_id):
    return db.session.scalar(
        db.select(ChallengeQuestions.content_id)
        .join(Options)
        .where(Options.id == option_id)
    )

def get_enrollment_module_id(enrollment_id, module_id):
    if enrollment_id is None or module_id is None:
        return None
    return db.session.scalar(
        db.select(EnrollmentsModules.id)
        .where(EnrollmentsModules.module_id == module_id)
        .where(EnrollmentsModules.enrollment_id == enrollment_id)
    )

def modules_complete(enrollment_id, status) -> bool:
    enrollment_modules = db.session.execute(
        db.select(EnrollmentsModules)
        .where(EnrollmentsModules.enrollment_id == enrollment_id)
        .where(EnrollmentsModules.status != status)
    ).scalars().all()
    return False if enrollment_modules else True

def course_complete(enrollment_id, status):
    enrollment_status = db.session.scalar(
        db.select(Enrollments.status)
        .where(Enrollments.id == enrollment_id)
    )

    if enrollment_status == status:
        return True
    else:
        return False
