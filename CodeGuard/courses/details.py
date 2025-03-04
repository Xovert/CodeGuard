import math
from flask import g, current_app as app
from sqlalchemy import func, case

from CodeGuard.models import (
    db, 
    Courses, 
    Enrollments,
    CourseImages,
    Modules,
    EnrollmentsModules,
    Contents,
    UsersContents,
    Exams
)
from CodeGuard.models.enums import CompletionStatus, CourseStatus
from datetime import datetime, timezone, timedelta
log = app.logger

def update_time():
    if g.enrollment_id is None:
        return
    
    enrollment = db.session.scalars(
        db.select(Enrollments)
        .where(Enrollments.id == g.enrollment_id)
    ).first()
    enrollment.last_accessed_time = datetime.now(tz=timezone(timedelta(hours=7)))
    try:
        db.session.commit()
    except:
        db.session.rolback()


def get_course_fields():
    course = db.session.execute(
        db.select(Courses.course_name, Courses.description, CourseImages.new_filename)
        .join(CourseImages)
        .where(Courses.id == g.course_id)
    ).first()
    return course


def get_modules():
    return db.session.execute(
        db.select(Modules.module_name, Modules.order, EnrollmentsModules.progress, EnrollmentsModules.status)
        .join(Courses)
        .outerjoin(
            EnrollmentsModules,
            (Modules.id == EnrollmentsModules.module_id) & 
            (EnrollmentsModules.enrollment_id == g.enrollment_id)
        )
        .where(Courses.id == g.course_id)
        .order_by(Modules.order.asc())
    ).all()


def get_curr_module():
    return db.session.scalar(
        db.select(EnrollmentsModules)
        .where(EnrollmentsModules.id == g.enrollment_module_id)
    )


def get_next_module():
    current_order = db.session.scalar(
        db.select(Modules.order)
        .where(Modules.id == g.module_id)
    )
    enrollment = db.session.execute(
        db.select(EnrollmentsModules)
        .join(Modules)
        .where(EnrollmentsModules.enrollment_id == g.enrollment_id)
        .where(Modules.order == current_order+1)
    ).scalars().first()
    return enrollment


def get_prev_module():
    current_order = db.session.scalar(
        db.select(Modules.order)
        .where(Modules.id == g.module_id)
    )
    if current_order == 1:
        return EnrollmentsModules(status=CompletionStatus.COMPLETE)
    
    return db.session.execute(
        db.select(EnrollmentsModules)
        .join(Modules)
        .where(EnrollmentsModules.enrollment_id == g.enrollment_id)
        .where(Modules.order == current_order-1)
    ).scalars().first()


def unlock_module(module: Modules):
    module.status = CompletionStatus.STARTED
    module.users_contents[0].status = CompletionStatus.STARTED
    module.progress = 1
    module.enrollment.progress += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log.error(f'Error: {e}')

    
def get_percentage():
    if g.enrollment_id is None:
        return -1
    
    stmt = (
        db.select(
            func.count(Modules.id).label('total_modules'),
            func.sum(
                case(
                    (EnrollmentsModules.status == CompletionStatus.COMPLETE, 1),
                    else_=0
                )
            ).label('finished')
        )
        .select_from(Modules)
        .join(
            EnrollmentsModules,
            (Modules.id == EnrollmentsModules.module_id) &
            (EnrollmentsModules.enrollment_id == g.enrollment_id),
            isouter=True  # so all modules get counted
        )
        .where(Modules.course_id == g.course_id)
    )
    
    row = db.session.execute(stmt).one()
    total_modules = row.total_modules
    finished = row.finished if row.finished else 0

    enrollment: Enrollments = db.session.scalar(
        db.select(Enrollments)
        .where(Enrollments.id == g.enrollment_id)
    )

    if enrollment.exam:
        total_modules += 1

    if total_modules == 0:
        return 0
    
    if g.courseComplete:
        return 100
    
    return math.ceil((finished / total_modules) * 100)

def enroll_course():
    error = None
    tz = timezone(timedelta(hours=7))
    curr_time = datetime.now(tz=tz)
    enrollment = Enrollments(
        user_id=g.user_id,
        course_id=g.course_id,
        enrollment_date=curr_time,  # Localized datetime
        status=CompletionStatus.STARTED,
        progress=0,
        last_accessed_time=curr_time.timetz() # Time only, extracted from datetime
    )
    course = db.session.scalar(
        db.select(Courses)
        .where(Courses.id == g.course_id)
    )

    import random
    exams:Exams = course.exams
    if exams:
        exam: Exams = random.choice(exams)
        enrollment.exam_id = exam.id

    db.session.add(enrollment)
    try:
        db.session.flush()
        g.enrollment_id = enrollment.id
    except:
        error = "User is already enrolled to course!"
        db.session.rollback()
        return error
    else:
        db.session.commit()
    
    modules = db.session.execute(
        db.select(Modules)
        .where(Modules.course_id == g.course_id)
        .order_by(Modules.order)
    ).scalars().all()

    if not modules:
        log.error("No Modules")
        return

    enrollments_modules = [
        {
            "enrollment_id": g.enrollment_id,
            "module_id": module.id,
            "progress": 0
        }
        for module in modules
    ]
    enrollments_modules[0]["status"] = CompletionStatus.STARTED
    enrollments_modules[0]["progress"] = 1

    try:
        enrollments_modules_ids = db.session.execute(
            db.insert(EnrollmentsModules).returning(EnrollmentsModules.id, EnrollmentsModules.module_id, sort_by_parameter_order=True),
            enrollments_modules
        )
    except:
        db.session.rollback()
        error = "Enrollment Failed!, Modules not Exist!"
        return error
    else:
        db.session.commit()


    users_contents = []
    for enrollment_module_id, module_id in enrollments_modules_ids.all():
        contents = db.session.execute(
            db.select(Contents)
            .where(Contents.module_id == module_id)
            .order_by(Contents.order)
        ).scalars().all()

        if not contents:
            continue
        
        users_contents.extend(
            [
                {
                    "enrollment_module_id": enrollment_module_id,
                    "content_id": content.id,
                }
                for content in contents
            ]
        )

    if not users_contents:
        log.error('No contents found!')
        return

    users_contents[0]["status"] = CompletionStatus.STARTED
    try:
        db.session.execute(
            db.insert(UsersContents),users_contents
        )
    except:
        db.session.rollback()
        error = "Contents doesn't exist!"
        return error
    else:
        db.session.commit()
    
    return error

def get_exam():
    return db.session.scalar(
        db.select(Exams)
        .join(Enrollments)
        .where(Enrollments.id == g.enrollment_id)
    )
