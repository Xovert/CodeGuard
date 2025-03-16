from flask import current_app as app, render_template, url_for, Blueprint, session, request, flash, redirect, jsonify, abort
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError as sqlerror
from CodeGuard.utils.decorators import admin_required
from CodeGuard.utils.files import delete_file
from CodeGuard.admin.create import upload_image

from urllib.parse import unquote

from CodeGuard.forms.course import (
    NewCourseForm,
    CourseForm,
    NewModuleForm,
    ModuleForm
)
from CodeGuard.admin import dashboard_catalogue, create, details as detail
from CodeGuard.models import (
    db,
    Courses,
    CourseStatus,
    Contents,
    Modules,
    ContentsLearning,
    ContentsChallenges,
    ChallengeQuestions,
    ChallengeOptions
)

log = app.logger
admin = Blueprint('admin', __name__, template_folder='front-end')
from CodeGuard.admin import exam

@admin.route('/admin', methods=('GET',))
@admin_required
def dashboard():
    username = session.get('username', '')
    drafts = dashboard_catalogue.get_courses(CourseStatus.DRAFT)
    published = dashboard_catalogue.get_courses(CourseStatus.PUBLISHED)
    archived = dashboard_catalogue.get_courses(CourseStatus.ARCHIVED)

    return render_template(
        'admin/dashboard.html', 
        username=username, 
        drafts=drafts,
        published=published,
        archived=archived
    )


@admin.route('/admin/new', methods=('GET', 'POST'))
@admin_required
def add_course():
    if request.method == 'GET':
        username = session.get('username', '')
        return render_template('admin/new_course.html', username=username)
    
    error = None
    success = None

    form = NewCourseForm()
    if form.validate_on_submit():
        course_name = form.title.data
        course_img = form.logo.data
        course_description = form.description.data

        create.new_course(course_name, course_img, course_description)
        success = f'Course "{course_name}" has been succesfully added!'
        flash(success)
        return redirect(url_for('admin.dashboard'))
    
    error = "<br>".join(
        message for messages in form.errors.values() for message in messages
    )
    flash(error)
    return redirect(url_for('admin.add_course'))



@admin.route('/admin/<path:course_name>', methods=('GET','POST'))
@admin_required
def description(course_name):
    if request.method == 'GET':
        username = session.get('username', '')

        course_name = unquote(course_name)
        course = detail.get_course_fields(course_name)

        if course is None:
            abort(404)
        
        usage_mapping = {
            CourseStatus.DRAFT : 'draft',
            CourseStatus.ARCHIVED : 'archived',
            CourseStatus.PUBLISHED : 'published'
        }

        form = CourseForm()
        form.title.data = course.course_name
        form.description.data = course.description
        form.visibility.data = usage_mapping.get(course.status)

        return render_template(
            'admin/course_detail.html',
            username=username,
            form=form,
            original_filename=course.original_filename,
            new_filename=course.new_filename,
        )
    
    error = None
    form = CourseForm()

    usage_mapping = {
        'draft': CourseStatus.DRAFT,
        'archived' : CourseStatus.ARCHIVED,
        'published' : CourseStatus.PUBLISHED
    }
     
    if form.validate_on_submit():
        old_name = course_name
        new_name = form.title.data
        course_img = form.logo.data
        course_description = form.description.data
        course_status = usage_mapping.get(form.visibility.data)

        error, success = detail.update_course(old_name, new_name, course_description, course_status, course_img)

        if error:
            flash(error)
        elif success:
            flash(success)
    else:
        error = "<br>".join(
            message for messages in form.errors.values() for message in messages
        )
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/delete_course/<path:course_name>', methods=('POST',))
@admin_required
def delete_course(course_name):
    if request.method == 'POST':
        course_name = unquote(course_name)
        error, success = dashboard_catalogue.delete_course(course_name)
        if error:
            flash(error)
        else:
            flash(success)
        
        return jsonify({"url": url_for('admin.dashboard')})


