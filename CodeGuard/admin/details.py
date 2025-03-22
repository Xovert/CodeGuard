from flask import session, current_app as app, abort
from werkzeug.datastructures.file_storage import FileStorage
import mimetypes
from sqlalchemy.exc import IntegrityError as sqlerror

from CodeGuard.models import (
    db, 
    Courses, 
    Users,
    CourseImages,
    ContentImages,
    CourseStatus,
    Modules,
    Contents,
    ContentsLearning,
    ContentsChallenges,
    ChallengeQuestions,
    ChallengeOptions
)

from CodeGuard.utils.files import delete_file
from CodeGuard.admin.create import upload_image

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
        db.select(Modules)
        .join(Courses)
        .where(Courses.course_name == course_name)
        .order_by(Modules.order.asc())
    ).scalars().all()
    return modules

def get_module_id(module_name, course_id):
    module = db.session.scalars(
        db.select(Modules.id)
        .where(Modules.module_name == module_name, Modules.course_id == course_id)
    ).first()
    return module

def get_single_module(module_name, course_id):
    return db.session.scalars(
        db.select(Modules)
        .where(Modules.module_name == module_name, Modules.course_id == course_id)
    ).first()

def get_contents(module_id):
    contents = db.session.execute(
        db.select(Contents, ContentImages.new_filename, ContentImages.original_filename, ContentImages.id)
        .outerjoin(ContentImages, Contents.id == ContentImages.content_id)
        .where(Contents.module_id == module_id)
        .order_by(Contents.order.asc())
    ).all()
    return contents

def get_single_content(content_id):
    return db.session.execute(
        db.select(Contents, ContentImages)
        .outerjoin(ContentImages, Contents.id == ContentImages.content_id)
        .where(Contents.id == content_id)
    ).first()

def get_challenge_data(content_id):
    data = db.session.scalars(
        db.select(ChallengeQuestions)
        .join(Contents)
        .where(Contents.id == content_id)
    ).first()
    return data

def get_options(question_id):
    options = db.session.execute(
        db.select(ChallengeOptions.option_text, ChallengeOptions.is_correct)
        .join(ChallengeQuestions)
        .where(ChallengeQuestions.id == question_id)
    ).all()
    return options

def delete_options(question_id):
    try:
        db.session.execute(
            db.delete(ChallengeOptions)
            .where(ChallengeOptions.question_id == question_id)
        )
        db.session.flush()
    except sqlerror as e:
        db.session.rollback()
    return

def delete_content(content_id):
    content, images = get_single_content(content_id)
    try:
        db.session.delete(content)
        db.session.flush()
    except sqlerror as e:
        db.session.rollback()
    else:
        db.session.commit()
    return

def delete_module(module_name, course_id):
    module = get_single_module(module_name, course_id)
    try:
        db.session.delete(module)
        db.session.flush()
    except sqlerror as e:
        db.session.rollback()
    else:
        db.session.commit()
    return

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
        success = f'"{course_name}" has been updated!'

    return error, success

def update_module(new_module_name, old_module_name, course_id):
    error = success = None
    module = get_single_module(old_module_name, course_id)
    
    if module is None:
        abort(404)

    try:
        module.module_name = new_module_name
        db.session.flush()
        success = f"Module name for {old_module_name} has been updated to {module.module_name}"
    except sqlerror as e:
        error = f"An error has occured while updating the module"
        db.session.rollback()
    return error, success, module.id

def update_single_option(question_id, answer):
    error = success = None

    option = db.session.execute(
        db.select(ChallengeOptions)
        .join(ChallengeQuestions)
        .where(ChallengeQuestions.id == question_id)
    ).scalars().first()

    try:
        option.option_text = answer
        db.session.flush()
        success = f"Option for {question_id} has been updated to {option.option_text}"
    except sqlerror as e:
        error = f"An error has occurred while updating the options"
        db.session.rollback()
    
    return error, success