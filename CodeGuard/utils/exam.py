from flask import session, flash, redirect, url_for, request
from urllib.parse import quote_plus


def check_exam():
    if ('exam_in_progress' in session) and (session['exam_in_progress'] == True):
        course_name = quote_plus(session.get('course_name', None))
        if 'exam' not in request.path or 'results' in request.path:
            flash("Exam is still in progress!")
            return url_for('courses.exam', course_name=course_name)
    return None

def clear_exam_lock():
    session.pop('exam_in_progress')
    session.pop('exam_start_time')
    session.pop('exam_duration')
    session.pop('course_name')
    session.pop('code_state')
