from flask import current_app as app, render_template, url_for, Blueprint, session, request, flash, redirect, jsonify
from wtforms.fields import FieldList
from sqlalchemy.exc import IntegrityError as sqlerror
import logging
from CodeGuard.utils.decorators import admin_required
from CodeGuard.utils.files import delete_file
from CodeGuard.admin.create import upload_image

# from werkzeug.urls 
from urllib.parse import unquote

from CodeGuard.forms.course import (
    NewCourseForm,
    CourseForm,
    NewModuleForm,
    ModuleForm
)
from CodeGuard.admin import dashboard_catalogue, create
from CodeGuard.admin import details as detail
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
# from CodeGuard.admin import create

admin = Blueprint('admin', __name__, template_folder='front-end')

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
    # return render_template('admin/course_settings.html')
    error = None
    success = None

    form = NewCourseForm()
    if form.validate_on_submit():
        course_name = form.title.data
        course_img = form.logo.data
        course_description = form.description.data
        # course_status = form.visibility.data

        create.new_course(course_name, course_img, course_description)
        success = f'Course {course_name} has been succesfully added!'
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
     
    if form.validate_on_submit:
        old_name = course_name
        new_name = form.title.data
        course_img = form.logo.data
        course_description = form.description.data
        course_status = usage_mapping.get(form.visibility.data)

        # if there is an image, update the image
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


@admin.route('/admin/<path:course_name>/modules', methods=('GET','POST'))
@admin_required
def modules(course_name):
    if request.method == 'GET':
        username = session.get('username', '')
        course_name = unquote(course_name)
        modules = detail.get_modules(course_name)
        print(modules)
        
        return render_template(
            'admin/module_list.html',
            username=username,
            course_name=course_name,
            modules=modules
        )
    
    # course = detail.get_course(course_name)
    course_name = unquote(course_name)
    print(course_name)
    modules = detail.get_modules(course_name)
    print(f"Existing Modules: {modules}")
    existing_name = [module.module_name for module in modules]
    print(f"Existing Name: {existing_name}")

    data = request.get_json()
    print(f"Data: {data}")
    # Data: {'modules': [{'order': '1', 'module_name': 'testing'}, {'order': '2', 'module_name': '333333'}, {'order': '3', 'module_name': 'asaddff'}]}
    # return jsonify({"success": True})

    for module_data in data["modules"]:
        module_name = module_data["module_name"]
        order = module_data["order"]

        # i dont think this is the right algo???
        # if module yg dikirim exists
        if module_name in existing_name:
            print(f"{module_name} is in existing_name")
            existing_module = next((module for module in modules if module.module_name == module_name))
            print(f"Existing Module: {existing_module}")
            
            try:
                existing_module.order = order
                db.session.flush()
            except Exception as e:
                db.session.rollback()
            else:
                db.session.commit()
        
    # leftover module
    # code here
    
        # return jsonify({"success": False, "error": str(e)}), 500
    # NNTI GET NEWLY ADDED MODULE, MODULE = NEW MODULES

