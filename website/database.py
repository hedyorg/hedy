from utils import timems, times
from datetime import date
from . import dynamo
import functools
import operator


storage = dynamo.AwsDynamoStorage.from_env() or dynamo.MemoryStorage('dev_database.json')

USERS = dynamo.Table(storage, 'users', 'username', indexed_fields=[dynamo.IndexKey('email')])
TOKENS = dynamo.Table(storage, 'tokens', 'id', indexed_fields=[dynamo.IndexKey(v) for v in ['id', 'username']])
PROGRAMS = dynamo.Table(storage, 'programs', 'id', indexed_fields=[dynamo.IndexKey(v) for v in ['username', 'public', 'hedy_choice']])
CLASSES = dynamo.Table(storage, 'classes', 'id', indexed_fields=[dynamo.IndexKey(v) for v in ['teacher', 'link']])
ADVENTURES = dynamo.Table(storage, 'adventures', 'id', indexed_fields=[dynamo.IndexKey('creator')])
INVITATIONS = dynamo.Table(storage, 'class_invitations', partition_key='username', indexed_fields=[dynamo.IndexKey('class_id')])
CUSTOMIZATIONS = dynamo.Table(storage, 'class_customizations', partition_key='id')
ACHIEVEMENTS = dynamo.Table(storage, 'achievements', partition_key='username')
PUBLIC_PROFILES = dynamo.Table(storage, 'public_profiles', partition_key='username')

# Information on quizzes. We will update this record in-place as the user completes
# more of the quiz. The database is formatted like this:
#
# { user -> [ { levelAttempt [SORT KEY],
#               user,
#               level,
#               date,
#               q1: ["A", "A", "C"],
#               q2: ["B", "C"],
#               ...
#               correct: { 1, 5, 10 }
#             } }
#
# We will add to the q1, q2, q3... sets as the user submits answers, and add to the
# 'correct' set as users submit correct answers.
#
# 'levelAttempt' is a combination of level and attemptId, to distinguish attempts
# by a user. 'level' is padded to 4 characters, then attemptId is added.
#
QUIZ_ANSWERS = dynamo.Table(storage, 'quizAnswers', partition_key='user', sort_key='levelAttempt')

# Holds information about program runs: success/failure and produced exceptions. Entries are created per user per level
# per week and updated in place. Uses a composite partition key 'id#level' and 'week' as a sort key. Structure:
# {
#   "id#level": "hedy#1",
#   "week": '2025-52',
#   "successful_runs": 10,
#   "InvalidCommandException": 3,
#   "InvalidSpaceException": 2
# }
#
PROGRAM_STATS = dynamo.Table(storage, 'program-stats', partition_key='id#level', sort_key='week',
                             indexed_fields=[dynamo.IndexKey('id', 'week')])

QUIZ_STATS = dynamo.Table(storage, 'quiz-stats', partition_key='id#level', sort_key='week',
                          indexed_fields=[dynamo.IndexKey('id', 'week')])

