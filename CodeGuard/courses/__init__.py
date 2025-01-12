from flask import Blueprint, current_app as app, render_template, url_for, session, make_response, send_file
# from werkzeug.urls 
from urllib.parse import unquote

from CodeGuard.utils.decorators import login_required
from CodeGuard.utils.files import get_file

courses = Blueprint('courses', __name__, template_folder='front-end')
from CodeGuard.courses import catalogue
from CodeGuard.courses import details as detail
from CodeGuard.courses import contents as content

@courses.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    username = session.get('username', '')
    enrolled = catalogue.get_enrolled()
    unenrolled = catalogue.get_catalogue()
    return render_template("course/dashboard.html", username=username, enrolled=enrolled, catalogue=unenrolled)


@courses.route('/course/<path:course_name>', methods=('GET',))
@login_required
def details(course_name):
    course_name = unquote(course_name)
    course = detail.get_course_fields(course_name)
    modules, enrollment_id = detail.get_modules(course_name)
    if enrollment_id:
        detail.update_time(enrollment_id)

    return render_template(
        'course/course_details.html',
        course = course,
        modules = modules
    )

@courses.route('/course/<path:course_name>/module/<path:module_name>', methods=("GET",))
@login_required
def contents(course_name, module_name, page=1):
    course_name = unquote(course_name)
    module_name = unquote(module_name)
    pagination = detail.get_content(course_name, module_name, page)

    return render_template(
        "course/learning.html",
        course_name=course_name,
        module_name=module_name,
        pagination = pagination
    )



# Temporary
@courses.route('/challenge_option')
def challenge_option():
    return render_template('course/challenge_option.html')

@courses.route('/exam')
def exam():
    return render_template('exam.html')

@courses.route('/exam/PHP')
def examPHP():
    return render_template('exam_PHP.html')


@courses.route('/challengePHP')
def challengePHP():
    return render_template('courses/challengePHP.html')

@courses.route('/challengeJS')
def challengeJS():
    return render_template('courses/challengeJS.html')

# @courses.route('/testcodeMirror')
# def testcodeMirror():
#     return render_template('testcodeMirror.html')