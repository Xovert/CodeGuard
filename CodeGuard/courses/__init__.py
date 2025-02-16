from flask import (
    Blueprint, 
    current_app as app, 
    render_template, 
    url_for, 
    session,
    make_response, 
    send_file,
    request,
    abort,
    g,
    flash,
    redirect
)
# from werkzeug.urls 
from urllib.parse import unquote, quote_plus

from CodeGuard.utils.decorators import login_required, exams_unlocked
from CodeGuard.utils.files import get_file
from CodeGuard.utils.exam import check_exam

courses = Blueprint('courses', __name__, template_folder='front-end')
from CodeGuard.courses import exam
from CodeGuard.courses import catalogue
from CodeGuard.courses import details as detail
from CodeGuard.courses import contents as content
from CodeGuard.models.enums import CompletionStatus, CourseStatus
from CodeGuard.utils.course import (
    get_challenge_id_from_option,
    get_course_id_from_name,
    get_enrollment_id,
    get_enrollment_module_id,
    get_module_id_from_name,
    modules_complete,
    course_complete
)
from CodeGuard.utils.security import generate_token


@courses.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    username = session.get('username', '')
    enrolled = catalogue.get_enrolled()
    unenrolled = catalogue.get_catalogue()
    return render_template(
        "course/dashboard.html", 
        username=username, 
        enrolled=enrolled, 
        catalogue=unenrolled
    )


@courses.route('/course/<path:course_name>', methods=('GET',))
@login_required
def details(**kwargs):
    course = detail.get_course_fields()
    modules = detail.get_modules()
    percentage = detail.get_percentage()
    exam = detail.get_exam()
    detail.update_time()
    link_url = None
    if not g.courseComplete:
        if g.modulesComplete:
            token = generate_token()
            link_url = url_for('courses.exam', course_name=kwargs.get('course_name', None), token=token, _external=True)
    
    if g.courseComplete:
        link_url = url_for('courses.exam', course_name=kwargs.get('course_name', None), _external=True)

        
    return render_template(
        'course/course_details.html',
        course = course,
        modules = modules,
        percentage = percentage,
        exam = True if exam else False,
        modulesComplete = g.modulesComplete,
        courseComplete = g.courseComplete,
        exam_url = link_url
    )

@courses.route('/course/<path:course_name>/enroll', methods=('GET',))
@login_required
def enroll(course_name):
    error = detail.enroll_course()
    if error:
        flash(error)
    return redirect(url_for('courses.details', course_name=course_name))


@courses.route('/course/<path:course_name>/module/<path:module_name>/next', methods=('GET',))
@login_required
def next(course_name, module_name):
    page = content.get_progress()
    curr = content.get_content_status(page)
    next = content.get_content_status(page+1)

    content.set_status(curr, CompletionStatus.COMPLETE)
    
    if content.check() == CompletionStatus.COMPLETE:
        next_module = detail.get_next_module()
        detail.unlock_module(next_module)

    if not next:
        return redirect(url_for(
            'courses.details',
            course_name=course_name,
        ))
    else:
        return redirect(url_for(
            'courses.contents',
            course_name=course_name,
            module_name=module_name,
            page=page+1
        ))
    

@courses.route('/course/<path:course_name>/module/<path:module_name>/prev', methods=('GET',))
@login_required
def prev(course_name, module_name):
    page = content.get_progress()
    if page-1 < 1:
        abort(404)

    return redirect(url_for(
        'courses.contents',
        course_name=course_name,
        module_name=module_name,
        page=page-1
    ))

@courses.route('/course/<path:course_name>/module/<path:module_name>', methods=('GET',))
@login_required
def contents(course_name, module_name):
    errors = None
    page = request.args.get("page", 1, type=int)
    if page < 1:
        abort(404)
    
    pagination = content.get_contents(page)

    if not pagination.items:
        abort(404)
    
    if page == 1:
        prev_module = detail.get_prev_module()
        if prev_module.status != CompletionStatus.COMPLETE:
            abort(403)


    module_progress = content.get_progress()
    if (page-1) - module_progress > 1:
        abort(403)

    prev = content.get_content_status(page-1)
    if prev.status != CompletionStatus.COMPLETE:
        abort(403)


    content.update_progress(page)

    return render_template(
        "course/contents.html",
        course_name=g.course_name,
        module_name=g.module_name,
        pagination = pagination
    )


@courses.route("/course/<path:course_name>/module/<path:module_name>/get-attempts", methods=("GET",))
@login_required
def get_attempts(**kwargs):
    content_id = request.args.get('content')
    row = content.get_user_content(content_id)
    attempts = row.attempts
    isComplete = row.correct
    selected = row.option_selected
    answer = row.answer
    
    if attempts >= 0 or isComplete:
        data = {
            'attempts': attempts,
            'isComplete': isComplete,
        }
        if selected:
            data['selected'] = selected
        if answer:
            data['answer'] = answer
        return data
    abort(404)


@courses.route('/course/<path:course_name>/module/<path:module_name>/check', methods=("POST",))
@login_required
def check_challenge(**kwargs):
    request_data = request.json
    content_id = int(request_data["content"])
    user_content = content.get_user_content(content_id)
    if user_content.attempts > 0:
        if request_data["type"] == "options":
            option_id = int(request_data["answer"])
            status = content.check_option(option_id)
            user_content.option_selected = option_id
            
        elif request_data["type"] == "input_text":
            input_text = request_data['answer']
            correct = content.get_correct(content_id)
            sanitized_input, error = content.sanitize_input(input_text)
            if error:
                return {
                    'status': "error",
                    'error': error
                }
            status = (sanitized_input == correct)
            user_content.answer = sanitized_input

        if status == False:
            user_content.attempts -=1

        if status == True:
            user_content.status = CompletionStatus.COMPLETE
            user_content.correct = True

        content.update_user_content(user_content)
        return { 
            'status': status,
        }

    abort(404)


@courses.before_request
def load_datas():
    course_name = request.view_args.get("course_name", None)
    module_name = request.view_args.get("module_name", None)
    if course_name:
        course_name = unquote(course_name)
    if module_name:
        module_name = unquote(module_name)
    g.course_name = course_name
    g.module_name = module_name
    g.course_id = get_course_id_from_name(course_name)
    g.module_id = get_module_id_from_name(module_name)
    g.enrollment_id = get_enrollment_id(g.course_id, g.user_id)
    g.enrollment_module_id = get_enrollment_module_id(g.enrollment_id, g.module_id)
    g.modulesComplete = modules_complete(g.enrollment_id, CompletionStatus.COMPLETE)
    g.courseComplete = course_complete(g.enrollment_id, CompletionStatus.COMPLETE)
    url = check_exam()
    if url != None:
        return redirect(url)