class Database:
    def record_quiz_answer(self, attempt_id, username, level, question_number, answer, is_correct):
        """Update the current quiz record with a new answer.

        Uses a DynamoDB update to add to the exising record.
        """
        key = {
            "user": username,
            "levelAttempt": str(level).zfill(4) + '_' + attempt_id,
        }

        updates = {
            "attemptId": attempt_id,
            "level": level,
            "date": times(),
            "q" + str(question_number): dynamo.DynamoAddToList(answer),
        }

        if is_correct:
            updates['correct'] = dynamo.DynamoAddToNumberSet(int(question_number))

        return QUIZ_ANSWERS.update(key, updates)

    def get_quiz_answer(self, username, level, attempt_id):
        """Load a quiz answer from the database."""

        quizAnswers = QUIZ_ANSWERS.get({'user': username, 'levelAttempt': str(level).zfill(4) + '_' + attempt_id})

        array_quiz_answers = []
        for question_number in range(len(quizAnswers)):
            answers = quizAnswers.get("q" + str(question_number))
            array_quiz_answers.append(answers)
        return array_quiz_answers

    def level_programs_for_user(self, username, level):
        """List level programs for the given user, newest first.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        programs = PROGRAMS.get_many({'username': username}, reverse=True)
        return [x for x in programs if x.get('level') == int(level)]

    def programs_for_user(self, username):
        """List programs for the given user, newest first.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        return PROGRAMS.get_many({'username': username}, reverse=True)

    def filtered_programs_for_user(self, username, level, adventure):
        programs = PROGRAMS.get_many({'username': username}, reverse=True)
        if level:
            programs = [x for x in programs if x.get('level') == int(level)]
        if adventure:
            # If the adventure we filter on is called 'default' -> return all programs WITHOUT an adventure
            if adventure == "default":
                return [x for x in programs if x.get('adventure_name') == ""]
            return [x for x in programs if x.get('adventure_name') == adventure]

    def public_programs_for_user(self, username):
        programs = PROGRAMS.get_many({'username': username}, reverse=True)
        return [p for p in programs if p.get('public') == 1]

    def program_by_id(self, id):
        """Get program by ID.

        Returns: { code, name, program, level, adventure_name, date }
        """
        return PROGRAMS.get({'id': id})

    def store_program(self, program):
        """Store a program."""
        PROGRAMS.create(program)

    def set_program_public_by_id(self, id, public):
        """Store a program."""
        PROGRAMS.update({'id': id}, {'public': 1 if public else 0})

    def submit_program_by_id(self, id):
        PROGRAMS.update({'id': id}, {'submitted': True})

    def delete_program_by_id(self, id):
        """Delete a program by id."""
        PROGRAMS.delete({'id': id})

    def increase_user_program_count(self, username, delta=1):
        """Increase the program count of a user by the given delta."""
        return USERS.update({ 'username': username }, {
            'program_count': dynamo.DynamoIncrement(delta)
        })

    def user_by_username(self, username):
        """Return a user object from the username."""
        return USERS.get({'username': username.strip().lower()})

    def user_by_email(self, email):
        """Return a user object from the email address."""
        return USERS.get({'email': email.strip().lower()})

    def get_token(self, token_id):
        """Load a token from the database."""
        return TOKENS.get({'id': token_id})

    def store_token(self, token):
        """Store a token in the database."""
        TOKENS.create(token)

    def forget_token(self, token_id):
        """Forget a Token.

        Returns the Token that was deleted.
        """
        return TOKENS.delete({'id': token_id})

    def delete_all_tokens(self, username):
        """Forget all Tokens from a user."""
        TOKENS.del_many({'username': username})

    def store_user(self, user):
        """Store a user in the database."""
        USERS.create(user)

    def record_login(self, username, new_password_hash=None):
        """Record the fact that the user logged in, potentially updating their password hash."""
        if new_password_hash:
            self.update_user(username, {'password': new_password_hash, 'last_login': timems ()})
        else:
            self.update_user(username, {'last_login': timems ()})

    def update_user(self, username, userdata):
        """Update the user data with the given fields.

        This method is a bit of a failing of the API, but there are too many
        slight variants of tweaking some fields on the user in the code to
        turn each of them into a separate method here.
        """
        USERS.update({'username': username}, userdata)

    def forget_user(self, username):
        """Forget the given user."""
        classes = USERS.get({'username': username}).get ('classes') or []
        USERS.delete({'username': username})
        INVITATIONS.delete({'username': username})
        # The recover password token may exist, so we delete it
        TOKENS.delete({'id': username})
        PROGRAMS.del_many({'username': username})

        # Remove user from classes of which they are a student
        for class_id in classes:
            self.remove_student_from_class (class_id, username)

        # Delete classes owned by the user
        for Class in self.get_teacher_classes (username, False):
            self.delete_class (Class)

    def all_users(self, filtering=False):
        """Return all users."""
        # If we have some filtering -> return all possible users, otherwise return last 500
        if filtering:
            return USERS.scan()
        return USERS.scan(limit=500)

    def get_all_explore_programs(self):
        return PROGRAMS.get_many({'public': 1}, sort_key='date', limit=48, reverse=True)

    def get_filtered_explore_programs(self, level=None, adventure=None):
        programs = PROGRAMS.get_many({'public': 1}, sort_key='date', reverse=True)
        if level:
            programs = [x for x in programs if x.get('level') == int(level)]
        if adventure:
            # If the adventure we filter on is called 'default' -> return all programs WITHOUT an adventure
            if adventure == "default":
                programs = [x for x in programs if x.get('adventure_name') == ""]
                return programs[-48:]
            programs = [x for x in programs if x.get('adventure_name') == adventure]
        return programs[-48:]

    def get_all_favourite_programs(self):
        return PROGRAMS.get_many({'hedy_choice': True}, sort_key='date', reverse=True)

    def get_favourite_programs(self):
        return PROGRAMS.get_many({'hedy_choice': True}, sort_key='date', limit=4, reverse=True)

    def all_programs_count(self):
        """Return the total number of all programs."""
        return PROGRAMS.item_count()

    def all_users_count(self):
        """Return the total number of all users."""
        return USERS.item_count()

    def get_class(self, id):
        """Return the classes with given id."""
        return CLASSES.get({'id': id})

    def get_teacher_classes(self, username, students_to_list):
        """Return all the classes belonging to a teacher."""
        classes = None
        if isinstance(storage, dynamo.AwsDynamoStorage):
            classes = CLASSES.get_many({'teacher': username}, reverse=True)

        # If we're using the in-memory database, we need to make a shallow copy
        # of the classes before changing the `students` key from a set to list,
        # otherwise the field will remain a list later and that will break the
        # set methods.
        #
        # FIXME: I don't understand what the above comment is saying, but I'm
        # skeptical that it's accurate.
        else:
            classes = []
            for Class in CLASSES.get_many({'teacher': username}, reverse=True):
                classes.append (Class.copy())
        if students_to_list:
            for Class in classes:
                if not 'students' in Class:
                    Class ['students'] = []
                else:
                    Class ['students'] = list (Class ['students'])
        return classes

    def get_teacher_students(self, username):
        """Return all the students belonging to a teacher."""
        students = []
        classes = CLASSES.get_many({'teacher': username}, reverse=True)
        for Class in classes:
            for student in Class.get ('students', []):
                if student not in students:
                    students.append (student)
        return students

    def get_adventure(self, adventure_id):
        return ADVENTURES.get({'id': adventure_id})

    def delete_adventure(self, adventure_id):
        # If we delete an adventure -> also delete is from possible class customizations
        teacher = self.get_adventure(adventure_id).get('creator', '')
        ADVENTURES.delete({'id': adventure_id})
        for Class in self.get_teacher_classes(teacher, True):
            customizations = self.get_class_customizations(Class.get('id'))
            if customizations and adventure_id in customizations.get('teacher_adventures',[]):
                customizations['teacher_adventures'].remove(adventure_id)
                self.update_class_customizations(customizations)


    def store_adventure(self, adventure):
        """Store an adventure."""
        ADVENTURES.create(adventure)

    def update_adventure(self, adventure_id, adventure):
        ADVENTURES.update({'id': adventure_id}, adventure)

    def get_teacher_adventures(self, username):
        return ADVENTURES.get_many({'creator': username})

    def all_adventures(self):
        return ADVENTURES.scan()

    def get_student_classes_ids(self, username):
        ids = USERS.get({'username': username}).get('classes')
        return list(ids) if ids else []

    def get_student_classes(self, username):
        """Return all the classes of which the user is a student."""
        classes = []
        for class_id in self.get_student_classes_ids(username):
            Class = self.get_class (class_id)
            classes.append ({'id': Class ['id'], 'name': Class ['name']})

        return classes

    def store_class(self, Class):
        """Store a class."""
        CLASSES.create(Class)

    def update_class(self, id, name):
        """Updates a class."""
        CLASSES.update({'id': id}, {'name': name})

    def add_student_to_class(self, class_id, student_id):
        """Adds a student to a class."""
        CLASSES.update ({'id': class_id}, {'students': dynamo.DynamoAddToStringSet (student_id)})
        USERS.update({'username': student_id}, {'classes': dynamo.DynamoAddToStringSet (class_id)})

    def remove_student_from_class(self, class_id, student_id):
        """Removes a student from a class."""
        CLASSES.update ({'id': class_id}, {'students': dynamo.DynamoRemoveFromStringSet (student_id)})
        USERS.update({'username': student_id}, {'classes': dynamo.DynamoRemoveFromStringSet (class_id)})

    def delete_class(self, Class):
        for student_id in Class.get ('students', []):
            Database.remove_student_from_class (self, Class ['id'], student_id)

        CUSTOMIZATIONS.del_many({'id': Class['id']})
        INVITATIONS.del_many({'class_id': Class['id']})
        CUSTOMIZATIONS.delete({'id': Class['id']})
        CLASSES.delete({'id': Class['id']})

    def resolve_class_link(self, link_id):
        return CLASSES.get({'link': link_id})

    def get_username_invite(self, username):
        return INVITATIONS.get({'username': username}) or None

    def add_class_invite(self, data):
        INVITATIONS.put(data)

    def remove_class_invite(self, username):
        INVITATIONS.delete({'username': username})

    def get_class_invites(self, class_id):
        return INVITATIONS.get_many({'class_id': class_id}) or []

    def all_classes(self):
        return CLASSES.scan()

    def delete_class_customizations(self, class_id):
        CUSTOMIZATIONS.delete({'id': class_id})

    def update_class_customizations(self, customizations):
        CUSTOMIZATIONS.put(customizations)

    def get_class_customizations(self, class_id):
        customizations = CUSTOMIZATIONS.get({'id': class_id})
        return customizations

    def get_student_class_customizations(self, user):
        student_classes = self.get_student_classes(user)
        if student_classes:
            class_customizations = self.get_class_customizations(student_classes[0]['id'])
            return class_customizations or {}
        return {}

    def progress_by_username(self, username):
        return ACHIEVEMENTS.get({'username': username})

    def achievements_by_username(self, username):
        progress_data = ACHIEVEMENTS.get({'username': username})
        if progress_data and 'achieved' in progress_data:
            return progress_data['achieved']
        else:
            return None

    def add_achievement_to_username(self, username, achievement):
        user_achievements = ACHIEVEMENTS.get({'username': username})
        if not user_achievements:
            user_achievements = {'username': username}
        if 'achieved' not in user_achievements:
            user_achievements['achieved'] = []
        if achievement not in user_achievements['achieved']:
            user_achievements['achieved'].append(achievement)
            ACHIEVEMENTS.put(user_achievements)

    def add_achievements_to_username(self, username, achievements):
        user_achievements = ACHIEVEMENTS.get({'username': username})
        if not user_achievements:
            user_achievements = {'username': username}
        if 'achieved' not in user_achievements:
            user_achievements['achieved'] = []
        for achievement in achievements:
            if achievement not in user_achievements['achieved']:
                user_achievements['achieved'].append(achievement)
        user_achievements['achieved'] = list(dict.fromkeys(user_achievements['achieved']))
        ACHIEVEMENTS.put(user_achievements)

    def add_commands_to_username(self, username, commands):
        user_achievements = ACHIEVEMENTS.get({'username': username})
        if not user_achievements:
            user_achievements = {'username': username}
        if 'commands' not in user_achievements:
            user_achievements['commands'] = []
        for command in commands:
            if command not in user_achievements['commands']:
                user_achievements['commands'].append(command)
        ACHIEVEMENTS.put(user_achievements)

    def increase_user_run_count(self, username):
        ACHIEVEMENTS.update({'username': username}, {'run_programs': dynamo.DynamoIncrement(1)})

    def increase_user_save_count(self, username):
        ACHIEVEMENTS.update({'username': username}, {'saved_programs': dynamo.DynamoIncrement(1)})

    def increase_user_submit_count(self, username):
        ACHIEVEMENTS.update({'username': username}, {'submitted_programs': dynamo.DynamoIncrement(1)})

    def update_public_profile(self, username, data):
        data['username'] = username
        PUBLIC_PROFILES.put(data)

    def set_favourite_program(self, username, program_id):
        # We can only set a favourite program is there is already a public profile
        data = PUBLIC_PROFILES.get({'username': username})
        if data:
            data['favourite_program'] = program_id
            self.update_public_profile(username, data)
            return True
        return False

    def get_public_profile_settings(self, username):
        return PUBLIC_PROFILES.get({'username': username})

    def forget_public_profile(self, username):
        PUBLIC_PROFILES.delete({'username': username})

    def add_quiz_started(self, id, level):
        key = {"id#level": f'{id}#{level}', 'week': self.to_year_week(date.today())}

        add_attributes = {'id': id, 'level': level, 'started': dynamo.DynamoIncrement()}

        return QUIZ_STATS.update(key, add_attributes)

    def add_quiz_finished(self, id, level, score):
        key = {"id#level": f'{id}#{level}', 'week': self.to_year_week(date.today())}

        add_attributes = {'id': id, 'level': level,
                          'finished': dynamo.DynamoIncrement(),
                          'scores': dynamo.DynamoAddToList(score)}

        return QUIZ_STATS.update(key, add_attributes)

    def get_quiz_stats(self, ids, start=None, end=None):
        start_week = self.to_year_week(self.parse_date(start, date(2022, 1, 1)))
        end_week = self.to_year_week(self.parse_date(end, date.today()))

        data = [QUIZ_STATS.get_many({'id': i, 'week': dynamo.Between(start_week, end_week)}, sort_key='week') for i in ids]
        return functools.reduce(operator.iconcat, data, [])

    def add_program_stats(self, id, level, exception):
        key = {"id#level": f'{id}#{level}', 'week': self.to_year_week(date.today())}

        add_attributes = {'id': id, 'level': level}
        if exception:
            add_attributes[exception] = dynamo.DynamoIncrement()
        else:
            add_attributes['successful_runs'] = dynamo.DynamoIncrement()

        return PROGRAM_STATS.update(key, add_attributes)

    def get_program_stats(self, ids, start=None, end=None):
        start_week = self.to_year_week(self.parse_date(start, date(2022, 1, 1)))
        end_week = self.to_year_week(self.parse_date(end, date.today()))

        data = [PROGRAM_STATS.get_many({'id': i, 'week': dynamo.Between(start_week, end_week)}, sort_key='week') for i in ids]
        return functools.reduce(operator.iconcat, data, [])

    def parse_date(self, d, default):
        return date(*map(int, d.split('-'))) if d else default

    def to_year_week(self, d):
        cal = d.isocalendar()
        return f'{cal[0]}-{cal[1]:02d}'
