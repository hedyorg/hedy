import functools
import operator
import itertools
from datetime import date, timedelta

from utils import timems, times

from . import dynamo
from . import querylog

storage = dynamo.AwsDynamoStorage.from_env() or dynamo.MemoryStorage("dev_database.json")

USERS = dynamo.Table(storage, "users", "username", indexes=[
    dynamo.Index("email"),
    dynamo.Index("epoch", sort_key="created")
])
TOKENS = dynamo.Table(storage, "tokens", "id", indexes=[
    dynamo.Index('id'),
    dynamo.Index('username'),
])
PROGRAMS = dynamo.Table(storage, "programs", "id", indexes=[
    dynamo.Index('username', sort_key='date', index_name='username-index'),
    dynamo.Index('hedy_choice', sort_key='date', index_name='hedy_choice-index'),
    # For the explore page, this index has 'level', 'lang' and 'adventure_name'
    dynamo.Index('public', sort_key='date'),

    # For the filtered view of the 'explore' page (keys_only so we don't duplicate other attributes unnecessarily)
    dynamo.Index('lang', sort_key='date', keys_only=True),
    dynamo.Index('level', sort_key='date', keys_only=True),
    dynamo.Index('adventure_name', sort_key='date', keys_only=True),
])
CLASSES = dynamo.Table(storage, "classes", "id", indexes=[
    dynamo.Index('teacher'),
    dynamo.Index('link'),
])

# A custom teacher adventure
# - id (str): id of the adventure
# - content (str): adventure text
# - creator (str): username (of a teacher account, hopefully)
# - date (int): timestamp of last update
# - level (int | str): level number, sometimes as an int, sometimes as a str
# - name (str): adventure name
# - public (bool): whether it can be shared
ADVENTURES = dynamo.Table(storage, "adventures", "id", indexes=[dynamo.Index("creator")])
INVITATIONS = dynamo.Table(
    storage, "class_invitations", partition_key="username", indexes=[dynamo.Index("class_id")]
)

# Class customizations
#
# Various columns with different meanings:
#
# These I'm quite sure about:
#
# - id (str): the identifier of the class this customization set applies to
# - levels (int[]): the levels available in this class
# - opening_dates ({ str -> str }): key is level nr as string, value is an ISO date
# - other_settings (str[]): string list with values like "hide_quiz", "hide_parsons"
# - sorted_adventures ({ str -> { from_teacher: bool, name: str }[] }):
#     for every level (key as string) the adventures to show, in order. If from_teacher
#     is False, the name of a built-in adventure. If from_teacher is true, name is the
#     id of a adventure in the ADVENTURES table. The id may refer to an adventure that
#     has been deleted. In that case, it should be ignored.
#
# These not so much:
#
# - level_thresholds ({ "quiz" -> int }): TODO don't know what this does
# - adventures: ({ str -> int[] }): probably a map indicating, for each adventure, what
#      levels it should be available in. It's sort of redundant with sorted_adventures,
#      so I'm not sure why it exists.
# - teacher_adventures (str[]): a list of all ids of the adventures that have been made
#      available to this class. This list is deprecated, all adventures a teacher created
#      are now automatically available to all of their classes.
CUSTOMIZATIONS = dynamo.Table(storage, "class_customizations", partition_key="id")
ACHIEVEMENTS = dynamo.Table(storage, "achievements", partition_key="username")
PUBLIC_PROFILES = dynamo.Table(storage, "public_profiles", partition_key="username")
PARSONS = dynamo.Table(storage, "parsons", "id")
STUDENT_ADVENTURES = dynamo.Table(storage, "student_adventures", "id")
CLASS_ERRORS = dynamo.Table(storage, "class_errors", "id")
# We use the epoch field to make an index on the users table, sorted by a different
# sort key. In our case, we want to sort by 'created', so that we can make an ordered
# list of users.
#
# We add an 'epoch' field so that we can make an index of (PK: epoch, SK: created).
# It doesn't matter what the 'epoch' field is, it just needs to have a predictable value
# that we know so we can query on it again.
# Once the users table starts to hit 10GB, we need to increase this number to make sure
# the new users to to separate partition, and at that point we need to query both
# partitions in the index (but that will most likely not happen any time soon...)
CURRENT_USER_EPOCH = 1

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
QUIZ_ANSWERS = dynamo.Table(storage, "quizAnswers", partition_key="user", sort_key="levelAttempt")

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
PROGRAM_STATS = dynamo.Table(
    storage, "program-stats", partition_key="id#level", sort_key="week", indexes=[dynamo.Index("id", "week")]
)

