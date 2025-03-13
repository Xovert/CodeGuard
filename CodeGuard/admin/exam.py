from flask import g, current_app as app, render_template, redirect, abort, request, url_for, flash, session

from CodeGuard.admin import admin
from CodeGuard.utils.decorators import admin_required
from CodeGuard.models import (
    db,
    Courses,
    CourseStatus,
    Contents,
    Modules,
    ContentsLearning,
    ContentsChallenges,
    ChallengeQuestions,
    ChallengeOptions,
    Exams,
    ExamQuestions,
)
from CodeGuard.models.enums import CompletionStatus
from datetime import timedelta
from CodeGuard.forms.exam import NewExamForm, DurationForm
from CodeGuard.utils.errors import collect_errors
log = app.logger
from urllib.parse import unquote, quote_plus
from sqlalchemy import func

@admin.route('/admin/<path:course_name>/exams', methods=('GET',))
@admin_required
def exams(course_name):
    course_name = unquote(course_name)

    if request.method == "GET":
        exams_obj: Exams = db.session.execute(
            db.select(Exams)
            .join(Courses)
            .where(Courses.course_name == course_name)
        ).scalars()
        username = session.get('username', '')
        return render_template(
            'admin/exam_list.html',
            course_name=course_name,
            exams=exams_obj,
            username=username,
        )

@admin.route('/admin/<path:course_name>/exams/new', methods=('GET', 'POST'))
@admin_required
def add_exam(course_name):
    course_name = unquote(course_name)
    if request.method == "GET":
        # return render_template('admin/test.html')
        username = session.get('username', '')
        result = db.session.execute(
            db.select(func.max(Exams.exam_number))
            .join(Courses)
            .where(Courses.course_name == course_name)
        )
        max_exam_id = result.scalar() or 0
        exam_name = f'{course_name}-{max_exam_id+1:03d}'
        return render_template(
            'admin/new_exam.html',
            exam_name=exam_name,
            course_name=course_name,
            username=username,
        )
    
    if request.method == "POST":
        result = db.session.execute(
            db.select(func.max(Exams.exam_number))
            .join(Courses)
            .where(Courses.course_name == course_name)
        )
        max_exam_id = result.scalar() or 0
        exam_name = f'{course_name}-{max_exam_id+1:03d}'

        form: NewExamForm = NewExamForm(exam=exam_name)
        if form.validate_on_submit():
            hours: int = form.duration.data.get('hours', 0)
            minutes: int = form.duration.data.get('minutes', 0)
            todo: int = form.todo.data
            question: str = form.question.data.strip()
            code: str = form.code.data

            duration: timedelta = timedelta(hours=hours, minutes=minutes)

            course: Courses = db.session.execute(
                db.select(Courses)
                .where(Courses.course_name == course_name)
            ).scalars().one()
            
            try:
                course.exams.append(
                    Exams(
                        duration = duration,
                        todo=todo,
                        questions=[
                            ExamQuestions(
                                question_text=question,
                                code=code
                            ),
                        ]
                    )
                )
                db.session.flush()
            except Exception as e:
                db.session.rollback()
                log.error(e)
                flash("An error has occured while adding exam to database.")
                return redirect(url_for('admin.add_exam', course_name=quote_plus(course_name)))
            finally:
                db.session.commit()
            
        else:
            errors = "<br>".join(collect_errors(form.errors))
            flash(errors)
            return redirect(url_for('admin.add_exam', course_name=quote_plus(course_name)))

        flash('Exam has been added successfully!')
        return redirect(url_for('admin.dashboard'))
    
    abort(404)

@admin.route('/admin/<path:course_name>/exams', methods=('GET', 'POST'))
@admin_required
def detail_exam(course_name):
    course_name = unquote(course_name)
    if request.method == "GET":
        exam_number = request.args.get('number')
        return render_template(
            'admin/exam_detail.html'
        )

    if request.method == "POST":
        pass

@admin.route('/admin/<path:course_name>/exams/delete', methods=('POST',))
def delete_exam(course_name):
    course_name = unquote(course_name)
    status:str = 'success'
    if request.method == "POST":
        delete_req = request.get_json()
        examNumbers = delete_req.get('numbers', None)
        if examNumbers is None:
            abort(500)
        
        to_be_deleted:list[Exams] = db.session.execute(
            db.select(Exams)
            .join(Courses)
            .where(Courses.course_name == course_name)
            .where(Exams.exam_number.notin_(examNumbers))
        ).scalars().all()
        
        if not to_be_deleted:
            abort(500)

        existing_exams:Exams = db.session.execute(
            db.select(Exams)
            .join(Courses)
            .where(Courses.course_name == course_name)
            .where(Exams.exam_number.in_(examNumbers))
        ).scalars().all()

        import random
        for exam in to_be_deleted:
            if len(existing_exams) > 0:
                enrollments = list(exam.enrollments)
                for enrollment in enrollments:
                    if enrollment.status != CompletionStatus.COMPLETE: 
                        enrollment.exam = random.choice(existing_exams)
            db.session.delete(exam)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error(f'Error deleting exam: {e}')
            status = 'failed'
            
        return {
            'status': status
        }, 200 if status == 'success' else 500
        
    abort(404)