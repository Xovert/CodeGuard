import subprocess
import os
import json
from flask import g, current_app as app, request, render_template, abort, session,redirect, url_for, flash
from urllib.parse import unquote, quote_plus
from datetime import datetime, timezone, timedelta

from CodeGuard.courses import courses
from CodeGuard.models import (
    Enrollments,
    ExamQuestions,
    Exams,
    ExamsResults,
    db
)
from CodeGuard.models.enums import CompletionStatus, Severity
from CodeGuard.utils.decorators import login_required, exams_unlocked
from CodeGuard.utils.security import verify_token
from CodeGuard.utils.exam import clear_exam_lock, check_exam
log = app.logger

@courses.route('/exam/<path:course_name>', methods=('GET','POST'))
@login_required
@exams_unlocked
def exam(course_name):
    if not g.modulesComplete:
        abort(403)

    if g.courseComplete:
        if request.method == "GET":
            enrollment: Enrollments = db.session.scalar(
                db.select(Enrollments)
                .where(Enrollments.id == g.enrollment_id)
            )
            score = enrollment.score
            incorrect = enrollment.exams_results

            return render_template(
                'results.html',
                score = score,
                incorrect = incorrect,
            )

    if request.method == "GET":
        if not session.get('exam_in_progress', False):
            token = request.args.get("token", None, type=str)
            if not verify_token(token=token):
                abort(403)
            session['exam_in_progress'] = True
            session['course_name'] = course_name
            time = datetime.now(timezone(timedelta(hours=7)))
            session['exam_start_time'] = time.isoformat()

        enrollment = db.session.execute(
            db.select(Enrollments)
            .where(Enrollments.id == g.enrollment_id)
        ).scalars().first()

        exam:Exams = enrollment.exam
        question:ExamQuestions = exam.questions[0]
        duration = exam.duration
        if 'exam_duration' not in session:
            session['exam_duration'] = duration.total_seconds()
            # session['exam_duration'] = 20


        return render_template("exam.html", 
            question=question.question_text,
            course_name = course_name,
        )
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(500)
        
        clear_exam_lock()
        code = data.get('code')
        username = session.get('username')
        dir = os.path.join(app.instance_path, username)
        os.makedirs(dir, exist_ok=True)
        filepath = os.path.join(dir, 'exam.php')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        semgrep_path = os.path.join(app.root_path, app.config['SEMGREP_PATH'])
        results = run_semgrep_scan(target_path=filepath, semgrep_config=['p/php', semgrep_path])

        enrollment:Enrollments = db.session.scalar(
            db.select(Enrollments)
            .where(Enrollments.id == g.enrollment_id)
        )
        exam:Exams = enrollment.exam
        todo = exam.todo

        correct = {}
        incorrect = []
        for rule in results:
            meta = rule['extra']['metadata']
            zetype = meta.get('type', None)
            if zetype and zetype == 'codeguard.secure':
                if rule['check_id'] not in correct:
                    correct[rule['check_id']] = rule
            else:
                incorrect.append(rule)
        
        score = 0
        
        if todo != 0:
            score = (len(correct.keys())/todo)*100


        enrollment.score = score
        enrollment.status = CompletionStatus.COMPLETE

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error(f'An error has occurred: {e}')
        

        exams_results = [
            {
                "enrollment_id": enrollment.id,
                "exam_id": exam.id,
                "check_id": rule.get('check_id', f'rule{i}'),
                "lines": rule['extra'].get('lines', '').strip(),
                "message": rule['extra'].get("message", '').strip(),
                "severity": Severity.from_str(rule['extra'].get('severity', '')),
            }
            for i, rule in enumerate(incorrect)
        ]

        try:
            db.session.execute(
                db.insert(ExamsResults), exams_results
            )
        except Exception as e:
            db.session.rollback()
            log.error(f'An error has occurred: {e}')
        else:
            db.session.commit()

        
        return {
            "url": url_for(
                'courses.exam',
                course_name=course_name
            ),
        }


def run_semgrep_scan(target_path: str, semgrep_config: list[str] = []):

    command = ['semgrep','scan']
    for config in semgrep_config:
        command.extend(['--config', config])

    command.extend([target_path, '--json'])

    env = os.environ.copy()
    env['SEMGREP_APP_TOKEN'] = app.config['SEMGREP_APP_TOKEN']
    
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    scan_result:dict = json.loads(result.stdout)

    return scan_result.get('results')


@courses.route('/exam/<path:course_name>/status', methods=('GET','POST'))
@login_required
@exams_unlocked
def exam_status(course_name):
    if not g.modulesComplete or g.courseComplete:
        abort(404)

    if request.method == "GET":

        exam:Exams = db.session.execute(
            db.select(Exams)
            .join(Enrollments)
            .where(Enrollments.id == g.enrollment_id)
        ).scalars().first()
        question:ExamQuestions = exam.questions[0]
        elapsed = get_elapsed()
        if 'code_state' not in session:
            session['code_state'] = question.code

        return {
            "code" : session['code_state'],
            "elapsed": elapsed,
            "duration": session['exam_duration']
        }
    
    if request.method == "POST":
        data = request.get_json()
        session['code_state'] = data.get('doc', '')
        return {'status': 'success'}, 200


def get_elapsed():
    now = datetime.now(timezone(timedelta(hours=7)))
    elapsed = now - datetime.fromisoformat(session['exam_start_time'])
    return elapsed.total_seconds()