from flask import Blueprint, current_app as app, render_template, url_for, session, make_response, send_file

from CodeGuard.utils.decorators import login_required
from CodeGuard.utils.files import get_file

courses = Blueprint('courses', __name__, template_folder='front-end')
from CodeGuard.courses import catalogue

@courses.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    username = session.get('username', '')
    enrolled = catalogue.get_enrolled()
    unenrolled = catalogue.get_catalogue()
    return render_template("course/dashboard.html", username=username)


@courses.route('/course', methods=('GET',))
@login_required
def details():
    username = session.get('username', '')
    return render_template('course/course_details.html', username=username)


# Temporary
@courses.route('/learning') # temporary only, nnti diganti
def learning():
    #login required
    return render_template('course/learning.html')

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