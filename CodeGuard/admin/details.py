# import math
from flask import session, current_app as app
from werkzeug.datastructures.file_storage import FileStorage
import mimetypes
from sqlalchemy.exc import IntegrityError as sqlerror
# from sqlalchemy import func

from CodeGuard.models import (
    db, 
    Courses, 
    Enrollments,
    Users,
    CourseImages,
    ContentImages,
    CourseStatus,
    Modules,
    EnrollmentsModules,
    Contents,
    ContentsLearning,
    ContentsChallenges,
    ChallengeQuestions,
    ChallengeOptions
)

from CodeGuard.utils.files import get_file, upload_file, delete_file
from CodeGuard.admin.create import upload_image

# from CodeGuard.courses import courses
# from CodeGuard import courses as course
# from CodeGuard.utils.user import get_uuid
# from datetime import datetime, timezone, timedelta
# from urllib.parse import quote

def get_course(course_name):
    course = db.session.scalars(
        db.select(Courses)
        .where(Courses.course_name == course_name)
    ).first()
    return course

def get_course_fields(course_name):
    course = db.session.execute(
        db.select(Courses.course_name, Courses.description, CourseImages.new_filename, CourseImages.original_filename, Courses.status)
        .join(CourseImages)
        .where(Courses.course_name == course_name)
    ).first()
    return course


def get_modules(course_name):
    modules = db.session.execute(
        db.select(Modules.module_name, Modules.order)
        .join(Courses)
        .where(Courses.course_name == course_name)
        .order_by(Modules.order.asc())
    ).all()
    return modules

def get_module_id(module_name):
    module = db.session.scalars(
        db.select(Modules.id)
        .where(Modules.module_name == module_name)
    ).first()
    return module

def get_contents(module_id):
    # contents = db.session.execute(
    #     db.select(Contents)
    #     .join(Modules)
    #     .where(Modules.module_name == module_name)
    #     .order_by(Contents.order.asc())
    # ).all()

    contents = db.session.execute(
        db.select(Contents, ContentImages.new_filename, ContentImages.original_filename)
        .outerjoin(ContentImages, Contents.id == ContentImages.content_id)
        .where(Contents.module_id == module_id)
        .order_by(Contents.order.asc())
    ).all()
    return contents

def get_challenge_data(content_id):
    data = db.session.execute(
        db.select(ChallengeQuestions.id, ChallengeQuestions.question_text, ChallengeQuestions.code)
        .join(Contents)
        .where(Contents.id == content_id)
    ).first()
    return data
    # def get_correct(content_id) -> str:
    # return db.session.scalar(
    #     db.select(ChallengeOptions.option_text)
    #     .join(ChallengeQuestions)
    #     .where(ChallengeQuestions.content_id == content_id)
    # )

def get_options(question_id):
    options = db.session.execute(
        db.select(ChallengeOptions.option_text, ChallengeOptions.is_correct)
        .join(ChallengeQuestions)
        .where(ChallengeQuestions.id == question_id)
    ).all()
    return options

def update_course(old_name, course_name, course_description, course_status, course_img:FileStorage=None):
    course, images = (
        db.session.query(Courses, CourseImages)
        .join(CourseImages)
        .filter(Courses.course_name == old_name)
        .first()
    )
    error = None
    success = None

    if not course:
        error = f"Course not found!"
        return error, success

    # visibility validation
    if (course.status == CourseStatus.PUBLISHED or course.status == CourseStatus.ARCHIVED) and course_status == CourseStatus.DRAFT:
        error = "A published or archived course cannot go back as a draft!"
    elif course.status == CourseStatus.DRAFT and course_status == CourseStatus.ARCHIVED:
        error = "A draft needs to be published first before being archived!"
    if error:
        return error, success

    try:
        course.course_name = course_name
        course.description = course_description
        course.status = course_status

        # if the image is changed
        if (course_img):
            try:
                delete_file(images.id)
                upload_image(
                    file=course_img,
                    ref_id=course.id,
                    usage='course',
                )
            except FileNotFoundError as e:
                error = f"An error occcured while uploading course image:\n\t {e}"
                db.session.rollback()

    except sqlerror:
        error = f'An error has occured when adding the course'
        db.session.rollback()
        
    else:
        db.session.commit()
        success = f"{course_name} has been updated!"

    return error, success


def update_image(file: FileStorage, ref_id, usage=None, location=None):
    filename = file.filename
    file_stream = file.stream
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        # Default to binary stream if MIME type cannot be determined
        mime_type = 'application/octet-stream'

    file_storage = FileStorage(
        stream=file_stream,
        filename=filename,
        content_type=mime_type
    )

    ret = upload_file(
        file=file_storage,
        id=ref_id,
        usage=usage,
        location=location
    )

    print(ret)
    return
