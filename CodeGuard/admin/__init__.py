from flask import current_app, render_template, url_for, Blueprint, session, request, flash, redirect, jsonify
from wtforms.fields import FieldList
from CodeGuard.utils.decorators import admin_required

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


@admin.route('/admin/<path:course_name>/modules', methods=('GET',))
@admin_required
def modules(course_name):
    username = session.get('username', '')

    course_name = unquote(course_name)
    modules = detail.get_modules(course_name)

    return render_template(
        'admin/module_list.html',
        username=username,
        course_name=course_name,
        modules=modules
    )

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
                return redirect(url_for('admin.add_module'), course_name=course_name)

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
                        return redirect(url_for('admin.add_module'), course_name=course_name)

                    if image:
                        create.upload_image(
                            file=image,
                            ref_id=content_id,
                            usage="content"
                        )
                        print("IMAGE ADDED")

            if challenge_option:
                ###### NOT DONE #######
                for content in challenge_option:
                    print("ini challenge_option")
                    print(content)
                    # {'order': '1', 'image': <FileStorage: '008.png' ('image/png')>, 'question': 'ini questionn', 'code': 'ini codeee', 'options': 'Option 2as', 'choices': [{'choices': 'Option 1as'}, {'choices': 'Option 2as'}, {'choices': 'Option 3as'}]}

                    # model = ContentsChallenges
                    order = content["order"]
                    image = content["image"]
                    question_text = content["question"]
                    code = content["code"]
                    # WE DONT RLY USE THE CODE?
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
                        order=order,
                        # content_body=content_body
                    )
                    error, success, content_id = create.add_content(new_content)
                    if error:
                        flash(error)
                        return redirect(url_for('admin.add_module'), course_name=course_name)


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
                        return redirect(url_for('admin.add_module'), course_name=course_name)


                    # add options
                    print("ini choices:")
                    print(options)
                    # [{'choices': 'Option 1as'}, {'choices': 'Option 2as'}, {'choices': 'Option 3as'}]

                    rows = []
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
                            return redirect(url_for('admin.add_module'), course_name=course_name)
                        # rows.append(row)
                        # print(row)

                    print(rows)
                    print("dah ketambah semua challenge option")
            
            success = f"All contents for {module_name} successfully added"
            flash(success)
            return redirect(url_for('admin.add_module', course_name=course_name))
                        
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
        
        # error = "<br>".join(
        #     message for messages in form.errors.values() for message in messages
        # )
        # flash(error)
        ###### NOT DONE, utk printing errornya #######
        print(form.errors.values())
        print("DATA FINISHED")

        # ini fix
        return redirect(url_for('admin.modules, course_name=course_name'))

@admin.route('/admin/<path:course_name>/<path:module_name>', methods=('GET','POST'))
def detail_module(course_name, module_name):
    print("awopga")
    if request.method == 'GET':
        ###### NOT DONE #######
        username = session.get('username', '')
        course_name = unquote(course_name)
        module_name = unquote(module_name)

        # course = detail.get_course(course_name)
        module_id = detail.get_module_id(module_name)
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
                # print(content.order)
                print("learning detected")
                print(i, content.order, content.type, content.content_body)
                # 0 1 learning testing learning content
                form.content[i].order.data = content.order
                form.content[i].content_type.data = content.type
                form.content[i].content_body.data = content.content_body
                form.content[i].new_filename.data = data[1]
                form.content[i].original_filename.data = data[2]
                print("update learning done")
            elif content.type == 'challenges':
                print("challenge detected")
                challenge_data = detail.get_challenge_data(content.id)
                print(f"Challenge data: {challenge_data}")
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
        # module_name = unquote(module_name)

        form = ModuleForm()

        if form.validate_on_submit:
            print("form validated")

            # get module name
            module_name = form.module.data

            # get all existing contents
            contents = detail.get_contents
            
            # loop over each content in the form
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