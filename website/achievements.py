from website import database
from hedyweb import AchievementTranslations
from website.auth import requires_login
from flask import request, jsonify


class Achievements:

    def __init__(self):
        self.DATABASE = database.Database()
        self.TRANSLATIONS = AchievementTranslations()
        self.achieved = None
        self.new_achieved = []
        self.lang = "en"
        self.previous_code = None
        self.run_programs = 0
        self.saved_programs = 0
        self.submitted_programs = 0
        self.identical_consecutive_errors = 0
        self.consecutive_errors = 0

    def update_language(self, lang):
        self.lang = lang

    def routes(self, app, database):
        global DATABASE
        DATABASE = database

        @app.route('/achievements', methods=['POST'])
        @requires_login
        def push_new_achievement(user):
            body = request.json
            if "achievement" in body:
                if not self.achieved:
                    self.get_db_data(user['username'])
                if body['achievement'] not in self.achieved and body['achievement'] in self.TRANSLATIONS.get_translations(self.lang):
                    return jsonify({"achievements": self.verify_pushed_achievement(user.get('username'), body['achievement'])})
            return jsonify({})

    def increase_count(self, category):
        if category == "run":
            self.run_programs += 1
        elif category == "saved":
            self.saved_programs += 1
        elif category == "submitted":
            self.submitted_programs += 1

    def get_db_data(self, username):
        achievements_data = self.DATABASE.progress_by_username(username)
        if 'achieved' in achievements_data:
            self.achieved = achievements_data['achieved']
        else:
            self.achieved = []
        if 'run_programs' in achievements_data:
            self.run_programs = achievements_data['run_programs']
        else:
            self.run_programs = 0
        if 'saved_programs' in achievements_data:
            self.saved_programs = achievements_data['saved_programs']
        else:
            self.saved_programs = 0
        if 'submitted_programs' in achievements_data:
            self.submitted_programs = achievements_data['submitted_programs']
        else:
            self.submitted_programs = 0

    def add_single_achievement(self, username, achievement):
        if achievement not in self.achieved and achievement in self.TRANSLATIONS.get_translations(self.lang):
            return self.verify_pushed_achievement(username, achievement)
        else:
            return None

    def verify_run_achievements(self, username, code=None, response=None):
        if not self.achieved:
            self.get_db_data(username)
        self.new_achieved = []
        self.check_programs_run(self.run_programs)
        if code:
            self.check_code_achievements(code)
        if response:
            self.check_response_achievements(code, response)

        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def verify_save_achievements(self, username, adventure=None):
        if not self.achieved:
            self.get_db_data(username)
        self.new_achieved = []
        self.check_programs_saved(self.saved_programs)
        if adventure and 'adventure_is_worthwhile' not in self.achieved:
            self.new_achieved.append("adventure_is_worthwhile")

        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def verify_submit_achievements(self, username):
        if not self.achieved:
            self.get_db_data(username)
        self.new_achieved = []
        self.check_programs_submitted(self.submitted_programs)

        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def verify_pushed_achievement(self, username, achievement):
        self.new_achieved = [achievement]
        self.DATABASE.add_achievement_to_username(username, achievement)
        return self.get_earned_achievements()

    def get_earned_achievements(self):
        translations = self.TRANSLATIONS.get_translations(self.lang)
        translated_achievements = []
        for achievement in self.new_achieved:
            translated_achievements.append([translations[achievement]['title'], translations[achievement]['text'], translations[achievement]['image']])
        return translated_achievements

    def check_programs_run(self, amount):
        if 'getting_started_I' not in self.achieved and amount >= 1:
            self.new_achieved.append("getting_started_I")
        if 'getting_started_II' not in self.achieved and amount >= 10:
            self.new_achieved.append("getting_started_II")
        if 'getting_started_III' not in self.achieved and amount >= 50:
            self.new_achieved.append("getting_started_III")
        if 'getting_started_IV' not in self.achieved and amount >= 200:
            self.new_achieved.append("getting_started_IV")
        if 'getting_started_V' not in self.achieved and amount >= 500:
            self.new_achieved.append("getting_started_V")

    def check_programs_saved(self, amount):
        if 'one_to_remember_I' not in self.achieved and amount >= 1:
            self.new_achieved.append("one_to_remember_I")
        if 'one_to_remember_II' not in self.achieved and amount >= 5:
            self.new_achieved.append("one_to_remember_II")
        if 'one_to_remember_III' not in self.achieved and amount >= 10:
            self.new_achieved.append("one_to_remember_III")
        if 'one_to_remember_IV' not in self.achieved and amount >= 25:
            self.new_achieved.append("one_to_remember_IV")
        if 'one_to_remember_V' not in self.achieved and amount >= 50:
            self.new_achieved.append("one_to_remember_V")

    def check_programs_submitted(self, amount):
        if 'deadline_daredevil_I' not in self.achieved and amount >= 1:
            self.new_achieved.append("deadline_daredevil_I")
        if 'deadline_daredevil_II' not in self.achieved and amount >= 3:
            self.new_achieved.append("deadline_daredevil_II")
        if 'deadline_daredevil_III' not in self.achieved and amount >= 10:
            self.new_achieved.append("deadline_daredevil_III")

    def check_code_achievements(self, code):
        if 'did_you_say_please' not in self.achieved and "ask" in code:
            self.new_achieved.append("did_you_say_please")
        if 'talk-talk-talk' not in self.achieved and code.count("ask") >= 5:
            self.new_achieved.append("talk-talk-talk")
        if 'hedy_honor' not in self.achieved and "Hedy" in code:
            self.new_achieved.append("hedy_honor")
        if 'hedy-ious' not in self.achieved:
            lines = code.splitlines()
            for line in lines:
                if "print" in line:
                    if lines.count(line) >= 10:
                        self.new_achieved.append("hedy-ious")
                        return

    def check_response_achievements(self, code, response):
        if 'ninja_turtle' not in self.achieved and 'has_turtle' in response and response['has_turtle']:
            self.new_achieved.append("ninja_turtle")
        if 'watch_out' not in self.achieved and 'Warning' in response and response['Warning']:
            self.new_achieved.append("watch_out")
        if 'Error' in response and response['Error']:
            self.consecutive_errors += 1
            if self.previous_code == code:
                self.identical_consecutive_errors += 1
            if self.identical_consecutive_errors >= 3:
                if 'programming_panic' not in self.achieved:
                    self.new_achieved.append("programming_panic")
            self.previous_code = code
        else:
            if 'programming_protagonist' not in self.achieved and self.consecutive_errors >= 1:
                self.new_achieved.append("programming_protagonist")
            self.consecutive_errors = 0
            self.identical_consecutive_errors = 0