@admin.route('/admin/<path:course_name>/new', methods=('GET','POST'))
@admin_required
def add_module(course_name):
    if request.method == 'GET':
        username = session.get('username', '')
        course_name = unquote(course_name)

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
            print("AMAN")
            
            # get form data
            module_name = form.module.data
            learning = form.learning.data
            # challenge_code = form.challenge_code.data
            challenge_option = form.challenge_options.data
            exam_code = form.exam_code.data
            exam_options = form.exam_options.data

            # add module
            course_name = unquote(course_name)
            course = detail.get_course(course_name)
            num_of_modules = len(detail.get_modules(course_name))

            module = Modules(
                course_id=course.id,
                order=num_of_modules+1,
                module_name=module_name
            )
            print(module)
            error, success, module_id = create.add_module(module)
            print(module_id)
            if error:
                flash(error)
                return redirect(url_for('admin.add_module', course_name=course_name))

            # add contents
            if learning:
                for content in learning:
                    print("ini content learning")
                    print(content)
                    # {'order': '1', 'image': <FileStorage: '010.png' ('image/png')>, 'content_body': 'adsadsa'}, INI PER PAGE POKOKNYA
                    # model = ContentsLearning
                    order = content["order"]
                    image = content["image"]
                    content_body = content["content_body"]
                    # attribute = {
                    #     "module_id": module_id,
                    #     "order": order,
                    #     "content_body": content_body
                    # }
                    
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
                        print("IMAGE ADDED")

            if challenge_option:
                for content in challenge_option:
                    print("ini challenge_option")
                    print(content)
                    # {'order': '1', 'image': <FileStorage: '008.png' ('image/png')>, 'question': 'ini questionn', 'code': 'ini codeee', 'options': 'Option 2as', 'choices': [{'choices': 'Option 1as'}, {'choices': 'Option 2as'}, {'choices': 'Option 3as'}]}

                    # model = ContentsChallenges
                    order = content["order"]
                    image = content["image"]
                    question_text = content["question"]
                    code = content["code"]
                    correct = content["options"]
                    options = content["choices"]

                    # '''
                    # attribute = {
                    #     "module_id": module_id,
                    #     "order": order,
                    #     "content_body": content_body
                    # }
                    # ini utk add, pokoknya atribut doank
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
                        print("IMAGE ADDED")

                    # "questions": {
                    #     "model": ChallengeQuestions,
                    #     "attributes": {
                    #         "question_text": "Manakah teknik mitigasi berikut yang TIDAK efektif untuk mencegah SSRF?",
                    #         "code": None
                    #     },
                    #     "options": {
                    #         "model": ChallengeOptions,
                    #         "rows": [
                    #             {"option_text": "Membatasi permintaan HTTP ke domain eksternal tertentu menggunakan whitelist.", "is_correct": False},
                    #             {"option_text": "Menggunakan validasi input untuk memastikan URL sesuai format yang diizinkan.", "is_correct": False},
                    #             {"option_text": "Memblokir semua permintaan HTTP yang menggunakan protokol HTTPS.", "is_correct": True},
                    #             {"option_text": "Menggunakan library cURL dengan konfigurasi CURLOPT_FOLLOWLOCATION diatur ke false.", "is_correct": False}
                    #         ]
                    #     }
                    # },
                    # '''

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
                    print("ini choices:")
                    print(options)
                    # [{'choices': 'Option 1as'}, {'choices': 'Option 2as'}, {'choices': 'Option 3as'}]

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
                        # print(row)
                    print("dah ketambah semua challenge option")
            
            success = f"All contents for {module_name} successfully added"
            flash(success)
            return redirect(url_for('admin.modules', course_name=course_name))
                        
            # if challenge_code:
            #     print("ada nih challenge")
            # print(module, learning, challenge_code, challenge_option)

        # for field in form:
        #     if isinstance(field, FieldList):
        #         print(f"{field.name}:")
        #         for i, subfield in enumerate(field.entries):
        #             print(f"  [{i}] {subfield.name}: {subfield.data}")
        #     else:
        #         print(f"{field.name}: {field.data}")
        else:
            error = f"An error occurred when adding the module, please try again"
            flash(error)  
        print("DATA FINISHED")
        return redirect(url_for('admin.modules', course_name=course_name))