@admin.route('/admin/<path:course_name>/modules', methods=('GET','POST'))
@admin_required
def modules(course_name):
    if request.method == 'GET':
        username = session.get('username', '')
        course_name = unquote(course_name)
        course = detail.get_course(course_name)
        if course is None:
            abort(404)

        modules = detail.get_modules(course_name)

        return render_template(
            'admin/module_list.html',
            username=username,
            course_name=course_name,
            modules=modules
        )
    
    course_name = unquote(course_name)
    course = detail.get_course(course_name)
    if course is None:
        abort(404)

    modules = detail.get_modules(course_name)
    existing_name = [module.module_name for module in modules]

    data = request.get_json()
    
    try:
        for module_data in data["modules"]:
            module_name = module_data["module_name"]
            order = int(module_data["order"])

            # if sent module exists
            if module_name in existing_name:
                existing_module = next((module for module in modules if module.module_name == module_name), None)
                
                # update order to avoid unique constraint
                existing_module.order = order * 100
                db.session.flush()
                existing_name.remove(module_name)
            
        # leftover module
        for leftover_name in existing_name:
            detail.delete_module(leftover_name, course.id)

        # update order
        updated_modules = detail.get_modules(course_name)
        for module in updated_modules:
            module.order = int(module.order / 100)
            db.session.flush()
    except sqlerror as e:
        db.session.rollback()
        error = "An error occured while updating the order of the module"
        flash(error)
    else:
        db.session.commit()
        success = "List of modules have been updated"
        flash(success)
    
    return jsonify({"url": url_for('admin.modules', course_name=course_name)})


