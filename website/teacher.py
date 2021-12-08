from website.auth import requires_login, is_teacher, current_user
import utils
import uuid
from flask import g, request, jsonify, redirect
from flask_helpers import render_template
import os
import hedyweb
import hedy_content
TRANSLATIONS = hedyweb.Translations ()
from config import config
cookie_name     = config ['session'] ['cookie_name']

def routes (app, database):
    global DATABASE
    DATABASE = database

    @app.route('/classes', methods=['GET'])
    @requires_login
    def get_classes (user):
        if not is_teacher(user):
            return utils.page_403 (ui_message='retrieve_class')
        return jsonify (DATABASE.get_teacher_classes (user ['username'], True))

    @app.route('/for-teachers/class/<class_id>', methods=['GET'])
    @requires_login
    def get_class (user, class_id):
        app.logger.info('This is info output')
        if not is_teacher(user):
            return utils.page_403 (ui_message='retrieve_class')
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username']:
            return utils.page_404 (ui_message='no_such_class')
        students = []
        for student_username in Class.get ('students', []):
            student = DATABASE.user_by_username (student_username)
            programs = DATABASE.programs_for_user(student_username)
            highest_level = max(program['level'] for program in programs) if len(programs) else 0
            sorted_public_programs = list(sorted([program for program in programs if program.get ('public')], key=lambda p: p['date']))
            if sorted_public_programs:
                latest_shared = sorted_public_programs[-1]
                latest_shared['link'] = f"/hedy/{latest_shared['id']}/view"
            else:
                latest_shared = None
            students.append ({'username': student_username, 'last_login': utils.datetotimeordate (utils.mstoisostring (student ['last_login'])), 'programs': len (programs), 'highest_level': highest_level, 'latest_shared': latest_shared})

        if utils.is_testing_request (request):
            return jsonify ({'students': students, 'link': Class ['link'], 'name': Class ['name'], 'id': Class ['id']})
        return render_template ('class-overview.html', current_page='for-teachers',
                                page_title=hedyweb.get_page_title('class overview'),
                                class_info={'students': students, 'link': '/hedy/l/' + Class ['link'], 'name': Class ['name'], 'id': Class ['id']})

    @app.route('/class', methods=['POST'])
    @requires_login
    def create_class (user):
        if not is_teacher(user):
            return 'Only teachers can create classes', 403

        body = request.json
        # Validations
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('name'), str):
            return 'name must be a string', 400

        # We use this extra call to verify if the class name doesn't already exist, if so it's a duplicate
        Classes = DATABASE.get_teacher_classes(user['username'], True)
        for Class in Classes:
            if Class['name'] == body['name']:
                return "duplicate", 200

        Class = {
            'id': uuid.uuid4().hex,
            'date': utils.timems (),
            'teacher': user ['username'],
            'link': utils.random_id_generator (7),
            'name': body ['name']
        }

        DATABASE.store_class (Class)

        return {'id': Class['id']}, 200

    @app.route('/class/<class_id>', methods=['PUT'])
    @requires_login
    def update_class (user, class_id):
        if not is_teacher(user):
            return 'Only teachers can update classes', 403

        body = request.json
        # Validations
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('name'), str):
            return 'name must be a string', 400

        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username']:
            return 'No such class', 404

        # We use this extra call to verify if the class name doesn't already exist, if so it's a duplicate
        Classes = DATABASE.get_teacher_classes(user ['username'], True)
        for Class in Classes:
            if Class['name'] == body['name']:
                return "duplicate", 200

        Class = DATABASE.update_class (class_id, body ['name'])

        return {}, 200

    @app.route('/class/<class_id>', methods=['DELETE'])
    @requires_login
    def delete_class (user, class_id):
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username']:
            return 'No such class', 404

        DATABASE.delete_class (Class)

        return {}, 200

    @app.route('/class/<class_id>/prejoin/<link>', methods=['GET'])
    def prejoin_class (class_id, link):
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['link'] != link:
            return utils.page_404 (ui_message='invalid_class_link')
        user = {}
        if request.cookies.get (cookie_name):
            token = DATABASE.get_token(request.cookies.get (cookie_name))
            if token:
                if token ['username'] in Class.get ('students', []):
                    return render_template ('class-already-joined.html', page_title=hedyweb.get_page_title('join class'),
                                            current_page='my-profile', class_info={'name': Class ['name']})
                user = DATABASE.user_by_username(token ['username'])

        return render_template ('class-prejoin.html', page_title=hedyweb.get_page_title('join class'),
            current_page='my-profile',
            class_info={
                'link': '/class/' + Class ['id'] + '/join/' + Class ['link'] + '?lang=' + g.lang,
                'name': Class ['name'],
            })

    @app.route('/class/<class_id>/join/<link>', methods=['GET'])
    @requires_login
    def join_class (user, class_id, link):
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['link'] != link:
            return utils.page_404 (ui_message='invalid_class_link')

        DATABASE.add_student_to_class (Class ['id'], user ['username'])

        return redirect(request.url.replace('/class/' + class_id + '/join/' + link, '/my-profile'), code=302)

    @app.route('/class/<class_id>/student/<student_id>', methods=['DELETE'])
    @requires_login
    def leave_class (user, class_id, student_id):

        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username'] or student_id != user ['username']:
            return 'No such class', 404

        DATABASE.remove_student_from_class (Class ['id'], student_id)

        return {}, 200

    @app.route('/for-teachers/customize-class/<class_id>', methods=['GET'])
    @requires_login
    def get_class_info(user, class_id):
        if not is_teacher(user):
            return utils.page_403 (ui_message='retrieve_class')
        Class = DATABASE.get_class(class_id)
        if not Class or Class['teacher'] != user['username']:
            return utils.page_404(ui_message='no_such_class')

        if hedy_content.Adventures(g.lang).has_adventures():
            adventures = hedy_content.Adventures(g.lang).get_adventure_keyname_name_levels()
        else:
            adventures = hedy_content.Adventures("en").get_adventure_keyname_name_levels()
        levels = hedy_content.LevelDefaults(g.lang).levels
        preferences = DATABASE.get_customizations_class(class_id)

        return render_template('customize-class.html', page_title=hedyweb.get_page_title('customize class'),
                               class_info={'name': Class['name'], 'id': Class['id']}, levels=levels,
                               adventures=adventures, preferences=preferences, current_page='for-teachers')

    @app.route('/customize-class/<class_id>', methods=['PUT'])
    @requires_login
    def update_level_preferences(user, class_id):
        if not is_teacher(user):
            return 'Only teachers can update class preferences', 403

        body = request.json
        print(body)
        # Validations
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('example_programs'), bool):
            return 'amount of example programs must be an integer', 400
        if not isinstance(body.get('hide_level'), bool):
            return 'level switch must be a boolean', 400
        if not isinstance(body.get('hide_prev_level'), bool):
            return 'level switch must be a boolean', 400
        if not isinstance(body.get('hide_next_level'), bool):
            return 'level switch must be a boolean', 400
        if not isinstance(int(body.get('level')), int):
            return 'level must ben an integer', 400

        Class = DATABASE.get_class(class_id)
        if not Class or Class['teacher'] != user['username']:
            return 'No such class', 404

        customizations = {}
        customizations['id'] = class_id
        customizations['level'] = int(body.get('level'))
        customizations['adventures'] = body.get('adventures')
        customizations['example_programs'] = body.get('example_programs')
        customizations['hide'] = body.get('hide_level')
        customizations['hide_prev_level'] = body.get('hide_prev_level')
        customizations['hide_next_level'] = body.get('hide_next_level')


        Class = DATABASE.update_customizations_class(customizations)

        return {}, 200

    @app.route('/hedy/l/<link_id>', methods=['GET'])
    def resolve_class_link (link_id):
        Class = DATABASE.resolve_class_link (link_id)
        if not Class:
            return utils.page_404 (ui_message='invalid_class_link')
        return redirect(request.url.replace('/hedy/l/' + link_id, '/class/' + Class ['id'] + '/prejoin/' + link_id), code=302)