@admin.route('/admin/<path:course_name>/<path:module_name>', methods=('GET','POST'))
def detail_module(course_name, module_name):
    print("awopga")
    if request.method == 'GET':
        username = session.get('username', '')
        course_name = unquote(course_name)
        module_name = unquote(module_name)

        course = detail.get_course(course_name)
        module_id = detail.get_module_id(module_name, course.id)
        print(f"module id = {module_id}")
        contents = detail.get_contents(module_id)
        print(f"Contents: {contents}")

        form = ModuleForm()
        form.module.data = module_name
        for i, data in enumerate(contents):
            # form.learning[0].order = content.order
            print("masuk for")
            print(f"Data: {data}")
            # (Contents: module_id:20 order=1 type=learning, '27d693ec-6c6d-4176-98f3-c8db2fcf0e5a-010.png', '010.png')
            # print(content["order"])
            content = data[0]
            if content.type == "learning":
                print(content.order)
                print("learning detected")
                print(i, content.order, content.type, content.content_body)
                # 0 1 learning testing learning content
                form.content[i].content_id.data = content.id
                form.content[i].order.data = content.order
                form.content[i].content_type.data = content.type
                form.content[i].content_body.data = content.content_body
                form.content[i].new_filename.data = data[1]
                form.content[i].original_filename.data = data[2]
                print("show learning done")
            elif content.type == 'challenges':
                print("challenge detected")
                challenge_data = detail.get_challenge_data(content.id)
                print(f"Challenge data: {challenge_data}")
                form.content[i].content_id.data = content.id
                form.content[i].order.data = content.order
                form.content[i].content_type.data = content.type
                form.content[i].question.data = challenge_data.question_text
                form.content[i].code.data = challenge_data.code
                form.content[i].new_filename.data = data[1]
                form.content[i].original_filename.data = data[2]

                options = detail.get_options(challenge_data.id)
                print(f"Options: {options}")
                # Options: [('op1', False), ('op2', False), ('op3', False), ('op5 skip op 4 (ini bener)', True)]
                for j, (option_text, is_correct) in enumerate(options):
                    form.content[i].choices[j].choices.data = option_text
                    if is_correct:
                        form.content[i].correct.data = option_text

                print("show challenges done")
            # print(f"new: {data[1]}, ori: {data[2]}")
            # print(form.content[i])


        # return redirect(url_for('admin.modules', course_name=course_name))
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
        old_module_name = unquote(module_name)
        
        success = None
        error = None
        form = ModuleForm()
        if form.validate_on_submit:
            # print("form validated")   

            # update module name
            module_name = form.module.data
            module = detail.get_single_module(old_module_name, course.id)
            print(f"Module {module}")
            try:
                module.module_name = module_name
                db.session.flush()
                success = f"Module name for {old_module_name} has been updated to {module.module_name}"
                print(success)
            except sqlerror as e:
                error = f"An error has occured while updating the module"
                db.session.rollback()
            else:
                db.session.commit()

            module_id = module.id
            # get all existing contents
            contents = detail.get_contents(module_id)
            # contents ada [1] = Contents, [2] = new_filename, [3] = original_filename
            print(f"Old Contents: {contents}")

            existing_id = [content[0].id for content in contents]
            # for content in contents:
            print(existing_id)
            # print(f"{[type(x) for x in existing_id]}")
    
            # loop over each content in the form
            for i, subform in enumerate(form.content):
                id = subform.content_id.data
                order = subform.order.data
                print(f"dah dapet id dari formnya: {id}, {type(id)}")
                print(i)
                # print(f"Subform: {subform}")

                if not id:
                    # new content, no id, but have order
                    if order:
                        print(f"{i} new content")
                        if subform.content_body.data:
                            print("this is learning")
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
                                print("IMAGE ADDED")
                            
                        elif subform.options.data:
                            print("this is challenges")
                            order = int(order) * 100
                            image = subform.image.data
                            question_text = subform.question.data
                            code = subform.code.data
                            correct = subform.options.data
                            options = subform.choices.data
                            print(f"choices: {options}")

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
                                print("IMAGE ADDED")

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
                                # print(row)
                            print("dah ketambah semua challenge option")
                            # SOMETHING IS WRONG HERE, TAMPUNG DULU
                        continue

                    # empty form (cuz content = min entries = 15)
                    elif not order:
                        print(f"{i}, subform ini none : {id}")
                        continue                   
                
                # if ketemu nih, course yg udah ada (id is not None and not "")
                id = int(id)
                if id in existing_id:
                    print(f"{i} {id} is in existing_id")
                    existing_content = next((content for content in contents if content[0].id == id), None)
                    print(f"existing content: {existing_content}")

                    if subform.content_body.data:
                        # if dulunya dia jg learning (ga berubah)
                        if existing_content[0].type == 'learning':
                        # content_type = "learning"
                            order = int(order) * 100
                            content_body = subform.content_body.data
                            image = subform.image.data

                            try:
                                # existing_content.type = "learning"
                                print(f"Existing content (before) order: {existing_content[0].order}")
                                existing_content[0].order = order
                                print(f"Order now (after): {existing_content[0].order}")
                                existing_content[0].content_body = content_body
                                
                                # if ada imagenya
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
                                db.session.flush()
                                print(f"After update: {existing_content[0]}")
                            except sqlerror as e:
                                error = f'An error has occured when updating the content'
                                print(error)
                                print(f"Database error: {e}")
                                db.session.rollback()
                                
                            else:
                                db.session.commit()
                                success = f"Content {id} has been updated!"

                    # if dia challenge options
                    elif subform.options.data:
                        # if dulu dia jg challenge options
                        if existing_content[0].type == 'challenges':
                        # content_type = "learning"
                            order = int(order) * 100
                            image = subform.image.data
                            question_text = subform.question.data
                            code = subform.code.data
                            correct = subform.options.data
                            options = subform.choices.data
                            print(f"choices: {options}")
                            # [{'choices': 'op1'}, {'choices': 'op2'}, {'choices': 'op3'}, {'choices': 'op5 skip op 4 (ini bener)'}, {'choices': None}]

                            # get challenges data (questions n code) + options
                            challenge_data = detail.get_challenge_data(id)
                            print(challenge_data)
                            
                            
                            try:
                                # existing_content.type = "challenges"
                                print(f"Existing content (before) order: {existing_content[0].order}")
                                
                                existing_content[0].order = order
                                print(f"Order now (after): {existing_content[0].order}")
                                challenge_data.question_text = question_text
                                challenge_data.code = code

                                # delete options n add new options
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
                                    # print(row)
                                print("dah ketambah semua challenge option")

                                # if ada imagenya
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
                                db.session.flush()
                            except sqlerror as e:
                                error = f'An error has occured when updating the content'
                                db.session.rollback()
                                print(error)
                                print(f"Database error: {e}")
                            else:
                                db.session.commit()
                                success = f"Content {id} has been updated!"

                    print(f"Existing ID before: {existing_id}")
                    print(f"popped id: {id}")
                    existing_id.remove(id)
                    print(f"Existing ID after: {existing_id}")    
               
            # leftover id > id yg ga disubmit, means it is deleted
            for leftover_id in existing_id:
                print(f"leftover id: {leftover_id}")
                content, image = detail.get_single_content(leftover_id)
                print(content, image)

                if content.type == 'learning':
                    print(f"deleted content id {content.id} type {content.type}")
                    if image:
                        delete_file(image.id)
                        print("succesfully delete image")
                    detail.delete_content(content.id)
                    print("sucessfully delete content")

                elif content.type == 'challenges':
                    print(f"deleted content id {content.id} type {content.type}")
                    if image:
                        delete_file(image.id)
                        print("succesfully delete image")

                    challenge_data = detail.get_challenge_data(content.id)
                    print(f"question id = {challenge_data.id}")
                    
                    detail.delete_options(challenge_data.id)
                    print(f"options deleted for question id {challenge_data.id}")
                    
                    detail.delete_challenge_data(challenge_data.id)
                    print(f"Challenge data successfully deleted")

                    detail.delete_content(content.id)
                    print("sucessfully delete content")

            # UPDATE ORDER VALUE (after all form.content is looped)
            contents = detail.get_contents(module_id)
            try:
                for content in contents:
                    content[0].order = int(content[0].order / 100)
                    db.session.flush()
                    print(f"order = {content[0].order}")
            except sqlerror as e:
                error = f'An error has occured when updating the content'
                db.session.rollback()
                print(error)
                print(f"Database error: {e}")
            else:
                db.session.commit()
                print("All order column has been updated")
            flash(f"Modules {module_name} has been updated") 

        else:
            error = f"An error occurred when updating the module, please try again"
            flash(error)
        return redirect(url_for(
            'admin.modules',  
            course_name=course_name
        ))


# template materials
@admin.route('/admin/course/material_learning', methods=('GET',))
def material_learning():
    return render_template('admin/material_learning.html')

@admin.route('/admin/course/material_challenge_code', methods=('GET',))
def material_challenge_code():
    return render_template('admin/material_challenge_code.html')

@admin.route('/admin/course/material_challenge_option', methods=('GET',))
def material_challenge_option():
    return render_template('admin/material_challenge_option.html')

@admin.route('/admin/course/material_exam_code', methods=('GET',))
def material_exam_code():
    return render_template('admin/material_exam_code.html')

@admin.route('/admin/course/material_exam_option', methods=('GET',))
def material_exam_option():
    return render_template('admin/material_exam_option.html')
# template materials