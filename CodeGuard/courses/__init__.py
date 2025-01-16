from flask import (
    Blueprint, 
    current_app as app, 
    render_template, 
    url_for, 
    session,
    make_response, 
    send_file,
    request,
    abort
)
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
    percentage = detail.get_percentage(course_name)

    return render_template(
        'course/course_details.html',
        course = course,
        modules = modules,
        percentage = percentage
    )

@courses.route('/course/<path:course_name>/module/<path:module_name>', methods=('GET',))
@login_required
def contents(course_name, module_name):
    page = request.args.get("page", 1, type=int)
    course_name = unquote(course_name)
    module_name = unquote(module_name)
    pagination = content.get_contents(course_name, module_name, page)
    if page == pagination.pages:
        content.update_progress(course_name, module_name, -1)
        content.unlock_next_module(course_name, module_name)
    else:
        content.update_progress(course_name, module_name, page)
    
    return render_template(
        "course/contents.html",
        course_name=course_name,
        module_name=module_name,
        pagination = pagination
    )

@courses.route("/course/<path:course_name>/module/<path:module_name>/get-attempts", methods=("GET",))
@login_required
def get_attempts(course_name, module_name):
    course_name = unquote(course_name)
    module_name = unquote(module_name)
    content_id = request.args.get('content')
    attempts, isComplete, selected = content.get_attempts(course_name, module_name, content_id)
    if attempts >= 0 or isComplete:
        data = {
            'attempts': attempts,
            'isComplete': isComplete,
        }
        if selected:
            data['selected'] = selected
        return data
    abort(404)

@courses.route('/course/<path:course_name>/module/<path:module_name>/check', methods=("POST",))
@login_required
def check_challenge(course_name, module_name):
    course_name = unquote(course_name)
    module_name = unquote(module_name)
    request_data = request.json
    if request_data["type"] == "options":
        answer = int(request_data["answer"])
        if content.check_attempts(course_name, module_name, option_id=answer):
            status = content.check_option(answer)
            if status == False:
                content.update_attempts(course_name, module_name, option_id=answer)
            if status == True:
                content.update_complete(course_name, module_name, option_id=answer)
            return {'status': status,}
        
    elif request_data["type"] == "input_text":
        content_id = int(request_data['content'])
        if content.check_attempts(course_name, module_name, content_id=content_id):
            input_text = request_data['answer']
            correct = content.get_correct(content_id)
            sanitized_input, error = content.sanitize_input(input_text)
            if error:
                return {
                    'status': "error",
                    'errror': error
                }
            status = (sanitized_input == correct)
            if status == False:
                content.update_attempts(course_name, module_name, content_id=content_id)
            if status == True:
                content.update_complete(course_name, module_name, content_id=content_id)
            return {
                'status': status,
            }
    
    abort(404)

@courses.route('/learning')
def learning():
    return render_template('course/learning.html')

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
    return render_template('course/challengePHP.html')

@courses.route('/challengeJS')
def challengeJS():
    return render_template('course/challengeJS.html')

# @courses.route('/testcodeMirror')
# def testcodeMirror():
#     return render_template('testcodeMirror.html')