@admin.route('/admin/<path:course_name>/new', methods=('GET','POST'))
@admin_required
def add_module(course_name):
    if request.method == 'GET':
        username = session.get('username', '')
        course_name = unquote(course_name)
        course = detail.get_course(course_name)
        if course is None:
            abort(404)

        return render_template(
            'admin/new_module.html',
            course_name=course_name,
            username=username
        )
    
    elif request.method == 'POST':
        error = None
        success = None
            
        form = NewModuleForm()
        if form.validate_on_submit(): 
            # get form data
            module_name = form.module.data
            learning = form.learning.data
            challenge_option = form.challenge_options.data
            challenge_input = form.challenge_input.data

            try:
                # add module
                course_name = unquote(course_name)
                course = detail.get_course(course_name)
                if course is None:
                    abort(404)

                num_of_modules = len(detail.get_modules(course_name))

                module = Modules(
                    course_id=course.id,
                    order=num_of_modules+1,
                    module_name=module_name
                )
                error, success, module_id = create.add_module(module)
                if error:
                    flash(error)
                    return redirect(url_for('admin.add_module', course_name=course_name))

                # add contents
                if learning:
                    for content in learning:
                        order = content["order"]
                        image = content["image"]
                        content_body = content["content_body"]
                        
                        new_content = ContentsLearning(
                            module_id=module_id,
                            order=order,
                            content_body=content_body
                        )
                        error, success, content_id = create.add_content(new_content)
                        if error:
                            flash(error)
                            return redirect(url_for('admin.add_module', course_name=course_name))

                        if image:
                            create.upload_image(
                                file=image,
                                ref_id=content_id,
                                usage="content"
                            )

                if challenge_option:
                    for content in challenge_option:
                        order = content["order"]
                        image = content["image"]
                        question_text = content["question"]
                        code = content["code"]
                        correct = content["options"]
                        options = content["choices"]

                        new_content = ContentsChallenges(
                            module_id=module_id,
                            order=order
                        )
                        error, success, content_id = create.add_content(new_content)
                        if error:
                            flash(error)
                            return redirect(url_for('admin.add_module', course_name=course_name))

                        # add image
                        if image:
                            create.upload_image(
                                file=image,
                                ref_id=content_id,
                                usage="content"
                            )

                        # add questions
                        questions = ChallengeQuestions(
                            question_text=question_text,
                            code=code,
                            content_id=content_id
                        )

                        error, success, question_id = create.add_questions(questions)
                        if error:
                            flash(error)
                            return redirect(url_for('admin.add_module', course_name=course_name))

                        # add options
                        for option in options:
                            option_text = option["choices"]
                            if option_text == correct:
                                is_correct = True
                            else:
                                is_correct = False
                            row = {
                                "option_text": option_text,
                                "is_correct": is_correct,
                                "question_id": question_id
                            }
                            error, success = create.add_options(ChallengeOptions(**row))
                            if error:
                                flash(error)
                                return redirect(url_for('admin.add_module', course_name=course_name))
                
                if challenge_input:
                    for content in challenge_input:
                        order = content["order"]
                        image = content["image"]
                        question_text = content["question"]
                        code = content["code"]
                        answer = content["answer"]

                        new_content = ContentsChallenges(
                            module_id=module_id,
                            order=order
                        )
                        error, success, content_id = create.add_content(new_content)
                        if error:
                            flash(error)
                            return redirect(url_for('admin.add_module', course_name=course_name))

                        # add image
                        if image:
                            create.upload_image(
                                file=image,
                                ref_id=content_id,
                                usage="content"
                            )

                        # add questions
                        questions = ChallengeQuestions(
                            question_text=question_text,
                            code=code,
                            content_id=content_id
                        )
                        error, success, question_id = create.add_questions(questions)
                        if error:
                            flash(error)
                            return redirect(url_for('admin.add_module', course_name=course_name))
                        
                        # add answer (1 option)
                        row = {
                            "option_text": answer,
                            "is_correct": True,
                            "question_id": question_id
                        }
                        error, success = create.add_options(ChallengeOptions(**row))
                        if error:
                            flash(error)
                            return redirect(url_for('admin.add_module', course_name=course_name))

            except sqlerror as e:
                error = "An error occurred when adding the module, please try again"
                flash(error)
                db.session.rollback()
            else:
                db.session.commit()   
                success = f'All contents for "{module_name}" is successfully added'
                flash(success)

            return redirect(url_for('admin.modules', course_name=course_name))

        else:
            error = f"An error has occurred while adding the module, please fill in all required fields before proceeding"
            flash(error)
        return redirect(url_for('admin.modules', course_name=course_name))

