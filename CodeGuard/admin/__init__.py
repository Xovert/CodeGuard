from flask import current_app, render_template, url_for, Blueprint, session, request, flash, redirect

from CodeGuard.utils.decorators import admin_required

admin = Blueprint('admin', __name__, template_folder='front-end')

# from werkzeug.urls 
from urllib.parse import unquote

from CodeGuard.forms.course import NewModuleForm, NewCourseForm, CourseForm
from CodeGuard.admin import dashboard_catalogue, create
from CodeGuard.admin import details as detail
from CodeGuard.models import (
    db,
    Courses,
    CourseStatus,
    Contents
)

# from CodeGuard.admin import create

@admin.route('/admin', methods=('GET',))
@admin_required
def dashboard():
    username = session.get('username', '')
    drafts = dashboard_catalogue.get_courses(CourseStatus.DRAFT)
    published = dashboard_catalogue.get_courses(CourseStatus.PUBLISHED)
    archived = dashboard_catalogue.get_courses(CourseStatus.ARCHIVED)

    return render_template(
        'admin/dashboard.html', 
        username=username, 
        drafts=drafts,
        published=published,
        archived=archived
    )


@admin.route('/admin/new', methods=('GET', 'POST'))
@admin_required
def add_course():
    if request.method == 'GET':
        username = session.get('username', '')
        return render_template('admin/new_course.html', username=username)
    # return render_template('admin/course_settings.html')
    error = None
    success = None

    form = NewCourseForm()
    if form.validate_on_submit():
        course_name = form.title.data
        course_img = form.logo.data
        course_description = form.description.data
        # course_status = form.visibility.data

        create.new_course(course_name, course_img, course_description)
        success = f'Course {course_name} has been succesfully added!'
        flash(success)
        return redirect(url_for('admin.dashboard'))
    
    error = "<br>".join(
        message for messages in form.errors.values() for message in messages
    )
    flash(error)
    return redirect(url_for('admin.add_course'))



@admin.route('/admin/<path:course_name>', methods=('GET','POST'))
@admin_required
def description(course_name):
    if request.method == 'GET':
        username = session.get('username', '')

        course_name = unquote(course_name)
        course = detail.get_course_fields(course_name)

        usage_mapping = {
            CourseStatus.DRAFT : 'draft',
            CourseStatus.ARCHIVED : 'archived',
            CourseStatus.PUBLISHED : 'published'
        }

        form = CourseForm()
        form.title.data = course.course_name
        form.description.data = course.description
        form.visibility.data = usage_mapping.get(course.status)

        return render_template(
            'admin/course_detail.html',
            username=username,
            form=form,
            original_filename=course.original_filename,
            new_filename=course.new_filename,
        )
    
    error = None
    form = CourseForm()

    usage_mapping = {
        'draft': CourseStatus.DRAFT,
        'archived' : CourseStatus.ARCHIVED,
        'published' : CourseStatus.PUBLISHED
    }
     
    if form.validate_on_submit:
        old_name = course_name
        new_name = form.title.data
        course_img = form.logo.data
        course_description = form.description.data
        course_status = usage_mapping.get(form.visibility.data)

        # if there is an image, update the image
        error, success = detail.update_course(old_name, new_name, course_description, course_status, course_img)

        if error:
            flash(error)
        elif success:
            flash(success)
    else:
        error = "<br>".join(
            message for messages in form.errors.values() for message in messages
        )
    return redirect(url_for('admin.dashboard'))


@admin.route('/admin/<path:course_name>/modules', methods=('GET',))
@admin_required
def modules(course_name):
    username = session.get('username', '')

    course_name = unquote(course_name)
    modules = detail.get_modules(course_name)

    return render_template(
        'admin/module_list.html',
        username=username,
        course_name = course_name,
        modules = modules
    )

@admin.route('/admin/<path:course_name>/new', methods=('GET',))
@admin_required
def add_module(course_name):
    username = session.get('username', '')
    return render_template(
        'admin/new_module.html',
        course_name=unquote(course_name),
        username=username
    )

# template materials
@admin.route('/admin/course/material_learning', methods=('GET',))
def material_learning():
    return render_template('admin/material_learning.html')

@admin.route('/admin/course/material_challenge_code', methods=('GET',))
def material_challenge_code():
    return render_template('admin/material_challenge_code.html')

@admin.route('/admin/course/material_challenge_option', methods=('GET',))
def material_challenge_option():
    return render_template('admin/material_challenge_option.html')

@admin.route('/admin/course/material_exam_code', methods=('GET',))
def material_exam_code():
    return render_template('admin/material_exam_code.html')

@admin.route('/admin/course/material_exam_option', methods=('GET',))
def material_exam_option():
    return render_template('admin/material_exam_option.html')
# template materials