from flask import current_app as app
from flask import render_template, url_for, Blueprint 
from flask import request, session, redirect, abort, flash

from CodeGuard.utils.decorators import admin_required
from CodeGuard.admin import admin
from CodeGuard.utils.uploads import upload_file
from CodeGuard.forms.course import NewCourseForm
from CodeGuard.models import Contents, ContentsLearning, ContentsChallenges

@admin.route('/admin/create/new', methods=("POST",))
@admin_required
def new_course():
    form = NewCourseForm()

    if form.validate_on_submit():
        id = 1
        content_type = form.type.data
        image = form.image.data
        content_body = form.content_body.data


        upload_file(file=image)
        return redirect(url_for('admin.dashboard'))
    
    #     uploads(file)
    abort(404)