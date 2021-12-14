from website import database


class Achievements:

    def __init__(self):
        self.DATABASE = database.Database()
        self.achieved = []
        self.new_achieved = []

    def verify_new_achievements(self, username):
        achievements_data = self.DATABASE.progress_by_username(username)
        reached_achievements = self.check_all_achievements(achievements_data)
        self.new_achieved = list(set(reached_achievements) - set(achievements_data['achieved']))
        if len(self.new_achieved) > 0:
            for achievement in self.new_achieved:
                self.DATABASE.add_achievement_to_username(username, achievement)
            return True
        return False

    def get_earned_achievements(self):
        temp = self.new_achieved.copy()
        self.new_achieved = []
        return temp

    def check_all_achievements(self, user_data):
        self.achieved = []
        self.check_programs_run(user_data['run_programs'])
        self.check_programs_saved(user_data['saved_programs'])
        self.check_programs_submitted(user_data['submitted_programs'])
        return self.achieved

    def check_programs_run(self, amount):
        if amount >= 1:
            self.achieved.append("Getting Started I")
        if amount >= 10:
            self.achieved.append("Getting Started II")
        if amount >= 50:
            self.achieved.append("Getting Started III")
        if amount >= 200:
            self.achieved.append("Getting Started IV")
        if amount >= 500:
            self.achieved.append("Getting Started V")

    def check_programs_saved(self, amount):
        if amount >= 1:
            self.achieved.append("One to Remember I")
        if amount >= 5:
            self.achieved.append("One to Remember II")
        if amount >= 10:
            self.achieved.append("One to Remember III")
        if amount >= 25:
            self.achieved.append("One to Remember IV")
        if amount >= 50:
            self.achieved.append("One to Remember V")

    def check_programs_submitted(self, amount):
        if amount >= 1:
            self.achieved.append("Deadline Daredevil I")
        if amount >= 3:
            self.achieved.append("Deadline Daredevil II")
        if amount >= 10:
            self.achieved.append("Deadline Daredevil III")

