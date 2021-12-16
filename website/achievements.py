from website import database
from hedyweb import AchievementTranslations


class Achievements:

    def __init__(self):
        self.DATABASE = database.Database()
        self.TRANSLATIONS = AchievementTranslations()
        self.achieved = []
        self.new_achieved = []

    def verify_new_achievements(self, username, code=None, response=None):
        achievements_data = self.DATABASE.progress_by_username(username)
        self.check_all_achievements(achievements_data)
        if code:
            self.check_code_achievements(code)
        if response and response['has_turtle']:
            self.achieved.append("ninja_turtle")

        self.new_achieved = [i for i in self.achieved + achievements_data['achieved'] if i not in achievements_data['achieved']]
        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def get_earned_achievements(self, language):
        translations = self.TRANSLATIONS.get_translations(language)
        translated_achievements = []
        for achievement in self.new_achieved:
            translated_achievements.append([translations[achievement]['title'], translations[achievement]['text'], translations[achievement]['image']])
        return translated_achievements

    def check_all_achievements(self, user_data):
        self.achieved = []
        self.check_programs_run(user_data['run_programs'])
        self.check_programs_saved(user_data['saved_programs'])
        self.check_programs_submitted(user_data['submitted_programs'])
        return self.achieved

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


