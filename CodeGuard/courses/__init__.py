from flask import Blueprint, current_app, render_template, url_for, session, make_response

from CodeGuard.utils.decorators import login_required
from CodeGuard.utils.uploads import stream

courses = Blueprint('courses', __name__, template_folder='front-end')

@courses.route('/dashboard', methods=('GET',))
@login_required
def dashboard():
    username = session.get('username', '')
    return render_template("course/dashboard.html", username=username)

@courses.route('/course', methods=('GET',))
def details():
    username = session.get('username', '')
    return render_template('course/course_details.html', username=username)

# Temporary
@courses.route('/learning') # temporary only, nnti diganti
def learning():
    #login required
    return render_template('course/learning.html')

@courses.route('/render-image')
def renderimage():
    return render_template('test.html')

@courses.route('/image/<path:key_object>', methods=("GET",))
def image(key_object):
    return make_response(stream(key_object))

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