@admin.route('/admin/<path:course_name>/<path:module_name>', methods=('GET','POST'))
def detail_module(course_name, module_name):
    if request.method == 'GET':
        username = session.get('username', '')
        course_name = unquote(course_name)
        module_name = unquote(module_name)

        course = detail.get_course(course_name)
        if course is None:
            abort(404)

        module_id = detail.get_module_id(module_name, course.id)
        if module_id is None:
            abort(404)

        contents = detail.get_contents(module_id)

        form = ModuleForm()
        form.module.data = module_name
        for i, data in enumerate(contents):
            content = data[0]
            if content.type == "learning":
                form.content[i].content_id.data = content.id
                form.content[i].order.data = content.order
                form.content[i].content_type.data = content.type
                form.content[i].content_body.data = content.content_body
                form.content[i].new_filename.data = data[1] if data[1] is not None else ""
                form.content[i].original_filename.data = data[2] if data[2] is not None else ""

            elif content.type == 'challenges':
                challenge_data = detail.get_challenge_data(content.id)
                form.content[i].content_id.data = content.id
                form.content[i].order.data = content.order
                form.content[i].content_type.data = content.type
                form.content[i].question.data = challenge_data.question_text if challenge_data.question_text is not None else ""
                form.content[i].code.data = challenge_data.code if challenge_data.code is not None else ""
                form.content[i].new_filename.data = data[1] if data[1] is not None else ""
                form.content[i].original_filename.data = data[2] if data[2] is not None else ""

                options = detail.get_options(challenge_data.id)

                # for challenge input
                if len(options) == 1:
                    form.content[i].answer.data = options[0][0]
                    form.content[i].correct.data = None
                
                # for challenge options
                else:
                    form.content[i].answer.data = None
                    for j, (option_text, is_correct) in enumerate(options):
                        form.content[i].choices[j].choices.data = option_text
                        if is_correct:
                            form.content[i].correct.data = option_text

        return render_template(
            'admin/module_detail.html',
            username=username,
            course_name=course_name,
            module_name=module_name,
            form=form
        )
    
    elif request.method == 'POST':
        username = session.get('username', '')
        course_name = unquote(course_name)
        course = detail.get_course(course_name)
        if course is None:
            abort(404)
        old_module_name = unquote(module_name)
        
        success = None
        error = None
        form = ModuleForm()
        if form.validate_on_submit():
            try:
                # update module name
                module_name = form.module.data
                error, success, module_id = detail.update_module(module_name, old_module_name, course.id)

                # get all existing contents
                contents = detail.get_contents(module_id)
                existing_id = [content[0].id for content in contents]
        
                # loop over each content in the form
                for i, subform in enumerate(form.content):
                    id = subform.content_id.data
                    order = subform.order.data

                    if not id:
                        # new content, no id, but have order
                        if order:
                            if subform.content_body.data:
                                order = int(order) * 100
                                image = subform.image.data
                                content_body = subform.content_body.data
                                new_content = ContentsLearning(
                                    module_id=module_id,
                                    order=order,
                                    content_body=content_body
                                )
                                error, success, content_id = create.add_content(new_content)
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))
                                
                                if image:
                                    create.upload_image(
                                        file=image,
                                        ref_id=content_id,
                                        usage="content"
                                    )
                                
                            elif subform.options.data:
                                order = int(order) * 100
                                image = subform.image.data
                                question_text = subform.question.data
                                code = subform.code.data
                                correct = subform.options.data
                                options = subform.choices.data
                                
                                if not question_text:
                                    db.session.rollback()
                                    error = "An error has occurred while updating the module, please fill in all required fields before proceeding"
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))

                                new_content = ContentsChallenges(
                                    module_id=module_id,
                                    order=order
                                )
                                error, success, content_id = create.add_content(new_content)
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))
                                
                                # add image
                                if image:
                                    create.upload_image(
                                        file=image,
                                        ref_id=content_id,
                                        usage="content"
                                    )

                                # add question
                                questions = ChallengeQuestions(
                                    question_text=question_text,
                                    code=code,
                                    content_id=content_id
                                )
                                error, success, question_id = create.add_questions(questions)
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))

                                # add options
                                for option in options:
                                    option_text = option["choices"]
                                    if option_text is None:
                                        continue
                                    
                                    if option_text == correct:
                                        is_correct = True
                                    else:
                                        is_correct = False
                                    row = {
                                        "option_text": option_text,
                                        "is_correct": is_correct,
                                        "question_id": question_id
                                    }
                                    error, success = create.add_options(ChallengeOptions(**row))
                                    if error:
                                        flash(error)
                                        return redirect(url_for('admin.modules', course_name=course_name))
                            
                            elif subform.answer.data:
                                order = int(order) * 100
                                image = subform.image.data
                                question_text = subform.question.data
                                code = subform.code.data
                                answer = subform.answer.data
                                                                
                                if not question_text:
                                    db.session.rollback()
                                    error = "An error has occurred while updating the module, please fill in all required fields before proceeding"
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))

                                new_content = ContentsChallenges(
                                    module_id=module_id,
                                    order=order
                                )
                                error, success, content_id = create.add_content(new_content)
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))
                                
                                # add image
                                if image:
                                    create.upload_image(
                                        file=image,
                                        ref_id=content_id,
                                        usage="content"
                                    )

                                # add question
                                questions = ChallengeQuestions(
                                    question_text=question_text,
                                    code=code,
                                    content_id=content_id
                                )
                                error, success, question_id = create.add_questions(questions)
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))

                                # add answer (1 option)
                                row = {
                                    "option_text": answer,
                                    "is_correct": True,
                                    "question_id": question_id
                                }
                                error, success = create.add_options(ChallengeOptions(**row))
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))                               

                            # if in the newly added content, some important field is emptied, and hence their respective if condition is not triggered
                            else:
                                db.session.rollback()
                                error = "An error has occurred while adding a new content, please fill in all required fields before proceeding"
                                flash(error)
                                return redirect(url_for('admin.modules', course_name=course_name))
                        continue                 
                    
                    # update existing content, id exists
                    id = int(id)
                    if id in existing_id:
                        existing_content = next((content for content in contents if content[0].id == id), None)

                        # if content is learning
                        if subform.content_body.data and existing_content[0].type == 'learning':
                            order = int(order) * 100
                            content_body = subform.content_body.data
                            image = subform.image.data
                            original_filename = subform.original_filename.data

                            try:
                                existing_content[0].order = order
                                existing_content[0].content_body = content_body
                                
                                if image:
                                    try:
                                        if existing_content[3]:
                                            delete_file(existing_content[3])
                                        upload_image(
                                            file=image,
                                            ref_id=id,
                                            usage='content',
                                        )
                                    except FileNotFoundError as e:
                                        error = f"An error occcured while uploading course image:\n\t {e}"
                                        db.session.rollback()
                                else:
                                    if original_filename == "No file chosen" and existing_content[3]:
                                        delete_file(existing_content[3])

                                db.session.flush()
                            except sqlerror as e:
                                error = f'An error has occured when updating the content'
                                db.session.rollback()

                        # if content is challenge options
                        elif subform.options.data and existing_content[0].type == 'challenges':
                            order = int(order) * 100
                            image = subform.image.data
                            original_filename = subform.original_filename.data
                            question_text = subform.question.data
                            code = subform.code.data
                            correct = subform.options.data
                            options = subform.choices.data

                            if not question_text:
                                db.session.rollback()
                                error = "An error has occurred while updating the module, please fill in all required fields before proceeding"
                                flash(error)
                                return redirect(url_for('admin.modules', course_name=course_name))

                            # get challenges data (questions and code)
                            challenge_data = detail.get_challenge_data(id)
                            
                            try:
                                existing_content[0].order = order
                                challenge_data.question_text = question_text
                                challenge_data.code = code

                                # delete options and add new options
                                detail.delete_options(challenge_data.id)
                                for option in options:
                                    option_text = option["choices"]
                                    if option_text is None:
                                        continue

                                    if option_text == correct:
                                        is_correct = True
                                    else:
                                        is_correct = False
                                    row = {
                                        "option_text": option_text,
                                        "is_correct": is_correct,
                                        "question_id": challenge_data.id
                                    }
                                    error, success = create.add_options(ChallengeOptions(**row))
                                    if error:
                                        flash(error)
                                        return redirect(url_for('admin.modules', course_name=course_name))

                                # update image
                                if image:
                                    try:
                                        if existing_content[3]:
                                            delete_file(existing_content[3])
                                        upload_image(
                                            file=image,
                                            ref_id=id,
                                            usage='content',
                                        )
                                    except FileNotFoundError as e:
                                        error = f"An error occcured while uploading course image:\n\t {e}"
                                        db.session.rollback()
                                else:
                                    if original_filename == "No file chosen" and existing_content[3]:
                                        delete_file(existing_content[3])
                                db.session.flush()

                                
                            except sqlerror as e:
                                error = f'An error has occured when updating the module'
                                db.session.rollback()

                        # if content is challenge input
                        elif subform.answer.data and existing_content[0].type == 'challenges':
                            order = int(order) * 100
                            image = subform.image.data
                            original_filename = subform.original_filename.data
                            question_text = subform.question.data
                            code = subform.code.data
                            answer = subform.answer.data

                            if not question_text:
                                db.session.rollback()
                                error = "An error has occurred while updating the module, please fill in all required fields before proceeding"
                                flash(error)
                                return redirect(url_for('admin.modules', course_name=course_name))

                            # get challenges data (questions n code) + options
                            challenge_data = detail.get_challenge_data(id)
                            
                            try:
                                existing_content[0].order = order
                                challenge_data.question_text = question_text
                                challenge_data.code = code

                                # update option
                                error, success = detail.update_single_option(challenge_data.id, answer)
                                if error:
                                    flash(error)
                                    return redirect(url_for('admin.modules', course_name=course_name))

                                # update image
                                if image:
                                    try:
                                        if existing_content[3]:
                                            delete_file(existing_content[3])
                                        upload_image(
                                            file=image,
                                            ref_id=id,
                                            usage='content',
                                        )
                                    except FileNotFoundError as e:
                                        error = f"An error occcured while uploading course image:\n\t {e}"
                                        db.session.rollback()
                                else:
                                    if original_filename == "No file chosen" and existing_content[3]:
                                        delete_file(existing_content[3])
                                db.session.flush()
                                
                            except sqlerror as e:
                                error = f'An error has occured when updating the module'
                                db.session.rollback()

                        # some important fields from each content was empty, and hence their respective if condition is not executed
                        else:
                            db.session.rollback()
                            error = "An error has occurred while updating the module, please fill in all required fields before proceeding"
                            flash(error)
                            return redirect(url_for('admin.modules', course_name=course_name))

                        # pop the id of the updated content
                        existing_id.remove(id)  
                
                # leftover id (deleted content)
                for leftover_id in existing_id:
                    detail.delete_content(leftover_id)

                # update order value after all update is done
                contents = detail.get_contents(module_id)
                try:
                    for content in contents:
                        content[0].order = int(content[0].order / 100)
                        db.session.flush()
                except sqlerror as e:
                    error = f'An error has occured when updating the content'
                    db.session.rollback()

            except sqlerror as e:
                error = "An error has occurred while updating the module, please try again"
                flash(error)
                db.session.rollback()
            else:
                db.session.commit()
                success = f'Module "{module_name}" has been updated'
                flash(success) 
        else:
            error = f"An error has occurred while updating the module, please fill in all required fields before proceeding"
            flash(error)
        return redirect(url_for(
            'admin.modules',  
            course_name=course_name
        ))


