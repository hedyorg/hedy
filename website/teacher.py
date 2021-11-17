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

    from app import render_main_menu

    @app.route('/classes', methods=['GET'])
    @requires_login
    def get_classes (user):
        if not is_teacher(user):
            return 'Only teachers can retrieve classes', 403
        return jsonify (DATABASE.get_teacher_classes (user ['username'], True))

    @app.route('/class/<class_id>', methods=['GET'])
    @requires_login
    def get_class (user, class_id):
        if not is_teacher(user):
            return 'Only teachers can retrieve classes', 403
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username']:
            return utils.page_404 (TRANSLATIONS, render_main_menu('my-profile'), current_user()['username'], g.lang, TRANSLATIONS.get_translations(g.lang, 'ui').get('no_such_class'))
        students = []
        for student_username in Class.get ('students', []):
            student = DATABASE.user_by_username (student_username)
            programs = DATABASE.programs_for_user(student_username)
            highest_level = max(program['level'] for program in programs) if len(programs) else 0
            sorted_public_programs = list(sorted([program for program in programs if program.get ('public')], key=lambda p: p['date']))
            if sorted_public_programs:
                latest_shared = sorted_public_programs[-1]
                latest_shared['link'] = os.getenv ('BASE_URL') + f"/hedy/{latest_shared['id']}/view"
            else:
                latest_shared = None
            students.append ({'username': student_username, 'last_login': utils.mstoisostring (student ['last_login']), 'programs': len (programs), 'highest_level': highest_level, 'latest_shared': latest_shared})

        if utils.is_testing_request (request):
            return jsonify ({'students': students, 'link': Class ['link'], 'name': Class ['name'], 'id': Class ['id']})
        return render_template ('class-overview.html', auth=TRANSLATIONS.get_translations (g.lang, 'Auth'), menu=render_main_menu('my-profile'), current_page='my-profile', class_info={'students': students, 'link': os.getenv ('BASE_URL') + '/hedy/l/' + Class ['link'], 'name': Class ['name'], 'id': Class ['id']})

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

        return {}, 200

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
            return utils.page_404 (TRANSLATIONS, render_main_menu('my-profile'), current_user()['username'], g.lang, TRANSLATIONS.get_translations(g.lang, 'ui').get('invalid_class_link'))
        user = {}
        if request.cookies.get (cookie_name):
            token = DATABASE.get_token(request.cookies.get (cookie_name))
            if token:
                if token ['username'] in Class.get ('students', []):
                    return render_template ('class-already-joined.html', auth=TRANSLATIONS.get_translations (g.lang, 'Auth'), menu=render_main_menu('my-profile'), current_page='my-profile', class_info={'name': Class ['name']})
                user = DATABASE.user_by_username(token ['username'])

        return render_template ('class-prejoin.html',
            auth=TRANSLATIONS.get_translations (g.lang, 'Auth'),
            menu=render_main_menu('my-profile'),
            current_page='my-profile',
            class_info={
                'link': os.getenv ('BASE_URL') + '/class/' + Class ['id'] + '/join/' + Class ['link'] + '?lang=' + g.lang,
                'name': Class ['name'],
            })

    @app.route('/class/<class_id>/join/<link>', methods=['GET'])
    @requires_login
    def join_class (user, class_id, link):
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['link'] != link:
            return utils.page_404 (TRANSLATIONS, render_main_menu('my-profile'), current_user()['username'], g.lang, TRANSLATIONS.get_translations(g.lang, 'ui').get('invalid_class_link'))

        DATABASE.add_student_to_class (Class ['id'], user ['username'])

        return redirect(request.url.replace('/class/' + class_id + '/join/' + link, '/my-profile'), code=302)

    @app.route('/class/<class_id>/student/<student_id>', methods=['DELETE'])
    @requires_login
    def leave_class (user, class_id, student_id):

        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username']:
            return 'No such class', 404

        DATABASE.remove_student_from_class (Class ['id'], student_id)

        return {}, 200

    @app.route('/customize-class/<class_id>', methods=['GET'])
    @requires_login
    def get_class_info(user, class_id):
        if not is_teacher(user):
            return 'Only teachers can retrieve classes', 403
        Class = DATABASE.get_class (class_id)
        if not Class or Class ['teacher'] != user ['username']:
            return utils.page_404 (TRANSLATIONS, render_main_menu('my-profile'), current_user()['username'], g.lang, TRANSLATIONS.get_translations(g.lang, 'ui').get('no_such_class'))

        #It would be nice to improve this to only retrieve the name, id and level of each adventure
        #The current complicated processing on the front-end is not desirable!
        adventures = hedy_content.Adventures(g.lang).adventures_file['adventures']

        # We basically want the change the structure of the adventure storage
        # Suggestion: give each adventure a unique id, independent of language
        # Retrieve these together with all relevant adventure information
        # If a combination of level/id is true in the db for the current class: mark checkbox as selected, otherwise leave it empty
        # Store the selected adventures as a dict with a list of id's like this: {1: [1,2,3,4]} in the db

        return render_template ('customize-class.html', auth=TRANSLATIONS.get_translations (g.lang, 'Auth'), menu=render_main_menu('for-teachers'), class_info={'name': Class ['name']}, adventures=adventures, current_page='for-teachers')

    @app.route('/hedy/l/<link_id>', methods=['GET'])
    def resolve_class_link (link_id):
        Class = DATABASE.resolve_class_link (link_id)
        if not Class:
            return utils.page_404 (TRANSLATIONS, render_main_menu('my-profile'), current_user()['username'], g.lang, TRANSLATIONS.get_translations(g.lang, 'ui').get('invalid_class_link'))
        return redirect(request.url.replace('/hedy/l/' + link_id, '/class/' + Class ['id'] + '/prejoin/' + link_id), code=302)
