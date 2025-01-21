from flask import current_app, render_template, url_for, Blueprint, session

from CodeGuard.utils.decorators import admin_required

admin = Blueprint('admin', __name__, template_folder='front-end')

from CodeGuard.admin import create
from CodeGuard.forms.course import NewCourseForm


@admin.route('/admin', methods=('GET',))
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/admin/course', methods=('GET',))
@admin_required
def add_course():
    # return render_template('admin/course_settings.html')
    return render_template('admin/new_course.html')

@admin.route('/admin/module', methods=('GET',))
@admin_required
def add_module():
    return render_template('admin/new_module.html')

@admin.route('/admin/course/module', methods=('GET',))
@admin_required
def module():
    return render_template('admin/module_list.html')

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