QUIZ_STATS = dynamo.Table(
    storage, "quiz-stats", partition_key="id#level", sort_key="week", indexes=[dynamo.Index("id", "week")]
)

# Program stats also includes a boolean array indicating the order of successful and non-successful runs.
# In order to not flood the database, this history array can maximally have 100 entries.
MAX_CHART_HISTORY_SIZE = 50


class Database:
    def record_quiz_answer(self, attempt_id, username, level, question_number, answer, is_correct):
        """Update the current quiz record with a new answer.

        Uses a DynamoDB update to add to the exising record. Expects answer to be A, B, C etc.
        """
        key = {
            "user": username,
            "levelAttempt": str(level).zfill(4) + "_" + attempt_id,
        }

        updates = {
            "attemptId": attempt_id,
            "level": level,
            "date": times(),
            "q" + str(question_number): dynamo.DynamoAddToList(answer),
        }

        if is_correct:
            updates["correct"] = dynamo.DynamoAddToNumberSet(int(question_number))

        return QUIZ_ANSWERS.update(key, updates)

    def get_quiz_answer(self, username, level, attempt_id):
        """Load a quiz answer from the database."""

        quizAnswers = QUIZ_ANSWERS.get({"user": username, "levelAttempt": str(level).zfill(4) + "_" + attempt_id})

        array_quiz_answers = []
        for question_number in range(len(quizAnswers)):
            answers = quizAnswers.get("q" + str(question_number))
            array_quiz_answers.append(answers)
        return array_quiz_answers

    def level_programs_for_user(self, username, level):
        """List level programs for the given user, newest first.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        # FIXME: Query by index, the current behavior is slow for many programs
        # (See https://github.com/hedyorg/hedy/issues/4121)
        programs = PROGRAMS.get_many({"username": username}, reverse=True)
        return [x for x in programs if x.get("level") == int(level)]

    def last_level_programs_for_user(self, username, level):
        """Return the most recent program for the given user at a given level.

        Returns: { adventure_name -> { code, name, ... } }
        """
        programs = self.level_programs_for_user(username, level)
        ret = {}
        for program in programs:
            key = program.get('adventure_name', 'default')
            if key not in ret or ret[key]['date'] < program['date']:
                ret[key] = program
        return ret

    def programs_for_user(self, username):
        """List programs for the given user, newest first.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        return PROGRAMS.get_many({"username": username}, reverse=True)

    def filtered_programs_for_user(self, username, level=None, adventure=None, submitted=None,
                                   limit=None, pagination_token=None):
        ret = []

        # FIXME: Query by index, the current behavior is slow for many programs
        # (See https://github.com/hedyorg/hedy/issues/4121)
        programs = dynamo.GetManyIterator(PROGRAMS, {"username": username},
                                          reverse=True, batch_size=limit, pagination_token=pagination_token)
        for program in programs:
            if level and program.get('level') != int(level):
                continue
            if adventure:
                if adventure == 'default' and program.get('adventure_name') != '':
                    continue
                if adventure != 'default' and program.get('adventure_name') != adventure:
                    continue
            if submitted is not None:
                if program.get('submitted') != submitted:
                    continue

            ret.append(program)

            if len(ret) >= limit:
                break

        return dynamo.ResultPage(ret, programs.next_page_token)

    def public_programs_for_user(self, username, limit=None, pagination_token=None):
        # Only return programs that are public but not submitted
        programs = dynamo.GetManyIterator(PROGRAMS, {"username": username},
                                          reverse=True, batch_size=limit, pagination_token=pagination_token)
        ret = []
        for program in programs:
            if program.get("public") != 1 or program.get("submitted", False):
                continue
            ret.append(program)

            if limit is not None and len(ret) >= limit:
                break

        return dynamo.ResultPage(ret, programs.next_page_token)

    def program_by_id(self, id):
        """Get program by ID.

        Returns: { code, name, program, level, adventure_name, date }
        """
        return PROGRAMS.get({"id": id})

    def store_program(self, program):
        """Store a program.

        Returns the program.

        Add an additional indexable field: 'username_level'.
        """
        PROGRAMS.create(
            dict(program,
                 username_level=f"{program.get('username')}-{program.get('level')}"))

        return program

    def update_program(self, id, updates):
        """Update fields of an existing program.

        Returns the updated state of the program.
        """
        return PROGRAMS.update(dict(id=id), updates)

    def set_program_public_by_id(self, id, public):
        """Switch a program to public or private.

        Return the updated state of the program.
        """
        return PROGRAMS.update({"id": id}, {"public": 1 if public else 0})

    def submit_program_by_id(self, id):
        """Switch a program to submitted.

        Return the updated program state.
        """
        return PROGRAMS.update({"id": id}, {"submitted": True, "date": timems()})

    def delete_program_by_id(self, id):
        """Delete a program by id."""
        PROGRAMS.delete({"id": id})

    def student_adventure_by_id(self, id):
        # Fetch a student adventure with id formatted as studentID-adventureName-level
        return STUDENT_ADVENTURES.get({"id": id})

    def update_student_adventure(self, id, ticked):
        # Swap the ticked value when a request is sent
        return STUDENT_ADVENTURES.update({"id": id}, {"ticked": not ticked})

    def store_student_adventure(self, student_adventure):
        # Store the adventure data in this table in case it doesn't match the programs table.
        STUDENT_ADVENTURES.create(student_adventure)
        return student_adventure

    def get_class_errors(self, class_id):
        # Fetch a student adventure with id formatted as studentID-adventureName-level
        return CLASS_ERRORS.get({"id": class_id})

    def update_class_errors(self, class_errors):
        # Swap the ticked value when a request is sent
        return CLASS_ERRORS.put(class_errors)

    def store_class_errors(self, class_errors):
        # create a new class errors object
        CLASS_ERRORS.create(class_errors)
        return class_errors

    def increase_user_program_count(self, username, delta=1):
        """Increase the program count of a user by the given delta."""
        return USERS.update({"username": username}, {"program_count": dynamo.DynamoIncrement(delta)})

    def user_by_username(self, username):
        """Return a user object from the username."""
        return USERS.get({"username": username.strip().lower()})

    def user_by_email(self, email):
        """Return a user object from the email address."""
        return USERS.get({"email": email.strip().lower()})

    def get_token(self, token_id):
        """Load a token from the database."""
        return TOKENS.get({"id": token_id})

    def store_token(self, token):
        """Store a token in the database."""
        TOKENS.create(token)

    def forget_token(self, token_id):
        """Forget a Token.

        Returns the Token that was deleted.
        """
        return TOKENS.delete({"id": token_id})

    def delete_all_tokens(self, username):
        """Forget all Tokens from a user."""
        TOKENS.del_many({"username": username})

    def store_user(self, user):
        """Store a user in the database."""
        user["epoch"] = CURRENT_USER_EPOCH
        USERS.create(user)

    def record_login(self, username, new_password_hash=None):
        """Record the fact that the user logged in, potentially updating their password hash."""
        if new_password_hash:
            self.update_user(username, {"password": new_password_hash, "last_login": timems()})
        else:
            self.update_user(username, {"last_login": timems()})

    def update_user(self, username, userdata):
        """Update the user data with the given fields.

        This method is a bit of a failing of the API, but there are too many
        slight variants of tweaking some fields on the user in the code to
        turn each of them into a separate method here.
        """
        USERS.update({"username": username}, userdata)

    def forget_user(self, username):
        """Forget the given user."""
        classes = USERS.get({"username": username}).get("classes") or []
        USERS.delete({"username": username})
        INVITATIONS.delete({"username": username})
        # The recover password token may exist, so we delete it
        TOKENS.delete({"id": username})
        PROGRAMS.del_many({"username": username})

        # Remove user from classes of which they are a student
        for class_id in classes:
            self.remove_student_from_class(class_id, username)

        # Delete classes owned by the user
        for Class in self.get_teacher_classes(username, False):
            self.delete_class(Class)

    def all_users(self, page_token=None):
        """Return a page from the users table.

        There may be more users to retrieve. If so, the returned page object
        will have a 'next_page_token' attribute to continue retrieval.

        The pagination token will be of the form '<epoch>:<pagination_token>'
        """
        limit = 500

        epoch, pagination_token = (
            page_token.split(":", maxsplit=1) if page_token is not None else (CURRENT_USER_EPOCH, None)
        )
        epoch = int(epoch)

        page = USERS.get_many(dict(epoch=epoch), pagination_token=pagination_token, limit=limit, reverse=True)

        # If we are not currently at epoch > 1 and there are no more records in the current
        # epoch, also include the first page of the next epoch.
        if not page.next_page_token and epoch > 1:
            epoch -= 1
            next_epoch_page = USERS.get_many(dict(epoch=epoch), reverse=True, limit=limit)

            # Build a new result page with both sets of records, ending with the next "next page" token
            page = dynamo.ResultPage(list(page) + list(next_epoch_page), next_epoch_page.next_page_token)

        # Prepend the epoch to the next pagination token
        if page.next_page_token:
            page.next_page_token = f"{epoch}:{page.next_page_token}"
        return page

    def get_all_public_programs(self):
        programs = PROGRAMS.get_many({"public": 1}, reverse=True)
        return [x for x in programs if not x.get("submitted", False)]

    @querylog.timed_as("get_public_programs")
    def get_public_programs(self, level_filter=None, language_filter=None, adventure_filter=None, limit=40):
        """Return the most recent N public programs, optionally filtered by attributes.

        The 'public' index is the most discriminatory: fetch public programs, then evaluate them against
        the filters (on the server). The index we're using here has the 'lang', 'adventure_name' and
        'level' columns.
        """
        filter = {}
        if level_filter:
            filter['level'] = int(level_filter)
        if language_filter:
            filter['lang'] = language_filter
        if adventure_filter:
            filter['adventure_name'] = adventure_filter

        timeout = dynamo.Cancel.after_timeout(timedelta(seconds=3))
        id_batch_size = 200

        found_program_ids = []
        pagination_token = None
        while len(found_program_ids) < limit and not timeout.is_cancelled():
            page = PROGRAMS.get_many({'public': 1}, reverse=True, limit=id_batch_size,
                                     pagination_token=pagination_token, filter=filter)
            found_program_ids.extend([{'id': r['id']} for r in page])
            pagination_token = page.next_page_token
            if pagination_token is None:
                break
        del found_program_ids[limit:]  # Cap off in case we found too much

        # Now retrieve all programs we found with a batch-get
        found_programs = PROGRAMS.batch_get(found_program_ids)
        return found_programs

    def add_public_profile_information(self, programs):
        """For each program in a list, note whether the author has a public profile or not.

        For each program, add 'public_user': True or 'public_user': None.

        Modifies the records in the list in-place.
        """
        queries = {p['id']: {'username': p['username'].strip().lower()} for p in programs}
        profiles = PUBLIC_PROFILES.batch_get(queries)

        for program in programs:
            program['public_user'] = True if profiles[program['id']] else None

    def get_highscores(self, username, filter, filter_value=None):
        profiles = []

        # If the filter is global or country -> get all public profiles
        if filter == "global" or filter == "country":
            profiles = self.get_all_public_profiles()
        # If it's a class, only get the ones from your class
        elif filter == "class":
            Class = self.get_class(filter_value)
            customizations = self.get_class_customizations(Class.get("id"))
            for student in Class.get("students", []):
                profile = self.get_public_profile_settings(student)
                if profile:
                    profiles.append(profile)
                # If the user doesn't have a public profile the situation depends on the customizations
                # If the teacher has allowed the "all public" function -> add dummy profile to make all visible
                # Give the profile an extra attribute to clarify we don't update any non-existing public-profile
                elif customizations and "all_highscores" in customizations.get("other_settings", []):
                    profiles.append({"username": student, "no_public_profile": True})

        for profile in profiles:
            if not profile.get("country"):
                try:
                    country = self.user_by_username(profile.get("username")).get("country")
                    if not profile.get("no_public_profile"):
                        self.update_country_public_profile(profile.get("username"), country)
                except AttributeError:
                    print("This profile username is invalid...")
                    country = None
                profile["country"] = country
            if not profile.get("achievements"):
                achievements = self.achievements_by_username(profile.get("username"))
                if not profile.get("no_public_profile"):
                    self.update_achievements_public_profile(profile.get("username"), len(achievements) or 0)
                else:
                    # As the last achievement timestamp is stored on the public profile -> create an artificial one
                    # We don't have a choice, otherwise the double sorting below will crash
                    # Todo TB -> Store last achievement on achievements data instead of public profile data (11-11-22)
                    profile["last_achievement"] = timems()
                profile["achievements"] = len(achievements) if achievements else 0

        # If we filter on country, make sure to filter out all non-country values
        if filter == "country":
            profiles = [x for x in profiles if x.get("country") == filter_value]

        # Perform a double sorting: first by achievements (high-low), then by timestamp (low-high)
        profiles = sorted(profiles, key=lambda k: (k.get("achievements"), -k.get("last_achievement")), reverse=True)

        # Add ranking for each profile
        ranking = 1
        for profile in profiles:
            profile["ranking"] = ranking
            ranking += 1

        # If the user is not in the current top 50: still append to the results
        if not any(d["username"] == username for d in profiles[:50]):
            return profiles[:50] + [i for i in profiles if i["username"] == username]
        return profiles[:50]

    def get_all_hedy_choices(self):
        return PROGRAMS.get_many({"hedy_choice": 1}, reverse=True)

    def get_hedy_choices(self):
        return PROGRAMS.get_many({"hedy_choice": 1}, limit=4, reverse=True)

    def set_program_as_hedy_choice(self, id, favourite):
        PROGRAMS.update({"id": id}, {"hedy_choice": 1 if favourite else None})

    def get_class(self, id):
        """Return the classes with given id."""
        return CLASSES.get({"id": id})

    def get_teacher_classes(self, username, students_to_list=False):
        """Return all the classes belonging to a teacher."""
        classes = None
        if isinstance(storage, dynamo.AwsDynamoStorage):
            classes = CLASSES.get_many({"teacher": username}, reverse=True)

        # If we're using the in-memory database, we need to make a shallow copy
        # of the classes before changing the `students` key from a set to list,
        # otherwise the field will remain a list later and that will break the
        # set methods.
        #
        # FIXME: I don't understand what the above comment is saying, but I'm
        # skeptical that it's accurate.
        else:
            classes = []
            for Class in CLASSES.get_many({"teacher": username}, reverse=True):
                classes.append(Class.copy())
        if students_to_list:
            for Class in classes:
                if "students" not in Class:
                    Class["students"] = []
                else:
                    Class["students"] = list(Class["students"])
        return classes

    def get_teacher_students(self, username):
        """Return all the students belonging to a teacher."""
        students = []
        classes = CLASSES.get_many({"teacher": username}, reverse=True)
        for Class in classes:
            for student in Class.get("students", []):
                if student not in students:
                    students.append(student)
        return students

    def get_adventure(self, adventure_id):
        return ADVENTURES.get({"id": adventure_id})

    def batch_get_adventures(self, adventure_ids):
        """From a list of adventure ids, return a map of { id -> adventure }."""
        keys = {id: {"id": id} for id in adventure_ids}
        return ADVENTURES.batch_get(keys) if keys else {}

    def delete_adventure(self, adventure_id):
        ADVENTURES.delete({"id": adventure_id})

    def store_adventure(self, adventure):
        """Store an adventure."""
        ADVENTURES.create(adventure)

    def update_adventure(self, adventure_id, adventure):
        ADVENTURES.update({"id": adventure_id}, adventure)

    def get_teacher_adventures(self, username):
        return ADVENTURES.get_many({"creator": username})

    def all_adventures(self):
        return ADVENTURES.scan()

    def get_student_classes_ids(self, username):
        ids = USERS.get({"username": username}).get("classes")
        return list(ids) if ids else []

    def get_student_classes(self, username):
        """Return all the classes of which the user is a student."""
        classes = []
        for class_id in self.get_student_classes_ids(username):
            Class = self.get_class(class_id)
            classes.append({"id": Class["id"], "name": Class["name"]})

        return classes

    def store_class(self, Class):
        """Store a class."""
        CLASSES.create(Class)

    def update_class(self, id, name):
        """Updates a class."""
        CLASSES.update({"id": id}, {"name": name})

    def add_student_to_class(self, class_id, student_id):
        """Adds a student to a class."""
        CLASSES.update({"id": class_id}, {"students": dynamo.DynamoAddToStringSet(student_id)})
        USERS.update({"username": student_id}, {"classes": dynamo.DynamoAddToStringSet(class_id)})

    def remove_student_from_class(self, class_id, student_id):
        """Removes a student from a class."""
        CLASSES.update({"id": class_id}, {"students": dynamo.DynamoRemoveFromStringSet(student_id)})
        USERS.update({"username": student_id}, {"classes": dynamo.DynamoRemoveFromStringSet(class_id)})

    def delete_class(self, Class):
        for student_id in Class.get("students", []):
            Database.remove_student_from_class(self, Class["id"], student_id)

        CUSTOMIZATIONS.del_many({"id": Class["id"]})
        INVITATIONS.del_many({"class_id": Class["id"]})
        CUSTOMIZATIONS.delete({"id": Class["id"]})
        CLASSES.delete({"id": Class["id"]})

    def resolve_class_link(self, link_id):
        return CLASSES.get({"link": link_id})

    def get_username_invite(self, username):
        return INVITATIONS.get({"username": username}) or None

    def add_class_invite(self, data):
        INVITATIONS.put(data)

    def remove_class_invite(self, username):
        INVITATIONS.delete({"username": username})

    def get_class_invites(self, class_id):
        return INVITATIONS.get_many({"class_id": class_id}) or []

    def all_classes(self):
        return CLASSES.scan()

    def delete_class_customizations(self, class_id):
        CUSTOMIZATIONS.delete({"id": class_id})

    def update_class_customizations(self, customizations):
        CUSTOMIZATIONS.put(customizations)

    def get_class_customizations(self, class_id):
        customizations = CUSTOMIZATIONS.get({"id": class_id})
        return customizations

    def get_student_class_customizations(self, user):
        """Return customizations for the very first class this user is part of.

        If the user is part of multiple classes, they will only get the customizations
        of the first class.
        """
        student_classes = self.get_student_classes(user)
        if student_classes:
            class_customizations = self.get_class_customizations(student_classes[0]["id"])
            return class_customizations or {}
        return {}

    def progress_by_username(self, username):
        return ACHIEVEMENTS.get({"username": username})

    def achievements_by_username(self, username):
        progress_data = ACHIEVEMENTS.get({"username": username})
        if progress_data and "achieved" in progress_data:
            return progress_data["achieved"]
        else:
            return None

    def get_all_achievements(self):
        return ACHIEVEMENTS.scan()

    def add_achievement_to_username(self, username, achievement):
        new_user = False
        user_achievements = ACHIEVEMENTS.get({"username": username})
        if not user_achievements:
            new_user = True
            user_achievements = {"username": username}
        if "achieved" not in user_achievements:
            user_achievements["achieved"] = []
        if achievement not in user_achievements["achieved"]:
            user_achievements["achieved"].append(achievement)
            ACHIEVEMENTS.put(user_achievements)
        # Update the amount of achievements on the public profile (if exists)
        self.update_achievements_public_profile(username, len(user_achievements["achieved"]))
        if new_user:
            return True
        return False

    def add_achievements_to_username(self, username, achievements):
        new_user = False
        user_achievements = ACHIEVEMENTS.get({"username": username})
        if not user_achievements:
            new_user = True
            user_achievements = {"username": username}
        if "achieved" not in user_achievements:
            user_achievements["achieved"] = []
        for achievement in achievements:
            if achievement not in user_achievements["achieved"]:
                user_achievements["achieved"].append(achievement)
        user_achievements["achieved"] = list(dict.fromkeys(user_achievements["achieved"]))
        ACHIEVEMENTS.put(user_achievements)

        # Update the amount of achievements on the public profile (if exists)
        self.update_achievements_public_profile(username, len(user_achievements["achieved"]))
        if new_user:
            return True
        return False

    def add_commands_to_username(self, username, commands):
        user_achievements = ACHIEVEMENTS.get({"username": username})
        if not user_achievements:
            user_achievements = {"username": username}
        user_achievements["commands"] = commands
        ACHIEVEMENTS.put(user_achievements)

    def increase_user_run_count(self, username):
        ACHIEVEMENTS.update({"username": username}, {"run_programs": dynamo.DynamoIncrement(1)})

    def increase_user_save_count(self, username):
        ACHIEVEMENTS.update({"username": username}, {"saved_programs": dynamo.DynamoIncrement(1)})

    def increase_user_submit_count(self, username):
        ACHIEVEMENTS.update({"username": username}, {"submitted_programs": dynamo.DynamoIncrement(1)})

    def update_public_profile(self, username, data):
        PUBLIC_PROFILES.update({"username": username}, data)

    def update_achievements_public_profile(self, username, amount_achievements):
        data = PUBLIC_PROFILES.get({"username": username})
        # In the case that we make this call but there is no public profile -> don't do anything
        if data:
            PUBLIC_PROFILES.update(
                {"username": username}, {"achievements": amount_achievements, "last_achievement": timems()}
            )

    def update_country_public_profile(self, username, country):
        data = PUBLIC_PROFILES.get({"username": username})
        # If there is no data -> we might have made this request from the /update_profile route without a public profile
        # In this case don't do anything
        if data:
            PUBLIC_PROFILES.update({"username": username}, {"country": country})

    def set_favourite_program(self, username, program_id):
        # We can only set a favourite program is there is already a public profile
        data = PUBLIC_PROFILES.get({"username": username})
        if data:
            data["favourite_program"] = program_id
            self.update_public_profile(username, data)
            return True
        return False

    def get_public_profile_settings(self, username):
        return PUBLIC_PROFILES.get({"username": username})

    def forget_public_profile(self, username):
        PUBLIC_PROFILES.delete({"username": username})

    def get_all_public_profiles(self):
        return PUBLIC_PROFILES.scan()

    def store_parsons(self, attempt):
        PARSONS.create(attempt)

    def add_quiz_started(self, id, level):
        key = {"id#level": f"{id}#{level}", "week": self.to_year_week(date.today())}

        add_attributes = {"id": id, "level": level, "started": dynamo.DynamoIncrement()}

        return QUIZ_STATS.update(key, add_attributes)

    def add_quiz_finished(self, id, level, score):
        key = {"id#level": f"{id}#{level}", "week": self.to_year_week(date.today())}

        add_attributes = {
            "id": id,
            "level": level,
            "finished": dynamo.DynamoIncrement(),
            "scores": dynamo.DynamoAddToList(score),
        }

        return QUIZ_STATS.update(key, add_attributes)

    def get_quiz_stats(self, ids, start=None, end=None):
        start_week = self.to_year_week(self.parse_date(start, date(2022, 1, 1)))
        end_week = self.to_year_week(self.parse_date(end, date.today()))

        data = [QUIZ_STATS.get_many({"id": i, "week": dynamo.Between(start_week, end_week)}) for i in ids]
        return functools.reduce(operator.iconcat, data, [])

    def add_program_stats(self, id, level, number_of_lines, exception, error_message=None):
        key = {"id#level": f"{id}#{level}", "week": self.to_year_week(date.today())}
        add_attributes = {"id": id, "level": level, "number_of_lines": number_of_lines}
        program_stats = PROGRAM_STATS.get_many({"id": id, "week": self.to_year_week(date.today())})

        # chart history and error history are used for visual elements on the live dashboard, see statistics.py
        # for how they are read from the database
        chart_history = []
        if program_stats.records:
            chart_history = program_stats.records[0].get('chart_history', [])
        chart_slice = MAX_CHART_HISTORY_SIZE if len(chart_history) > MAX_CHART_HISTORY_SIZE else 0

        if exception:
            add_attributes[exception] = dynamo.DynamoIncrement()
            new_chart_history = list(chart_history) + [0]
        else:
            add_attributes["successful_runs"] = dynamo.DynamoIncrement()
            new_chart_history = list(chart_history) + [1]
        add_attributes["chart_history"] = new_chart_history[-chart_slice:]

        return PROGRAM_STATS.update(key, add_attributes)

    def get_program_stats(self, ids, start=None, end=None):
        end_week = self.to_year_week(self.parse_date(end, date.today()))

        from datetime import timedelta
        one_week_ago = date.today() - timedelta(days=7)
        start_week = self.to_year_week(self.parse_date(start, one_week_ago))

        data = [PROGRAM_STATS.get_many({"id": i, "week": dynamo.Between(start_week, end_week)}) for i in ids]
        return functools.reduce(operator.iconcat, data, [])

    def parse_date(self, d, default):
        return date(*map(int, d.split("-"))) if d else default

    def to_year_week(self, d):
        cal = d.isocalendar()
        return f"{cal[0]}-{cal[1]:02d}"

    def get_username_role(self, username):
        role = "teacher" if USERS.get({"username": username}).get("teacher_request") is True else "student"
        return role


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch
