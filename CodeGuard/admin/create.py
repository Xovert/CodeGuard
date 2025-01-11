from flask import current_app as app
from flask import render_template, url_for, Blueprint 
from flask import request, session, redirect, abort, flash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from CodeGuard.utils.decorators import admin_required
from CodeGuard.admin import admin
from CodeGuard.utils.files import upload_file
from CodeGuard.forms.course import NewCourseForm
from CodeGuard.models import (
    db,
    Courses,
    CourseStatus,
    Contents
)

@admin.route('/admin/create/new', methods=("POST",))
@admin_required
def new_course():
    form = NewCourseForm()

    if form.validate_on_submit():
        content_type = form.type.data
        image = form.image.data
        content_body = form.content_body.data
        course_name = form.course_name.data
        description = form.description.data

        course = Courses(
            course_name = course_name,
            duration = timedelta(days=30).total_seconds(),
            description = description,
            status = CourseStatus.DRAFT
        )
        db.session.add(course)
        try:
            db.session.flush()
            upload_file(file=image, usage='course', id=course.id)
        except IntegrityError:
            db.session.rollback()
        else:
            db.session.commit()

        return redirect(url_for('admin.dashboard'))
    
    #     uploads(file)
    abort(404)