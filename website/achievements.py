from website import database
from hedyweb import AchievementTranslations
from website.auth import requires_login, current_user
from flask import request, jsonify, session
import hedy


class Achievements:

    def __init__(self):
        self.DATABASE = database.Database()
        self.TRANSLATIONS = AchievementTranslations()
        self.all_commands = self.get_all_commands()
        self.total_users = 0
        self.statistics = self.get_global_statistics()

    def get_all_commands(self):
        commands = []
        for i in range(1, hedy.HEDY_MAX_LEVEL+1):
            for command in hedy.commands_per_level.get(i):
                commands.append(command)
        return set(commands)

    def get_global_statistics(self):
        all_achievements = self.DATABASE.get_all_achievements()
        statistics = {}
        for achievement in self.TRANSLATIONS.get_translations("en").get("achievements").keys():
            statistics[achievement] = 0

        self.total_users = len(all_achievements)
        for user in all_achievements:
            for achieved in user.get("achieved", []):
                statistics[achieved] += 1
        return statistics

    def initialize_user_data_if_necessary(self):
        if 'achieved' not in session:
            achievements_data = self.DATABASE.progress_by_username(current_user()['username'])
            session['new_achieved'] = []
            session['new_commands'] = []
            session['previous_code'] = None
            session['identical_consecutive_errors'] = 0
            session['consecutive_errors'] = 0
            if not achievements_data:
                achievements_data = {}
            if 'achieved' in achievements_data:
                session['achieved'] = achievements_data['achieved']
            else:
                session['achieved'] = []
            if 'commands' in achievements_data:
                session['commands'] = achievements_data['commands']
            else:
                session['commands'] = []
            if 'run_programs' in achievements_data:
                session['run_programs'] = achievements_data['run_programs']
            else:
                session['run_programs'] = 0
            if 'saved_programs' in achievements_data:
                session['saved_programs'] = achievements_data['saved_programs']
            else:
                session['saved_programs'] = 0
            if 'submitted_programs' in achievements_data:
                session['submitted_programs'] = achievements_data['submitted_programs']
            else:
                session['submitted_programs'] = 0

    def routes(self, app, database):
        global DATABASE
        DATABASE = database

        @app.route('/achievements', methods=['POST'])
        @requires_login
        def push_new_achievement(user):
            body = request.json
            if "achievement" in body:
                self.initialize_user_data_if_necessary()
                if body['achievement'] not in session['achieved'] and body['achievement'] in self.TRANSLATIONS.get_translations(session['lang']).get('achievements'):
                    return jsonify({"achievements": self.verify_pushed_achievement(user.get('username'), body['achievement'])})
            return jsonify({})

    def increase_count(self, category):
        self.initialize_user_data_if_necessary()
        if category == "run":
            session['run_programs'] += 1
        elif category == "saved":
            session['saved_programs'] += 1
        elif category == "submitted":
            session['submitted_programs'] += 1

    def add_single_achievement(self, username, achievement):
        self.initialize_user_data_if_necessary()
        if achievement not in session['achieved'] and achievement in self.TRANSLATIONS.get_translations(session['lang']):
            return self.verify_pushed_achievement(username, achievement)
        else:
            return None

    def verify_run_achievements(self, username, code=None, level=None, response=None):
        self.initialize_user_data_if_necessary()
        self.check_programs_run()
        if code and level:
            self.check_code_achievements(code, level)
        if code and response:
            self.check_response_achievements(code, response)

        if len(session['new_commands']) > 0:
            for command in session['new_commands']:
                session['commands'].append(command)
            session['new_commands'] = []
            self.DATABASE.add_commands_to_username(username, session['commands'])

        if len(session['new_achieved']) > 0:
            if self.DATABASE.add_achievements_to_username(username, session['new_achieved']):
                self.total_users += 1
            for achievement in session['new_achieved']:
                session['achieved'].append(achievement)
            return True
        return False

    def verify_save_achievements(self, username, adventure=None):
        self.initialize_user_data_if_necessary()
        self.check_programs_saved()
        if adventure and 'adventure_is_worthwhile' not in session['achieved']:
            session['new_achieved'].append("adventure_is_worthwhile")
        if len(session['new_achieved']) > 0:
            if self.DATABASE.add_achievements_to_username(username, session['new_achieved']):
                self.total_users += 1
            for achievement in session['new_achieved']:
                session['achieved'].append(achievement)
            return True
        return False

    def verify_submit_achievements(self, username):
        self.initialize_user_data_if_necessary()
        self.check_programs_submitted()

        if len(session['new_achieved']) > 0:
            if self.DATABASE.add_achievements_to_username(username, session['new_achieved']):
                self.total_users += 1
            for achievement in session['new_achieved']:
                session['achieved'].append(achievement)
            return True
        return False

    def verify_pushed_achievement(self, username, achievement):
        self.initialize_user_data_if_necessary()
        session['new_achieved'] = [achievement]
        if self.DATABASE.add_achievement_to_username(username, achievement):
            self.total_users += 1
        session['achieved'].append(achievement)
        self.statistics[achievement] += 1
        return self.get_earned_achievements()

    def get_earned_achievements(self):
        self.initialize_user_data_if_necessary()
        translations = self.TRANSLATIONS.get_translations(session['lang']).get('achievements')
        translated_achievements = []
        for achievement in session['new_achieved']:
            translated_achievements.append([translations[achievement]['title'], translations[achievement]['text']])
        session['new_achieved'] = [] # Once we get earned achievements -> empty the array with "waiting" ones
        session['new_commands'] = []
        return translated_achievements

    def check_programs_run(self):
        self.initialize_user_data_if_necessary()
        if 'getting_started_I' not in session['achieved'] and session['run_programs'] >= 1:
            session['new_achieved'].append("getting_started_I")
        if 'getting_started_II' not in session['achieved'] and session['run_programs'] >= 10:
            session['new_achieved'].append("getting_started_II")
        if 'getting_started_III' not in session['achieved'] and session['run_programs'] >= 50:
            session['new_achieved'].append("getting_started_III")
        if 'getting_started_IV' not in session['achieved'] and session['run_programs'] >= 200:
            session['new_achieved'].append("getting_started_IV")
        if 'getting_started_V' not in session['achieved'] and session['run_programs'] >= 500:
            session['new_achieved'].append("getting_started_V")

    def check_programs_saved(self):
        self.initialize_user_data_if_necessary()
        if 'one_to_remember_I' not in session['achieved'] and session['saved_programs'] >= 1:
            session['new_achieved'].append("one_to_remember_I")
        if 'one_to_remember_II' not in session['achieved'] and session['saved_programs'] >= 5:
            session['new_achieved'].append("one_to_remember_II")
        if 'one_to_remember_III' not in session['achieved'] and session['saved_programs'] >= 10:
            session['new_achieved'].append("one_to_remember_III")
        if 'one_to_remember_IV' not in session['achieved'] and session['saved_programs'] >= 25:
            session['new_achieved'].append("one_to_remember_IV")
        if 'one_to_remember_V' not in session['achieved'] and session['saved_programs'] >= 50:
            session['new_achieved'].append("one_to_remember_V")

    def check_programs_submitted(self):
        self.initialize_user_data_if_necessary()
        if 'deadline_daredevil_I' not in session['achieved'] and session['submitted_programs'] >= 1:
            session['new_achieved'].append("deadline_daredevil_I")
        if 'deadline_daredevil_II' not in session['achieved'] and session['submitted_programs'] >= 3:
            session['new_achieved'].append("deadline_daredevil_II")
        if 'deadline_daredevil_III' not in session['achieved'] and session['submitted_programs'] >= 10:
            session['new_achieved'].append("deadline_daredevil_III")

    def check_code_achievements(self, code, level):
        self.initialize_user_data_if_necessary()
        commands_in_code = hedy.all_commands(code, level, session['lang'])
        if 'trying_is_key' not in session['achieved']:
            for command in set(commands_in_code):
                if command not in session['commands'] and command not in session['new_commands']:
                    session['new_commands'].append(command)
            if set(session['commands']).union(session['new_commands']) == self.all_commands:
                session['new_achieved'].append("trying_is_key")
        if 'did_you_say_please' not in session['achieved'] and "ask" in hedy.all_commands(code, level, session['lang']):
            session['new_achieved'].append("did_you_say_please")
        if 'talk-talk-talk' not in session['achieved'] and hedy.all_commands(code, level, session['lang']).count("ask") >= 5:
            session['new_achieved'].append("talk-talk-talk")
        if 'hedy_honor' not in session['achieved'] and "Hedy" in code:
            session['new_achieved'].append("hedy_honor")
        if 'hedy-ious' not in session['achieved']:
            all_print_arguments = hedy.all_print_arguments(code, level, session['lang'])
            for argument in all_print_arguments:
                if all_print_arguments.count(argument) >= 10:
                    session['new_achieved'].append("hedy-ious")
                    break

    def check_response_achievements(self, code, response):
        self.initialize_user_data_if_necessary()
        if 'ninja_turtle' not in session['achieved'] and 'has_turtle' in response and response['has_turtle']:
            session['new_achieved'].append("ninja_turtle")
        if 'watch_out' not in session['achieved'] and 'Warning' in response and response['Warning']:
            session['new_achieved'].append("watch_out")
        if 'Error' in response and response['Error']:
            session['consecutive_errors'] += 1
            if session['previous_code'] == code:
                if session['identical_consecutive_errors'] == 0:
                    session['identical_consecutive_errors'] += 2 #We have to count the first one too!
                else:
                    session['identical_consecutive_errors'] += 1
            if session['identical_consecutive_errors'] >= 3:
                if 'programming_panic' not in session['achieved']:
                    session['new_achieved'].append("programming_panic")
            session['previous_code'] = code
        else:
            if 'programming_protagonist' not in session['achieved'] and session['consecutive_errors'] >= 1:
                session['new_achieved'].append("programming_protagonist")
            session['consecutive_errors'] = 0
            session['identical_consecutive_errors'] = 0



