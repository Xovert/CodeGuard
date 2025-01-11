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



