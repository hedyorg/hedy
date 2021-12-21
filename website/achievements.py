from website import database
from hedyweb import AchievementTranslations
from website.auth import requires_login
from flask import request, jsonify


class Achievements:

    def __init__(self):
        self.DATABASE = database.Database()
        self.TRANSLATIONS = AchievementTranslations()
        self.achieved = []
        self.new_achieved = []
        self.lang = "en"
        self.previous_code = None
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
                if body['achievement'] in self.TRANSLATIONS.get_translations(self.lang):
                    return jsonify({"achievements": self.verify_pushed_achievement(user.get('username'), body['achievement'])})
            return jsonify({})

    def strip_new_achievements(self, achievements_data):
        if 'achieved' in achievements_data:
            self.new_achieved = [i for i in self.achieved if i not in achievements_data['achieved']]
        else:
            self.new_achieved = self.achieved

    def add_single_achievement(self, username, achievement):
        if achievement in self.TRANSLATIONS.get_translations(self.lang):
            return self.verify_pushed_achievement(username, achievement)
        else:
            return None

    def verify_run_achievements(self, username, code=None, response=None):
        achievements_data = self.DATABASE.progress_by_username(username)
        self.achieved = []
        self.check_programs_run(achievements_data['run_programs'])
        if code:
            self.check_code_achievements(code)
        if response:
            self.check_response_achievements(code, response)

        self.strip_new_achievements(achievements_data)
        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def verify_save_achievements(self, username, adventure=None):
        achievements_data = self.DATABASE.progress_by_username(username)
        self.achieved = []
        self.check_programs_saved(achievements_data['saved_programs'])
        if adventure:
            self.achieved.append("adventure_is_worthwhile")

        self.strip_new_achievements(achievements_data)
        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def verify_submit_achievements(self, username):
        achievements_data = self.DATABASE.progress_by_username(username)
        self.achieved = []
        self.check_programs_submitted(achievements_data['submitted_programs'])

        self.strip_new_achievements(achievements_data)
        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def verify_pushed_achievement(self, username, achievement):
        achievements_data = self.DATABASE.progress_by_username(username)
        if ('achieved' not in achievements_data) or (achievement not in achievements_data['achieved']):
            self.new_achieved = [achievement]
            self.DATABASE.add_achievement_to_username(username, achievement)
            return self.get_earned_achievements()
        return None

    def get_earned_achievements(self):
        translations = self.TRANSLATIONS.get_translations(self.lang)
        translated_achievements = []
        for achievement in self.new_achieved:
            translated_achievements.append([translations[achievement]['title'], translations[achievement]['text'], translations[achievement]['image']])
        return translated_achievements

    def check_programs_run(self, amount):
        if amount >= 1:
            self.achieved.append("getting_started_I")
        if amount >= 10:
            self.achieved.append("getting_started_II")
        if amount >= 50:
            self.achieved.append("getting_started_III")
        if amount >= 200:
            self.achieved.append("getting_started_IV")
        if amount >= 500:
            self.achieved.append("getting_started_V")

    def check_programs_saved(self, amount):
        if amount >= 1:
            self.achieved.append("one_to_remember_I")
        if amount >= 5:
            self.achieved.append("one_to_remember_II")
        if amount >= 10:
            self.achieved.append("one_to_remember_III")
        if amount >= 25:
            self.achieved.append("one_to_remember_IV")
        if amount >= 50:
            self.achieved.append("one_to_remember_V")

    def check_programs_submitted(self, amount):
        if amount >= 1:
            self.achieved.append("deadline_daredevil_I")
        if amount >= 3:
            self.achieved.append("deadline_daredevil_II")
        if amount >= 10:
            self.achieved.append("deadline_daredevil_III")

    def check_code_achievements(self, code):
        if "ask" in code:
            self.achieved.append("did_you_say_please")
            if code.count("ask") >= 5:
                self.achieved.append("talk-talk-talk")
        if "Hedy" in code:
            self.achieved.append("hedy_honor")
        lines = code.splitlines()
        for line in lines:
            if "print" in line:
                if lines.count(line) >= 10:
                    self.achieved.append("hedy-ious")
                    return

    def check_response_achievements(self, code, response):
        if 'has_turtle' in response and response['has_turtle']:
            self.achieved.append("ninja_turtle")
        if 'Warning' in response and response['Warning']:
            self.achieved.append("watch_out")
        if 'Error' in response and response['Error']:
            self.consecutive_errors += 1
            if self.previous_code == code:
                self.identical_consecutive_errors += 1
            if self.identical_consecutive_errors >= 3:
                self.achieved.append("programming_panic")
            self.previous_code = code
        else:
            if self.consecutive_errors >= 1:
                self.achieved.append("programming_protagonist")
            self.consecutive_errors = 0
            self.identical_consecutive_errors = 0



