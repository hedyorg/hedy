from flask_babel import gettext
from website.auth import requires_login, current_user
import utils
import uuid
from flask import g, request, jsonify


def routes(app, database, achievements):
    global DATABASE
    global ACHIEVEMENTS
    DATABASE = database
    ACHIEVEMENTS = achievements

    @app.route('/programs_list', methods=['GET'])
    @requires_login
    def list_programs(user):
        return {'programs': DATABASE.programs_for_user(user['username']).records}

    @app.route('/programs/delete/', methods=['POST'])
    @requires_login
    def delete_program(user):
        body = request.json
        if not isinstance(body.get('id'), str):
            return 'program id must be a string', 400

        result = DATABASE.program_by_id(body['id'])

        if not result or result['username'] != user['username']:
            return "", 404
        DATABASE.delete_program_by_id(body['id'])
        DATABASE.increase_user_program_count(user['username'], -1)

        # This only happens in the situation were a user deletes their favourite program -> Delete from public profile
        public_profile = DATABASE.get_public_profile_settings(current_user()['username'])
        if public_profile and 'favourite_program' in public_profile and public_profile['favourite_program'] == body[
            'id']:
            DATABASE.set_favourite_program(user['username'], None)

        achievement = ACHIEVEMENTS.add_single_achievement(user['username'], "do_you_have_copy")
        resp = {'message': gettext(u'delete_success')}
        if achievement:
            resp['achievement'] = achievement
        return jsonify(resp)

    @app.route('/programs/duplicate-check', methods=['POST'])
    def check_duplicate_program():
        body = request.json
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('name'), str):
            return 'name must be a string', 400

        if not current_user()['username']:
            return 'not_logged', 403

        programs = DATABASE.programs_for_user(current_user()['username'])
        for program in programs:
            if program['name'] == body['name']:
                return jsonify({'duplicate': True, 'message': gettext(u'overwrite_warning')})
        return jsonify({'duplicate': False})

    @app.route('/programs', methods=['POST'])
    @requires_login
    def save_program(user):
        body = request.json
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('code'), str):
            return 'code must be a string', 400
        if not isinstance(body.get('name'), str):
            return 'name must be a string', 400
        if not isinstance(body.get('level'), int):
            return 'level must be an integer', 400
        if 'adventure_name' in body:
            if not isinstance(body.get('adventure_name'), str):
                return 'if present, adventure_name must be a string', 400

        # We check if a program with a name `xyz` exists in the database for the username.
        # It'd be ideal to search by username & program name, but since DynamoDB doesn't allow searching for two indexes at the same time, this would require to create a special index to that effect, which is cumbersome.
        # For now, we bring all existing programs for the user and then search within them for repeated names.
        programs = DATABASE.programs_for_user(user['username']).records
        program_id = uuid.uuid4().hex
        program_public = 0
        overwrite = False
        for program in programs:
            if program['name'] == body['name']:
                overwrite = True
                program_id = program['id']
                program_public = program.get('public', 0)
                break

        stored_program = {
            'id': program_id,
            'session': utils.session_id(),
            'date': utils.timems(),
            'lang': g.lang,
            'version': utils.version(),
            'level': body['level'],
            'code': body['code'],
            'name': body['name'],
            'username': user['username'],
            'public': program_public
        }

        if 'adventure_name' in body:
            stored_program['adventure_name'] = body['adventure_name']

        DATABASE.store_program(stored_program)
        if not overwrite:
            DATABASE.increase_user_program_count(user['username'])
        DATABASE.increase_user_save_count(user['username'])
        ACHIEVEMENTS.increase_count("saved")

        if ACHIEVEMENTS.verify_save_achievements(user['username'],
                                                 'adventure_name' in body and len(body['adventure_name']) > 2):
            return jsonify(
                {'message': gettext(u'save_success_detail'), 'name': body['name'], 'id': program_id, "achievements": ACHIEVEMENTS.get_earned_achievements()})
        return jsonify({'message': gettext(u'save_success_detail'), 'name': body['name'], 'id': program_id})

    @app.route('/programs/share', methods=['POST'])
    @requires_login
    def share_unshare_program(user):
        body = request.json
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('id'), str):
            return 'id must be a string', 400
        if not isinstance(body.get('public'), bool):
            return 'public must be a boolean', 400

        result = DATABASE.program_by_id(body['id'])
        if not result or result['username'] != user['username']:
            return 'No such program!', 404

        # This only happens in the situation were a user un-shares their favourite program -> Delete from public profile
        public_profile = DATABASE.get_public_profile_settings(current_user()['username'])
        if public_profile and 'favourite_program' in public_profile and public_profile['favourite_program'] == body[
            'id']:
            DATABASE.set_favourite_program(user['username'], None)

        DATABASE.set_program_public_by_id(body['id'], bool(body['public']), bool(body['error']))
        achievement = ACHIEVEMENTS.add_single_achievement(user['username'], "sharing_is_caring")

        resp = {'id': body['id']}
        if bool(body['public']):
            resp['message'] = gettext(u'share_success_detail')
        else:
            resp['message'] = gettext(u'unshare_success_detail')
        if achievement:
            resp['achievement'] = achievement
        return jsonify(resp)

    @app.route('/programs/submit', methods=['POST'])
    @requires_login
    def submit_program(user):
        body = request.json
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('id'), str):
            return 'id must be a string', 400

        result = DATABASE.program_by_id(body['id'])
        if not result or result['username'] != user['username']:
            return 'No such program!', 404

        DATABASE.submit_program_by_id(body['id'])
        DATABASE.increase_user_submit_count(user['username'])
        ACHIEVEMENTS.increase_count("submitted")

        if ACHIEVEMENTS.verify_submit_achievements(user['username']):
            return jsonify({"achievements": ACHIEVEMENTS.get_earned_achievements()})
        return jsonify({})

    @app.route('/programs/set_favourite', methods=['POST'])
    @requires_login
    def set_favourite_program(user):
        body = request.json
        if not isinstance(body, dict):
            return 'body must be an object', 400
        if not isinstance(body.get('id'), str):
            return 'id must be a string', 400

        result = DATABASE.program_by_id(body['id'])
        if not result or result['username'] != user['username']:
            return 'No such program!', 404

        if DATABASE.set_favourite_program(user['username'], body['id']):
            return jsonify({'message': gettext(u'favourite_success')})
        else:
            return "You can't set a favourite program without a public profile", 400
