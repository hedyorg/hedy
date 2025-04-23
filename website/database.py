"""Data layer for Hedy.

This file defines all DynamoDB tables that make up the Hedy data model,
as well as the class 'Database' which can be used to access those tables.

THE DATABASE CLASS
-------------------

The Database class should implement logical operations that make sense
for the data model, spanning multiple tables if necessary. As much as you
can, hide the details of how data is stored in and queried from tables so
that the front-end doesn't have to think about those details.

TYPE ANNOTATIONS
----------------

The tables below have type annotations. Type annotations will be used
to validate records that are stored INTO the database; they are not
used to validate records that are retrieved from the database.

!!! You cannot assume that records retrieved from a table will always have
    the fields of the types that are listed in the table definition!

The record could be older than the validation that was added. Always
program defensively!
"""

import functools
import operator
import itertools
from datetime import date
import sys
from os import path

from utils import timems, times
import utils
from config import config

from . import dynamo, auth

from .dynamo import DictOf, OptionalOf, ListOf, SetOf, RecordOf, EitherOf

from hedy_content import MAX_LEVEL

is_offline = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


# Program stats also includes a boolean array indicating the order of successful and non-successful runs.
# In order to not flood the database, this history array can maximally have 100 entries.
MAX_CHART_HISTORY_SIZE = 50

# We use the epoch field to make an index on the users table, sorted by a different
# sort key. In our case, we want to sort by 'created', so that we can make an ordered
# list of users.
#
# We add an 'epoch' field so that we can make an index of (PK: epoch, SK: created).
# It doesn't matter what the 'epoch' field is, it just needs to have a predictable value
# that we know so we can query on it again.
# Once the users table starts to hit 10GB (~30M users), we need to increase this
# number to make sure the new users to to separate partition, and at that point
# we need to query both partitions in the index (but that will most likely not
# happen any time soon...)
CURRENT_USER_EPOCH = 1


