from flask import current_app as app
from flask import render_template, url_for, Blueprint 
from flask import request, session, redirect, abort, flash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError as sqlerror
from werkzeug.datastructures.file_storage import FileStorage
import mimetypes

from CodeGuard.utils.files import upload_file
from CodeGuard.forms.course import NewModuleForm
from CodeGuard.models import (
    db,
    Courses,
    CourseStatus,
    Contents
)

def new_course(name, file: FileStorage, description):
    status = CourseStatus.DRAFT
    course = Courses(
        course_name=name,
        duration=timedelta(days=30).total_seconds(),
        description=description,
        status=status
    )
    db.session.add(course)

    try:
        db.session.flush()
        try:
            upload_image(
                file=file,
                ref_id=course.id,
                # filename=file.filename, 
                usage="course"
            )
        except FileNotFoundError as e:
            print(f"An error occcured while uploading course image:\n\t {e}")
    except sqlerror:
        print(f'An error has occured when adding the course')
        db.session.rollback()
    else:
        db.session.commit()

    return

def upload_image(file: FileStorage, ref_id, usage=None):
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

    upload_file(
        file=file_storage,
        id=ref_id,
        usage=usage,
    )

    return

def add_module(module):
    error = None
    success = None

    db.session.add(module)
    try:
        db.session.flush()
        success = f'Module {module.module_name} has succesfully been added'
        print(success)
        id = module.id
    except sqlerror:
        error = f"Module {module.module_name} already added"
        print(error)
        db.session.rollback()
    # else:
        # db.session.commit()
        # print("committed")
    # JGN COMMMIT DULU, COMMIT PAS AKHIR SETELAH ADD CONTENTS

    return error, success, id


def add_content(content):
    error = None
    success = None

    try:
        db.session.add(content)
        db.session.flush()
        success = f"Content number {content.order} successfully added"
        print(success)
        id = content.id
    except sqlerror:
        error = f"Content number {content.order} already added"
        print(error)
        db.session.rollback()
    else:
        db.session.commit()
        print("committed")

    return error, success, id


def add_questions(question):
    error = None
    success = None

    try:
        db.session.add(question)
        db.session.flush()
        success = f"Question for {question.content_id} succesfully added"
        print(success)
        id = question.id
    except sqlerror:
        error = f'Question for {question.content_id} already added'
        print(error)
        db.session.rollback()
        # jgn commit dulu
    
    return error, success, id

def add_options(option):
    error = None
    success = None

    try:
        db.session.add(option)
        db.session.flush()
        success = f'Option {option.option_text} for {option.question_id} successfully added'
        print(success)
    except sqlerror:
        error = f'Option {option.option_text} for {option.question_id} already added'
        print(error)
        db.session.rollback()
    else:
        db.session.commit()
    return error, success