# template materials
@admin.route('/admin/course/material_learning', methods=('GET',))
def material_learning():
    return render_template('admin/material_learning.html')

@admin.route('/admin/course/material_challenge_option', methods=('GET',))
def material_challenge_option():
    return render_template('admin/material_challenge_option.html')

@admin.route('/admin/course/material_challenge_input', methods=('GET',))
def material_challenge_input():
    return render_template('admin/material_challenge_input.html')

# for module details
@admin.route('/admin/course/detail_material_learning', methods=('GET',))
def detail_material_learning():
    return render_template('admin/detail_material_learning.html')

@admin.route('/admin/course/detail_material_challenge_option', methods=('GET',))
def detail_material_challenge_option():
    return render_template('admin/detail_material_challenge_option.html')

@admin.route('/admin/course/detail_material_challenge_input', methods=('GET',))
def detail_material_challenge_input():
    return render_template('admin/detail_material_challenge_input.html')
# template materials

@admin.before_request
def check_course():
    course_name = request.view_args.get('course_name', None)
    if course_name:
        course_name = unquote(course_name)
        try:
            course: Courses = db.session.execute(
                db.select(Courses)
                .where(Courses.course_name == course_name)
            ).scalars().one_or_none()
        except exc.MultipleResultsFound as e:
            log.error(e)
            abort(500, description="Multiple Course with the same name were found!")

        if course is None:
            abort(404, description=f'Course \"{course_name}\" was not found on the server!')