class Database:
    def __init__(self, for_testing=False):
        if for_testing:
            # In-memory testing: empty database that does not get persisted to disk
            storage = dynamo.MemoryStorage()
            is_dev = True
        elif is_offline:
            # Offline mode. Store data 1 directory upwards from `_internal`
            storage = dynamo.MemoryStorage(path.join(sys._MEIPASS, "..", "database.json"))
            is_dev = False
        elif storage := dynamo.AwsDynamoStorage.from_env():
            # Production: use environment variables
            is_dev = False
        else:
            # Use dev storage
            is_dev = True
            storage = dynamo.MemoryStorage("dev_database.json")

        self.storage = storage

        def only_in_dev(x):
            """Return the argument only in debug mode. In production or offline mode, return None.

            This is intended to be used with validation expressions, so that when testing
            locally we do validation, but production data that happens to work but doesn't
            validate doesn't throw exceptions.
            """
            return x if is_dev else None

        self.class_errors = dynamo.Table(storage, "class_errors", "id",
                                         types=only_in_dev({'id': str}),
                                         )
        self.users = dynamo.Table(storage, 'users', 'username',
                                  types=only_in_dev({
                                      'username': str,
                                      'password': str,
                                      'email': OptionalOf(str),
                                      'language': OptionalOf(str),
                                      'keyword_language': OptionalOf(str),
                                      'created': int,
                                      'is_teacher': OptionalOf(int),
                                      'verification_pending': OptionalOf(str),
                                      'last_login': int,
                                      'country': OptionalOf(str),
                                      'birth_year': OptionalOf(int),
                                      'gender': OptionalOf(str),
                                      'heard_about': OptionalOf(ListOf(str)),
                                      'prog_experience': OptionalOf(str),
                                      'experience_languages': OptionalOf(ListOf(str)),
                                      'epoch': int,
                                      'second_teacher_in': OptionalOf(ListOf(str)),
                                      'classes': OptionalOf(SetOf(str)),
                                      'teacher': OptionalOf(str),
                                      'pair_with_teacher': OptionalOf(int),
                                      'teacher_request': OptionalOf(bool),
                                      'is_super_teacher': OptionalOf(int),
                                      'certificate': OptionalOf(bool),
                                  }),
                                  indexes=[
                                      dynamo.Index('email'),
                                      dynamo.Index('epoch', sort_key='created'),
                                      dynamo.Index('epoch', sort_key='username', keys_only=True)
                                  ]
                                  )
        self.tokens = dynamo.Table(storage, 'tokens', 'id',
                                   types=only_in_dev({
                                       'id': str,
                                       'username': str,
                                       'ttl': int,
                                   }),
                                   indexes=[
                                       dynamo.Index('username'),
                                   ]
                                   )
        self.programs = dynamo.Table(storage, "programs", "id",
                                     types=only_in_dev({
                                         'id': str,
                                         'session': str,
                                         'username': str,
                                         'date': int,
                                         'hedy_choice': OptionalOf(int),
                                         'public': OptionalOf(int),
                                         'lang': str,
                                         'level': int,
                                         'code': str,
                                         'adventure_name': str,
                                         'name': str,
                                         'username_level': str,
                                         'error': OptionalOf(bool),
                                         'is_modified': OptionalOf(bool)
                                     }),
                                     indexes=[
                                         dynamo.Index('username', sort_key='date', index_name='username-index'),
                                         dynamo.Index('hedy_choice', sort_key='date', index_name='hedy_choice-index'),
                                         # For the explore page, this index has 'level', 'lang' and 'adventure_name'
                                         dynamo.Index('public', sort_key='date'),

                                         # For the filtered view of the 'explore' page (keys_only so we don't duplicate
                                         # other attributes unnecessarily)
                                         dynamo.Index('lang', sort_key='date', keys_only=True),
                                         dynamo.Index('level', sort_key='date', keys_only=True),
                                         dynamo.Index('adventure_name', sort_key='date', keys_only=True),
                                     ]
                                     )
        self.classes = dynamo.Table(storage, "classes", "id",
                                    types=only_in_dev({
                                        'id': str,
                                        'teacher': str,
                                        # TODO: remove once we deploy new redesign
                                        'link': str,
                                        'date': int,
                                        'name': str,
                                        'second_teachers': OptionalOf(ListOf(RecordOf({
                                            'role': str,
                                            'username': str,
                                        }))),
                                        'students': OptionalOf(SetOf(str)),
                                        'last_viewed_level': OptionalOf(int)
                                    }),
                                    indexes=[
                                        dynamo.Index('teacher'),
                                        # TODO: remove once we deploy new redesign
                                        # also remove from Dynamo AWS console
                                        dynamo.Index('link'),
                                    ]
                                    )

        # A custom teacher adventure
        # - id (str): id of the adventure
        # - content (str): adventure text
        # - creator (str): username (of a teacher account, hopefully). This originally was the person
        #       who created and owned an adventure before we had cloning. Now that we have cloning, this
        #       field is better understood as 'owner'.
        # - author (str): username (of a teacher account, hopefully). If present, this is the person
        #       who originally authored the adventure even throughout cloning.
        # - date (int): timestamp of last update (in milliseconds, JavaScript timestamp)
        # - level (str): level number, sometimes as an int, usually as a str
        # - levels: [str]: levels of the adventure
        # - name (str): adventure name
        # - public (int): 1 or 0 whether it can be shared
        # - tags_id (str): list of tags that describe this adventure.
        self.adventures = dynamo.Table(storage, "adventures", "id",
                                       types=only_in_dev({
                                           'id': str,
                                           'date': int,
                                           'creator': str,
                                           'name': str,
                                           'classes': OptionalOf(ListOf(str)),
                                           'level': EitherOf(str, int),  # this might be a string or a int
                                           'levels': ListOf(str),
                                           'content': str,
                                           'public': int,
                                           'language': str,
                                           'formatted_content': OptionalOf(str)
                                       }),
                                       indexes=[
                                           dynamo.Index("creator"),
                                           dynamo.Index("public"),
                                           dynamo.Index("language", keys_only=True),
                                           dynamo.Index("name", sort_key="creator", index_name="name-creator-index")
                                       ])
        self.invitations = dynamo.Table(
            storage, "invitations", partition_key="username#class_id",
            types=only_in_dev({
                'username': str,
                'class_id': str,
                'timestamp': int,
                'ttl': int,
                'invited_as': str,
                'invited_as_text': str,
                'username#class_id': str
            }),
            indexes=[
                dynamo.Index("username"),
                dynamo.Index("class_id"),
            ],
        )

        """
        # TAGS
            - id
            - name (str): tag name.
            - tagged_in ([{ id, public, language }]): tagged in which adventures.
            - popularity (int): # of adventures it's been tagged in.
        """
        self.tags = dynamo.Table(storage, "tags", "id",
                                 types=only_in_dev({
                                     'id': str,
                                     'name': str,
                                     'popularity': int,
                                     'tagged_in': OptionalOf(ListOf(RecordOf({
                                         'id': str,
                                         'public': int,
                                         'language': str
                                     })))
                                 }),
                                 indexes=[
                                     dynamo.Index("name", sort_key="popularity")
                                 ]
                                 )

        # A survey
        # - id (str): the identifier of the survey + the response identifier ex. "class_teacher1" or "students_student1"
        # - responses (str []): the response per question
        # - skip (str): if the survey should never be shown or today date to be reminded later

        self.surveys = dynamo.Table(storage, "surveys", "id",
                                    types=only_in_dev({
                                        'id': str,
                                        'responses':  OptionalOf(DictOf({
                                            str: RecordOf({
                                                'answer': str,
                                                'question': str
                                            })
                                        }))
                                    }),
                                    )

        self.feedback = dynamo.Table(storage, "teacher_feedback", "id",
                                     types=only_in_dev({
                                         'id': str,
                                         'username': str,
                                         'email': str,
                                         'message': str,
                                         'category': str,
                                         'page': str,
                                         'date': int
                                     }))

        # Class customizations
        #
        # - id (str): the identifier of the class this customization set applies to
        # - levels (int[]): the levels available in this class
        # - opening_dates ({ str -> str }): key is level nr as string, value is an ISO date
        # - other_settings (str[]): string list with values like "hide_quiz", "hide_parsons"
        # - sorted_adventures ({ str -> { from_teacher: bool, name: str }[] }):
        #     for every level (key as string) the adventures to show, in order. If from_teacher
        #     is False, the name of a built-in adventure. If from_teacher is true, name is the
        #     id of a adventure in the ADVENTURES table. The id may refer to an adventure that
        #     has been deleted. In that case, it should be ignored
        # - level_thresholds ({ "quiz" -> int }): the minimum quiz grade that unlocks the next level
        # - quiz_parsons_tabs_migrated if the customizations in this tab already have quiz
        #    and parson tabs in sorted adventures
        self.customizations = dynamo.Table(storage, "class_customizations", partition_key="id",
                                           types=only_in_dev({
                                               'id': str,
                                               'levels': ListOf(int),
                                               'opening_dates': DictOf({
                                                   str: str
                                               }),
                                               'other_settings': ListOf(str),
                                               'level_thresholds': DictOf({
                                                   str: int
                                               }),
                                               'sorted_adventures': DictOf({
                                                   str: ListOf(RecordOf({
                                                       'name': str,
                                                       'from_teacher': bool
                                                   }))
                                               }),
                                               'updated_by': OptionalOf(str),
                                               'quiz_parsons_tabs_migrated': OptionalOf(int)
                                           }))

        self.achievements = dynamo.Table(storage, "achievements", partition_key="username",
                                         types=only_in_dev({
                                             'username': str,
                                             'achieved': OptionalOf(ListOf(str)),
                                             'commands': OptionalOf(ListOf(str)),
                                             'saved_programs': OptionalOf(int),
                                             'run_programs': OptionalOf(int)
                                         }))
        self.public_profiles = dynamo.Table(storage, "public_profiles", partition_key="username",
                                            types=only_in_dev({
                                                'username': str,
                                                'image': str,
                                                'personal_text': str,
                                                'agree_terms': str,
                                                'tags': OptionalOf(ListOf(str))
                                            }))
        self.parsons = dynamo.Table(storage, "parsons", "id",
                                    types=only_in_dev({
                                        'id': str,
                                        'username': str,
                                        'level': str,
                                        'exercise': str,
                                        'order': ListOf(str),
                                        'correct': str,
                                        'timestamp': int
                                    }),
                                    )
        self.STUDENT_ADVENTURES = dynamo.Table(storage, "student_adventures", "id",
                                               types=only_in_dev({
                                                   'id': str,
                                                   'ticked': bool,
                                                   'program_id': str
                                               }),
                                               )
        self.class_errors = dynamo.Table(storage, "class_errors", "id",
                                         types=only_in_dev({'id': str}),
                                         )

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
        self.quiz_answers = dynamo.Table(storage, "quizAnswers", partition_key="user", sort_key="levelAttempt",
                                         types=only_in_dev({
                                             'user': str,
                                             'levelAttempt': str,
                                         })
                                         )

        # Holds information about program runs: success/failure and produced exceptions.
        # Entries are created per user per level
        # per week and updated in place. Uses a composite partition key 'id#level' and 'week' as a sort key. Structure:
        # {
        #   "id#level": "hedy#1",
        #   "week": '2025-52',
        #   "successful_runs": 10,
        #   "InvalidCommandException": 3,
        #   "InvalidSpaceException": 2
        # }
        #
        self.program_stats = dynamo.Table(
            storage, "program-stats", partition_key="id#level", sort_key="week",
            types=only_in_dev({
                'id#level': str,
                'id': str,
                'week': str,
            }),
            indexes=[dynamo.Index("id", "week")]
        )

        self.quiz_stats = dynamo.Table(
            storage, "quiz-stats", partition_key="id#level", sort_key="week",
            types=only_in_dev({
                'id#level': str,
                'id': str,
                'week': str,
            }),
            indexes=[dynamo.Index("id", "week")]
        )

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

        return self.quiz_answers.update(key, updates)

    def get_quiz_answer(self, username, level, attempt_id):
        """Load a quiz answer from the database."""

        quizAnswers = self.quiz_answers.get({"user": username, "levelAttempt": str(level).zfill(4) + "_" + attempt_id})

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
        programs = self.programs.get_many({"username": username}, reverse=True)
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

    def last_programs_for_user_all_levels(self, username):
        """Return the most recent programs for the given user for all levels.

        Returns: { level -> { adventure_name -> { code, name, ... } } }
        """
        programs = self.programs_for_user(username)
        ret = {i: {} for i in range(1, MAX_LEVEL + 1)}
        for program in programs:
            if 'adventure_name' not in program or 'level' not in program:
                continue
            key = program['adventure_name']
            level = program['level']
            if key not in ret[level] or ret[level][key]['date'] < program['date']:
                ret[level][key] = program
        return ret

    def programs_for_user(self, username):
        """List programs for the given user, newest first.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        return self.programs.get_many({"username": username}, reverse=True)

    def filtered_programs_for_user(self, username, level=None, adventure=None, submitted=None, public=None,
                                   limit=None, pagination_token=None):
        def client_side_filter(program):
            if level and int(program.get('level', 0)) != int(level):
                return False
            if adventure:
                if program.get('adventure_name') != adventure:
                    return False
            if submitted is not None:
                if program.get('submitted') != submitted:
                    return False
            if public is not None and bool(program.get('public')) != public:
                return False
            return True

        # FIXME: Query by index, the current behavior is slow for many programs
        # (See https://github.com/hedyorg/hedy/issues/4121)
        return self.programs.get_page({"username": username},
                                      reverse=True, limit=limit or 50, pagination_token=pagination_token,
                                      client_side_filter=client_side_filter)

    def program_by_id(self, id):
        """Get program by ID.

        Returns: { code, name, program, level, adventure_name, date }
        """
        return self.programs.get({"id": id})

    def store_program(self, program):
        """Store a program.

        Returns the program.

        Add an additional indexable field: 'username_level'.
        """
        self.programs.create(
            dict(program,
                 username_level=f"{program.get('username')}-{program.get('level')}"))

        return program

    def update_program(self, id, updates):
        """Update fields of an existing program.

        Returns the updated state of the program.
        """
        return self.programs.update(dict(id=id), updates)

    def set_program_public_by_id(self, id, public):
        """Switch a program to public or private.

        Return the updated state of the program.
        """
        return self.programs.update({"id": id}, {"public": 1 if public else 0})

    def submit_program_by_id(self, id, submit):
        """Switch a program to submitted.

        Return the updated program state.
        """
        return self.programs.update({"id": id}, {"submitted": submit, "date": timems()})

    def delete_program_by_id(self, id):
        """Delete a program by id."""
        self.programs.delete({"id": id})

    def student_adventure_by_id(self, id):
        # Fetch a student adventure with id formatted as studentID-adventureName-level
        return self.STUDENT_ADVENTURES.get({"id": id})

    def update_student_adventure(self, id, ticked):
        # Swap the ticked value when a request is sent
        return self.STUDENT_ADVENTURES.update({"id": id}, {"ticked": not ticked})

    def store_student_adventure(self, student_adventure):
        # Store the adventure data in this table in case it doesn't match the programs table.
        self.STUDENT_ADVENTURES.create(student_adventure)
        return student_adventure

    def get_class_errors(self, class_id):
        # Fetch a student adventure with id formatted as studentID-adventureName-level
        return self.class_errors.get({"id": class_id})

    def update_class_errors(self, class_errors):
        # Swap the ticked value when a request is sent
        return self.class_errors.put(class_errors)

    def store_class_errors(self, class_errors):
        # create a new class errors object
        self.class_errors.create(class_errors)
        return class_errors

    def add_certificate_to_user(self, username):
        return self.users.update({"username": username}, {"certificate": True})

    def achievements_by_username(self, username):
        return self.achievements.get({"username": username})

    def increase_user_program_count(self, username, delta=1):
        """Increase the program count of a user by the given delta."""
        return self.users.update({"username": username}, {"program_count": dynamo.DynamoIncrement(delta)})

    def user_by_username(self, username):
        """Return a user object from the username."""
        return self.users.get({"username": username.strip().lower()})

    def users_by_username(self, usernames: list[str]):
        """Return a list of user objects from the usernames."""
        return self.users.batch_get([{"username": username.strip().lower()} for username in usernames])

    def user_by_email(self, email):
        """Return a user object from the email address."""
        return self.users.get({"email": email.strip().lower()})

    def get_token(self, token_id):
        """Load a token from the database."""
        return self.tokens.get({"id": token_id})

    def store_token(self, token):
        """Store a token in the database."""
        self.tokens.create(token)

    def forget_token(self, token_id):
        """Forget a Token.

        Returns the Token that was deleted.
        """
        return self.tokens.delete({"id": token_id})

    def delete_all_tokens(self, username):
        """Forget all Tokens from a user."""
        self.tokens.del_many({"username": username})

    def store_user(self, user):
        """Store a user in the database."""
        user["epoch"] = CURRENT_USER_EPOCH
        self.users.create(user)

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
        self.users.update({"username": username}, userdata)

    def forget_user(self, username):
        """Forget the given user."""
        classes = self.users.get({"username": username}).get("classes") or []
        self.users.delete({"username": username})
        # The recover password token may exist, so we delete it
        self.tokens.delete({"id": username})
        self.programs.del_many({"username": username})
        # Remove user from classes of which they are a student
        for class_id in classes:
            self.remove_student_from_class(class_id, username)

        # Remove existing invitations.
        invitations = self.get_user_invitations(username)
        for invite in invitations:
            self.remove_user_class_invite(username, invite["class_id"])

        # Delete classes owned by the user
        for Class in self.get_teacher_classes(username, False):
            self.delete_class(Class)

        # Delete possible adventures owned by the user
        for adv in self.get_teacher_adventures(username):
            self.delete_adventure(adv["id"])

        # Delete possibly created public profile data
        self.forget_public_profile(username)

        # Delete programs stats
        self.program_stats.del_many({"id": username})

        # Delete existing achievements of the user
        self.achievements.delete({"username": username})

    def all_users(self, page_token=None, limit=500):
        """Return a page from the users table.

        There may be more users to retrieve. If so, the returned page object
        will have a 'next_page_token' attribute to continue retrieval.

        Right now, we will only ever query the current epoch, since we are very
        far from 30M users. Once we start to get in that neighbourhood, we should
        update this code.
        """
        return self.users.get_page(
            dict(epoch=CURRENT_USER_EPOCH, created=dynamo.UseThisIndex()),
            pagination_token=page_token,
            limit=limit,
            reverse=True,
        )

    def get_all_public_programs(self):
        programs = self.programs.get_many({"public": 1}, reverse=True)
        return [x for x in programs if not x.get("submitted", False)]

    def add_public_profile_information(self, programs):
        """For each program in a list, note whether the author has a public profile or not.

        For each program, add 'public_user': True or 'public_user': None.

        Modifies the records in the list in-place.
        """
        queries = {p['id']: {'username': p['username'].strip().lower()} for p in programs if 'username' in p}
        profiles = self.public_profiles.batch_get(queries)

        for program in programs:
            program['public_user'] = True if profiles.get(program['id']) else None

    def get_class(self, id):
        """Return the classes with given id."""
        return self.classes.get({"id": id})

    def get_teacher_classes(self, username, students_to_list=False, teacher_only=False):
        """Return all the classes for a teacher.

        This includes classes they own and classes where they are a second teacher.
        """
        classes = None
        # FIXME: This should be a parameter, not be called here!!
        user = auth.current_user()
        if isinstance(self.storage, dynamo.AwsDynamoStorage):
            classes = list(self.classes.get_many({"teacher": username}, reverse=True))

            # if current user is a second teacher, we show the related classes.
            if not teacher_only and auth.is_second_teacher(user):
                classes.extend([self.classes.get({"id": class_id}) for class_id in user["second_teacher_in"]])
        # If we're using the in-memory database, we need to make a shallow copy
        # of the classes before changing the `students` key from a set to list,
        # otherwise the field will remain a list later and that will break the
        # set methods.
        #
        # FIXME: I don't understand what the above comment is saying, but I'm
        # skeptical that it's accurate.
        else:
            classes = []
            for Class in self.classes.get_many({"teacher": username}, reverse=True):
                classes.append(Class.copy())

            # if current user is a second teacher, we show the related classes.
            if not teacher_only and auth.is_second_teacher(user):
                classes.extend([self.classes.get({"id": class_id}).copy() for class_id in user["second_teacher_in"]])
                # classes.extend(CLASSES.query.filter(id__in=user["second_teacher_in"]).all())

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
        classes = self.classes.get_many({"teacher": username}, reverse=True)
        for Class in classes:
            for student in Class.get("students", []):
                if student not in students:
                    students.append(student)
        return students

    def get_student_teachers(self, username):
        """Return a list of the main and all secondary teachers of a student."""
        teachers = []
        for class_id in self.get_student_classes_ids(username):
            class_ = self.get_class(class_id)
            teachers.append(class_["teacher"])
            sec_teachers = [t['username'] for t in class_.get('second_teachers', []) if t.get('role', '') == 'teacher']
            teachers.extend(sec_teachers)
        return teachers

    def get_adventure(self, adventure_id):
        return self.adventures.get({"id": adventure_id})

    def batch_get_adventures(self, adventure_ids):
        """From a list of adventure ids, return a map of { id -> adventure }."""
        keys = {id: {"id": id} for id in adventure_ids}
        return self.adventures.batch_get(keys) if keys else {}

    def get_public_adventures(self):
        return self.adventures.get_many({"public": 1})

    def get_public_adventures_filtered(self,
                                       language: str,
                                       level: int = None,
                                       tag: str = None,
                                       q: str = None,
                                       pagination_token: str = None):
        """Return a page of the public adventures, filtered by language, level and tag, and with a search string.

        Also returns the languages and tags that match the current filter.

        FIXME: This is right now very poorly optimized, and needs more work to be fast.
        """

        server_side_filter = {
            'language': language,
        }

        def client_side_filter(adventure):
            # levels are stored as strings T_T
            if level and adventure.get('level', '') != str(level) and str(level) not in adventure.get('levels', []):
                return False
            if tag and tag not in adventure.get('tags', []):
                return False
            if q:
                fulltext = '|'.join([
                    adventure.get('name', ''),
                    adventure.get('content', ''),
                    adventure.get('author', ''),
                    adventure.get('creator', '')
                ])
                if q.lower() not in fulltext.lower():
                    return False
            return True

        return self.adventures.get_page({"public": 1},
                                        pagination_token=pagination_token,
                                        limit=20,
                                        server_side_filter=server_side_filter,
                                        client_side_filter=client_side_filter)

    def get_public_adventures_tags(self):
        """Return all tags for public adventures.

        FIXME: This is right now very poorly optimized, and needs more work.
        """
        ret = set([])
        for adventure in dynamo.GetManyIterator(self.adventures, {"public": 1}):
            ret |= set(adventure.get("tags", []))
        return ret

    def get_adventure_by_creator_and_name(self, name, username):
        return self.adventures.get({"name": name, "creator": username})

    def delete_adventure(self, adventure_id):
        self.adventures.delete({"id": adventure_id})

    def store_adventure(self, adventure):
        """Store an adventure."""
        return self.adventures.create(adventure)

    def update_adventure(self, adventure_id, adventure):
        self.adventures.update({"id": adventure_id}, adventure)

    def create_tag(self, data):
        return self.tags.create(data)

    def read_tag(self, tag_name):
        return self.tags.get({"name": tag_name})

    def read_tags(self, tags):
        db_tags = []
        for name in tags:
            if (db_tag := self.read_tag(name)) is not None:
                db_tags.append(db_tag)
        return db_tags

    def read_public_tags(self):
        """Public tags are tagged within one or more public adventure or those that aren't in use."""
        all_tags = self.tags.scan()
        public_tags = []
        for tag in all_tags:
            if not tag["tagged_in"] or any([adv["public"] for adv in tag["tagged_in"]]):
                public_tags.append(tag)
        return public_tags

    def read_tags_by_username(self, username):
        tags = self.tags.get_many({"creator": username})
        return tags if tags else {}

    def update_tag(self, tags_id, data):
        # Update existing tags
        return self.tags.update({"id": tags_id}, data)

    def delete_tag(self, tags_id):
        self.tags.delete({"id": tags_id})

    def delete_tag_from_adventure(self, tag_name, adventure_id):
        db_adventure = self.get_adventure(adventure_id)
        adventure_tags = db_adventure.get("tags", [])
        adventure_tags = list(filter(lambda name: name != tag_name, adventure_tags))
        self.update_adventure(adventure_id, {"tags": adventure_tags})

    def get_teacher_adventures(self, username):
        return self.adventures.get_many({"creator": username})

    def get_second_teacher_adventures(self, classes, teacher):
        """Retrieves all adventures of every second teacher in a class.

        Input: the current user and all the classes they are in, as both primary
        and secondary teacher.

        - Retrieves adventures for all teachers that we are in a class with.
        """

        # Find all teachers that we share a class with, and include one name of
        # a class that we share with them.
        shared_teachers = {teacher: clas.get('name')
                           for clas in classes
                           for teacher in ([clas['teacher']] +
                           list(t['username'] for t in
                                clas.get('second_teachers', [])))}

        # We are explicitly not retrieving the current teacher's owned adventures
        if teacher in shared_teachers:
            del shared_teachers[teacher]

        adventures = []
        for teacher, shared_class_name in shared_teachers.items():
            this_teachers_advs = self.get_teacher_adventures(teacher)
            for a in this_teachers_advs:
                a['why'] = 'shared_class'
                a['why_class'] = shared_class_name
            adventures.extend(this_teachers_advs)
        return adventures

    def all_adventures(self):
        return self.adventures.scan()

    def get_student_classes_ids(self, username):
        ids = self.users.get({"username": username}).get("classes")
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
        self.classes.create(Class)

    def update_class(self, id, name):
        """Updates a class."""
        self.classes.update({"id": id}, {"name": name})

    def update_class_data(self, id, class_data):
        """Updates a class."""
        self.classes.update({"id": id}, class_data)

    def update_last_viewed_level_in_class(self, id, level):
        self.classes.update({"id": id}, {"last_viewed_level": level})

    def store_survey(self, survey):
        self.surveys.create(survey)

    def get_survey(self, id):
        return self.surveys.get({"id": id})

    def get_feedback(self):
        """Get allfeedback in the database"""
        return self.feedback.scan()

    def add_survey_responses(self, id, responses):
        self.surveys.update({"id": id}, {"responses":  responses})

    def add_skip_survey(self, id):
        self.surveys.update({"id": id}, {"skip": True})

    def add_remind_later_survey(self, id):
        self.surveys.update({"id": id}, {"skip": date.today().isoformat()})

    def add_student_to_class(self, class_id, student_id):
        """Adds a student to a class."""
        self.classes.update({"id": class_id}, {"students": dynamo.DynamoAddToStringSet(student_id)})
        self.users.update({"username": student_id}, {"classes": dynamo.DynamoAddToStringSet(class_id)})

    def remove_student_from_class(self, class_id, student_id):
        """Removes a student from a class."""
        self.classes.update({"id": class_id}, {"students": dynamo.DynamoRemoveFromStringSet(student_id)})
        self.users.update({"username": student_id}, {"classes": dynamo.DynamoRemoveFromStringSet(class_id)})

    def add_second_teacher_to_class(self, Class, second_teacher):
        """Adds a second teacher to a class."""
        st_classes = second_teacher.get("second_teacher_in", []) + [Class["id"]]
        self.update_user(second_teacher["username"], {"second_teacher_in": st_classes})

        second_teachers = Class.get("second_teachers", []) + \
            [{"username": second_teacher["username"], "role": "teacher"}]
        self.update_class_data(Class["id"], {"second_teachers": second_teachers})

    def remove_second_teacher_from_class(self, Class, second_teacher, only_user=False):
        """Removes a second teacher from a class."""
        # remove this class from the second teacher's table
        st_classes = list(filter(lambda cid: cid != Class["id"], second_teacher.get("second_teacher_in", [])))
        self.update_user(second_teacher["username"], {"second_teacher_in": st_classes})

        if not only_user:
            # remove this second teacher from the class' table
            second_teachers = list(filter(lambda st: st["username"] !=
                                          second_teacher["username"], Class.get("second_teachers", [])))
            self.update_class_data(Class["id"], {"second_teachers": second_teachers})

    def delete_class(self, Class):
        for student_id in Class.get("students", []):
            Database.remove_student_from_class(self, Class["id"], student_id)

        self.customizations.del_many({"id": Class["id"]})
        self.invitations.del_many({"class_id": Class["id"]})
        self.customizations.delete({"id": Class["id"]})
        self.classes.delete({"id": Class["id"]})

    def resolve_class_link(self, link_id):
        return self.classes.get({"link": link_id})

    def get_user_class_invite(self, username, class_id):
        return self.invitations.get({"username#class_id": f"{username}#{class_id}"}) or None

    def add_class_invite(self, username: str, class_id: str, invited_as: str, invited_as_text: str):
        invite_length = config["session"]["invite_length"] * 60
        data = {
            "username": username,
            "class_id": class_id,
            "timestamp": utils.times(),
            "ttl": utils.times() + invite_length,
            "invited_as": invited_as,
            "invited_as_text": invited_as_text,
        }
        data['username#class_id'] = data['username'] + '#' + data['class_id']
        self.invitations.put(data)

    def remove_user_class_invite(self, username, class_id):
        return self.invitations.delete({"username#class_id": f"{username}#{class_id}"})

    def get_user_invitations(self, username):
        return self.invitations.get_many({"username": username}) or []

    def get_class_invitations(self, class_id):
        return self.invitations.get_many({"class_id": class_id}) or []

    def all_classes(self):
        return self.classes.scan()

    def delete_class_customizations(self, class_id):
        self.customizations.delete({"id": class_id})

    def update_class_customizations(self, customizations):
        self.customizations.put(customizations)

    def get_class_customizations(self, class_id):
        customizations = self.customizations.get({"id": class_id})
        return customizations

    def get_student_class_customizations(self, user, class_to_preview=None):
        """Return customizations for the very first class this user is part of.

        If the user is part of multiple classes, they will only get the customizations
        of the first class.

        Class_to_preview is a mode for teachers to preview a custom class that they own.
        """
        student_classes = self.get_student_classes(user)
        if student_classes:
            class_customizations = self.get_class_customizations(student_classes[0]["id"])
            return class_customizations or {}
        elif class_to_preview:
            for Class in self.get_teacher_classes(user):
                if class_to_preview == Class["id"]:
                    class_customizations = self.get_class_customizations(class_to_preview)
                    return class_customizations or {}
        return {}

    def progress_by_username(self, username):
        return self.achievements.get({"username": username})

    def get_all_achievements(self):
        return self.achievements.scan()

    def add_achievement_to_username(self, username, achievement):
        new_user = False
        user_achievements = self.achievements.get({"username": username})
        if not user_achievements:
            new_user = True
            user_achievements = {"username": username}
        if "achieved" not in user_achievements:
            user_achievements["achieved"] = []
        if achievement not in user_achievements["achieved"]:
            user_achievements["achieved"].append(achievement)
            self.achievements.put(user_achievements)
        # Update the amount of achievements on the public profile (if exists)
        self.update_achievements_public_profile(username, len(user_achievements["achieved"]))
        if new_user:
            return True
        return False

    def add_achievements_to_username(self, username, achievements):
        new_user = False
        user_achievements = self.achievements.get({"username": username})
        if not user_achievements:
            new_user = True
            user_achievements = {"username": username}
        if "achieved" not in user_achievements:
            user_achievements["achieved"] = []
        for achievement in achievements:
            if achievement not in user_achievements["achieved"]:
                user_achievements["achieved"].append(achievement)
        user_achievements["achieved"] = list(dict.fromkeys(user_achievements["achieved"]))
        self.achievements.put(user_achievements)

        # Update the amount of achievements on the public profile (if exists)
        self.update_achievements_public_profile(username, len(user_achievements["achieved"]))
        if new_user:
            return True
        return False

    def add_commands_to_username(self, username, commands):
        user_achievements = self.achievements.get({"username": username})
        if not user_achievements:
            user_achievements = {"username": username}
        user_achievements["commands"] = commands
        self.achievements.put(user_achievements)

    def increase_user_run_count(self, username):
        self.achievements.update({"username": username}, {"run_programs": dynamo.DynamoIncrement(1)})

    def increase_user_save_count(self, username):
        self.achievements.update({"username": username}, {"saved_programs": dynamo.DynamoIncrement(1)})

    def increase_user_submit_count(self, username):
        self.achievements.update({"username": username}, {"submitted_programs": dynamo.DynamoIncrement(1)})

    def update_public_profile(self, username, data):
        self.public_profiles.update({"username": username}, data)

    def update_achievements_public_profile(self, username, amount_achievements):
        data = self.public_profiles.get({"username": username})
        # In the case that we make this call but there is no public profile -> don't do anything
        if data:
            self.public_profiles.update(
                {"username": username}, {"achievements": amount_achievements, "last_achievement": timems()}
            )

    def update_country_public_profile(self, username, country):
        data = self.public_profiles.get({"username": username})
        # If there is no data -> we might have made this request from the /update_profile route without a public profile
        # In this case don't do anything
        if data:
            self.public_profiles.update({"username": username}, {"country": country})

    def set_favourite_program(self, username, program_id, set_favourite):
        # We can only set a favourite program is there is already a public profile
        data = self.public_profiles.get({"username": username})
        if data:
            self.update_public_profile(username, {"favourite_program": program_id if set_favourite else ''})
            return True
        return False

    def get_public_profile_settings(self, username):
        return self.public_profiles.get({"username": username})

    def forget_public_profile(self, username):
        self.public_profiles.delete({"username": username})

    def get_all_public_profiles(self):
        return self.public_profiles.scan()

    def store_parsons(self, attempt):
        self.parsons.create(attempt)

    def add_quiz_started(self, id, level):
        key = {"id#level": f"{id}#{level}", "week": self.to_year_week(date.today())}

        add_attributes = {"id": id, "level": level, "started": dynamo.DynamoIncrement()}

        return self.quiz_stats.update(key, add_attributes)

    def add_quiz_finished(self, id, level, score):
        key = {"id#level": f"{id}#{level}", "week": self.to_year_week(date.today())}

        add_attributes = {
            "id": id,
            "level": level,
            "finished": dynamo.DynamoIncrement(),
            "scores": dynamo.DynamoAddToList(score),
        }

        return self.quiz_stats.update(key, add_attributes)

    def get_quiz_stats(self, ids, start=None, end=None):
        start_week = self.to_year_week(self.parse_date(start, date(2022, 1, 1)))
        end_week = self.to_year_week(self.parse_date(end, date.today()))

        data = [self.quiz_stats.get_many({"id": i, "week": dynamo.Between(start_week, end_week)}) for i in ids]
        return functools.reduce(operator.iconcat, data, [])

    def add_program_stats(self, id, level, number_of_lines, exception, error_message=None):
        key = {"id#level": f"{id}#{level}", "week": self.to_year_week(date.today())}
        add_attributes = {"id": id, "level": level, "number_of_lines": number_of_lines}
        program_stats = self.program_stats.get_many({"id": id, "week": self.to_year_week(date.today())})

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

        return self.program_stats.update(key, add_attributes)

    def get_program_stats_per_level(self, id, level, start=None, end=None):
        start_week = self.to_year_week(self.parse_date(start, date(2022, 1, 1)))
        end_week = self.to_year_week(self.parse_date(end, date.today()))
        data = self.program_stats.get_many(
            {'id#level': id + '#' + str(level), "week": dynamo.Between(start_week, end_week)})
        return data

    def get_program_stats(self, ids, start=None, end=None):
        start_week = self.to_year_week(self.parse_date(start, date(2022, 1, 1)))
        end_week = self.to_year_week(self.parse_date(end, date.today()))

        data = [self.program_stats.get_many({"id": i, "week": dynamo.Between(start_week, end_week)}) for i in ids]
        return functools.reduce(operator.iconcat, data, [])

    def parse_date(self, d, default):
        return date(*map(int, d.split("-"))) if d else default

    def to_year_week(self, d):
        cal = d.isocalendar()
        return f"{cal[0]}-{cal[1]:02d}"

    def get_username_role(self, username):
        role = "teacher" if self.users.get({"username": username}).get("is_teacher") == 1 else "student"
        return role

    def get_student_that_starts_with(self, search):
        """
        Gets students that aren't already in a class
        """
        return self.users.get_many(
            {"epoch": CURRENT_USER_EPOCH, "username": dynamo.BeginsWith(search)},
            server_side_filter={"classes": dynamo.SetEmpty()},
            limit=10,
        )

    def get_teacher_that_starts_with(self, search, not_in_class_id=None):
        """
        Gets teachers from DB that aren't second teacher's already of this class
        """
        server_side_filter = {'is_teacher': 1}
        if not_in_class_id:
            server_side_filter['second_teacher_in'] = dynamo.NotContains(not_in_class_id)
        records = self.users.get_many(
            {"epoch": CURRENT_USER_EPOCH, "username": dynamo.BeginsWith(search)},
            server_side_filter=server_side_filter,
            limit=10
        )
        return records

    def get_class_invites(self, class_id: str):
        invites = []
        for invite in self.get_class_invitations(class_id):
            invites.append(
                {
                    "username": invite["username"],
                    "invited_as_text": invite["invited_as_text"],
                    "invited_as": invite["invited_as"],
                    "timestamp": utils.localized_date_format(invite["timestamp"], short_format=True),
                    "expire_timestamp": utils.localized_date_format(invite["ttl"], short_format=True),
                }
            )
        return invites


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch
