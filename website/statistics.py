from collections import namedtuple
from enum import Enum
from difflib import SequenceMatcher
import re
from flask import g, jsonify, make_response, request
from flask_babel import gettext
import utils
import hedy_content
import exceptions as hedy_exceptions
from hedy import check_program_size_is_valid, parse_input, is_program_valid, process_input_string, HEDY_MAX_LEVEL
import hedy
from hedy_error import get_error_text
import jinja_partials
from website.flask_helpers import render_template
from website import querylog
from website.auth import is_admin, is_teacher, requires_admin, requires_login
from timeit import default_timer as timer
from .database import Database
from .website_module import WebsiteModule, route
from bs4 import BeautifulSoup

import logging
from logging_config import LOGGING_CONFIG
from logging.config import dictConfig as logConfig

logConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

"""The Key tuple is used to aggregate the raw data by level, time or username."""
Key = namedtuple("Key", ["name", "class_"])
level_key = Key("level", int)
username_key = Key("id", str)
week_key = Key("week", str)


class UserType(Enum):
    ALL = "@all"  # Old value used before user types
    ANONYMOUS = "@all-anonymous"
    LOGGED = "@all-logged"
    STUDENT = "@all-students"


class StatisticsModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("stats", __name__)
        self.db = db

    @route("/grid_overview/class/<class_id>", methods=["GET"])
    @requires_login
    def render_class_grid_overview(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))

        students, class_, class_adventures_formatted, ticked_adventures, \
            adventure_names, student_adventures = self.get_grid_info(
                user, class_id, 1)
        matrix_values = self.get_matrix_values(students, class_adventures_formatted, ticked_adventures, '1')
        adventure_names = {value: key for key, value in adventure_names.items()}

        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        return render_template(
            "class-grid.html",
            class_info={"id": class_id, "students": students, "name": class_["name"]},
            current_page="grid_overview",
            max_level=hedy.HEDY_MAX_LEVEL,
            class_adventures=class_adventures_formatted,
            ticked_adventures=ticked_adventures,
            matrix_values=matrix_values,
            adventure_names=adventure_names,
            student_adventures=student_adventures,
            page_title=gettext("title_class grid_overview"),
        )

    @route("/grid_overview/class/<class_id>/level", methods=["GET"])
    @requires_login
    def change_dropdown_level(self, user, class_id):
        level = request.args.get('level')
        students, class_, class_adventures_formatted, ticked_adventures, \
            adventure_names, student_adventures = self.get_grid_info(
                user, class_id, level)
        matrix_values = self.get_matrix_values(students, class_adventures_formatted, ticked_adventures, level)
        adventure_names = {value: key for key, value in adventure_names.items()}

        return jinja_partials.render_partial("customize-grid/partial-grid-levels.html",
                                             level=level,
                                             class_info={"id": class_id, "students": students, "name": class_["name"]},
                                             current_page="grid_overview",
                                             max_level=hedy.HEDY_MAX_LEVEL,
                                             class_adventures=class_adventures_formatted,
                                             ticked_adventures=ticked_adventures,
                                             matrix_values=matrix_values,
                                             adventure_names=adventure_names,
                                             student_adventures=student_adventures,
                                             page_title=gettext("title_class grid_overview"),
                                             )

    @route("/grid_overview/class/<class_id>/level", methods=["POST"])
    @requires_login
    def change_checkbox(self, user, class_id):
        level = request.args.get('level')
        student_index = request.args.get('student_index', type=int)
        adventure_index = request.args.get('adventure_index', type=int)
        students, class_, class_adventures_formatted, ticked_adventures, adventure_names, _ = self.get_grid_info(
            user, class_id, level)
        matrix_values = self.get_matrix_values(students, class_adventures_formatted, ticked_adventures, level)

        adventure_names = {value: key for key, value in adventure_names.items()}
        current_adventure_name = class_adventures_formatted[level][adventure_index]
        student_adventure_id = f"{students[student_index]}-{adventure_names[current_adventure_name]}-{level}"

        self.db.update_student_adventure(student_adventure_id, matrix_values[student_index][adventure_index])
        _, _, _, ticked_adventures, _, student_adventures = self.get_grid_info(user, class_id, level)
        matrix_values[student_index][adventure_index] = not matrix_values[student_index][adventure_index]

        return jinja_partials.render_partial("customize-grid/partial-grid-levels.html",
                                             level=level,
                                             class_info={"id": class_id, "students": students, "name": class_["name"]},
                                             current_page="grid_overview",
                                             max_level=hedy.HEDY_MAX_LEVEL,
                                             class_adventures=class_adventures_formatted,
                                             ticked_adventures=ticked_adventures,
                                             adventure_names=adventure_names,
                                             student_adventures=student_adventures,
                                             matrix_values=matrix_values,
                                             page_title=gettext("title_class grid_overview"),
                                             )

    def get_matrix_values(self, students, class_adventures_formatted, ticked_adventures, level):
        rendered_adventures = class_adventures_formatted.get(level)
        matrix = [[None for _ in range(len(class_adventures_formatted[level]))] for _ in range(len(students))]
        for student_index in range(len(students)):
            student_list = ticked_adventures.get(students[student_index])
            if student_list and rendered_adventures:
                for program in student_list:
                    if program['level'] == level:
                        index = rendered_adventures.index(program['name'])
                        matrix[student_index][index] = 1 if program['ticked'] else 0
        return matrix

    @route("/program-stats", methods=["GET"])
    @requires_admin
    def get_program_stats(self, user):
        start_date = request.args.get("start", default=None, type=str)
        end_date = request.args.get("end", default=None, type=str)

        ids = [e.value for e in UserType]
        program_runs_data = self.db.get_program_stats(ids, start_date, end_date)
        quiz_data = self.db.get_quiz_stats(ids, start_date, end_date)
        data = program_runs_data + quiz_data

        per_level_data = _aggregate_for_keys(data, [level_key])
        per_week_data = _aggregate_for_keys(data, [week_key, level_key])

        response = {
            "per_level": _to_response_per_level(per_level_data),
            "per_week": _to_response(per_week_data, "week", lambda e: f"L{e['level']}"),
        }
        return jsonify(response)

    def get_grid_info(self, user, class_id, level):
        class_ = self.db.get_class(class_id)
        if hedy_content.Adventures(g.lang).has_adventures():
            adventures = hedy_content.Adventures(g.lang).get_adventure_keyname_name_levels()
            full_adventures = hedy_content.Adventures(g.lang).get_adventures(g.keyword_lang)
        else:
            full_adventures = hedy_content.Adventures("en").get_adventures(g.keyword_lang)
            adventures = hedy_content.Adventures("en").get_adventure_keyname_name_levels()
        students = sorted(class_.get("students", []))
        teacher_adventures = self.db.get_teacher_adventures(user["username"])

        class_info = get_customizations(self.db, class_id)
        class_adventures = class_info.get('sorted_adventures')

        adventure_names = {}
        for adv_key, adv_dic in adventures.items():
            for name, _ in adv_dic.items():
                adventure_names[adv_key] = hedy_content.get_localized_name(name, g.keyword_lang)

        for adventure in teacher_adventures:
            adventure_names[adventure['id']] = adventure['name']

        class_adventures_formatted = {}
        for key, value in class_adventures.items():
            adventure_list = []
            for adventure in value:
                # if the adventure is not in adventure names it means that the data in the customizations is bad
                if not adventure['name'] == 'next' and adventure['name'] in adventure_names:
                    adventure_list.append(adventure_names[adventure['name']])
            class_adventures_formatted[key] = adventure_list

        ticked_adventures = {}
        student_adventures = {}
        for student in students:
            programs = self.db.last_level_programs_for_user(student, level)
            if programs:
                ticked_adventures[student] = []
                for _, program in programs.items():
                    # Old programs sometimes don't have adventures associated to them
                    # So skip them
                    if 'adventure_name' not in program:
                        continue
                    name = adventure_names.get(program['adventure_name'], program['adventure_name'])
                    customized_level = class_adventures_formatted.get(str(program['level']))
                    if name in customized_level\
                            and self.is_program_modified(program, full_adventures, teacher_adventures):
                        student_adventure_id = f"{student}-{program['adventure_name']}-{level}"
                        current_adventure = self.db.student_adventure_by_id(student_adventure_id)
                        if not current_adventure:
                            # store the adventure in case it's not in the table
                            current_adventure = self.db.store_student_adventure(
                                dict(id=f"{student_adventure_id}", ticked=False, program_id=program['id']))

                        current_program = dict(id=program['id'], level=str(program['level']),
                                               name=name, ticked=current_adventure['ticked'])

                        student_adventures[student_adventure_id] = program['id']
                        ticked_adventures[student].append(current_program)

        return students, class_, class_adventures_formatted, ticked_adventures, adventure_names, student_adventures

    def is_program_modified(self, program, full_adventures, teacher_adventures):
        # a single adventure migh have several code snippets, formatted using markdown
        # we need to get them individually
        adventure_info = full_adventures.get(program['adventure_name'], {})\
            .get('levels', {})\
            .get(program['level'], {})

        example_codes = []
        # for what I can see the examples codes start with no index, and then jump to two
        # e.g: example_code, example_code_2, etc.
        example_codes.append(adventure_info.get('example_code', ''))
        i = 2
        while adventure_info.get(f'example_code_{i}') is not None:
            example_codes.append(adventure_info[f'example_code_{i}'])
            i += 1
        # Examples codes sometimes are not single code sections
        # but actually can be several code sections mixed with text
        # formatted using markdown.
        adventure_snippets = []
        for code in example_codes:
            consecutive_backticks = 0
            inside_code = False
            previous_char = ''
            code_start = -1
            for index, char in enumerate(code):
                if char == '`':
                    consecutive_backticks += 1
                    if consecutive_backticks == 3:
                        # We've already finished the code section, which means
                        # we can add it to the example_codes array
                        if inside_code:
                            adventure_snippets.append(code[code_start:index-3])
                            inside_code = False
                        # We are starting a code section, therefore we need to save this index
                        else:
                            code_start = index + 1
                            inside_code = True
                # if we find a char before 3 consecutive backticks it's either inline code
                # or a malformed code section
                elif char != '`' and previous_char == '`':
                    consecutive_backticks = 0
                previous_char = char
        # now we have to get the snippets of the teacher adventures
        for adventure in teacher_adventures:
            if program['adventure_name'] == adventure["id"]:
                content = adventure['content']
                soup = BeautifulSoup(content, features="html.parser")
                for pre in soup.find_all('pre'):
                    adventure_snippets.append(str(pre.contents[0]))

        student_code = program['code'].strip()
        # now we have to calculate the differences between the student code and the code snippets
        can_save = True
        for snippet in adventure_snippets:
            if re.search(r'<code.*?>.*?</code>', snippet):
                snippet = re.sub(r'<code.*?>(.*?)</code>', r'\1', snippet)
            snippet = snippet.strip()
            seq_match = SequenceMatcher(None, snippet, student_code)
            matching_ratio = round(seq_match.ratio(), 2)
            # Allowing a difference of more than 10% or the student filled the placeholders
            if matching_ratio >= 0.95 and (self.has_placeholder(student_code) or not self.has_placeholder(snippet)):
                can_save = False
        return can_save

    def has_placeholder(self, code):
        return re.search(r'(?<![^ \n])(_)(?= |$)', code, re.M) is not None


class LiveStatisticsModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("live-stats", __name__)
        self.db = db
        """
        Every exception must be listed here, and assigned a type. Currently we have the following
        types of Exceptions:
        * Programs too large: when the programs surpass our limit
        * Use of blanks in programs: when the kids uses blanks in the programs (_)
        * Use of nested functions: nested functions are not allowed in Hedy
        * Incorrect use of types: this encompass errors that involve using the wrong type for a
          built-in function or a matemathical operation
        * Invalid command: We list here parse exception when the command used is wrong and we dont know it
        * Incomplete command: when the command have several parts, and the user forgot one.
        * Command not correct anymore: When a command changes sintax or is removed
        * Command not available yet: for commands that will be available in the following levels, but not yet
        * Incorect use of variable: When a variable is used before being assigned or is undefined.
        * Incorrect Indentation: the user put a space where it didnt belong or the indentation doesnt match
        * Echo and ask mismatch: when an echo is used without an ask
        * Incorrect handling of quotes: any scenario where text is not handled correctly
        """
        self.exception_types = {
            'InputTooBigException': 'program_too_large_exception',
            'CodePlaceholdersPresentException': 'use_of_blanks_exception',
            'NestedFunctionException': 'use_of_nested_functions_exception',
            'InvalidTypeCombinationException': 'incorrect_use_of_types_exception',
            'InvalidArgumentTypeException': 'incorrect_use_of_types_exception',
            'InvalidArgumentException': 'incorrect_use_of_types_exception',
            'InvalidCommandException': 'invalid_command_exception',
            'MissingCommandException': 'invalid_command_exception',
            'IncompleteCommandException': 'incomplete_command_exception',
            'MissingElseForPressitException': 'incomplete_command_exception',
            'MissingInnerCommandException': 'incomplete_command_exception',
            'IncompleteRepeatException': 'incomplete_command_exception',
            'WrongLevelException': 'command_unavailable_exception',
            'InvalidAtCommandException': 'command_unavailable_exception',
            'LockedLanguageFeatureException': 'command_not_available_yet_exception',
            'UnsupportedFloatException': 'command_not_available_yet_exception',
            'AccessBeforeAssignException': 'incorrect_use_of_variable_exception',
            'UndefinedVarException': 'incorrect_use_of_variable_exception',
            'CyclicVariableDefinitionException': 'incorrect_use_of_variable_exception',
            'IndentationException': 'indentation_exception',
            'InvalidSpaceException': 'indentation_exception',
            'NoIndentationException': 'indentation_exception',
            'LonelyEchoException': 'echo_and_ask_mismatch_exception',
            'UnsupportedStringValue': 'incorrect_handling_of_quotes_exception',
            'UnquotedAssignTextException': 'incorrect_handling_of_quotes_exception',
            'UnquotedEqualityCheckException': 'incorrect_handling_of_quotes_exception',
            'LonelyTextException': 'incorrect_handling_of_quotes_exception',
            'UnquotedTextException': 'incorrect_handling_of_quotes_exception',
            'ParseException': 'cant_parse_exception'
        }
        self.MAX_CONTINUOUS_ERRORS = 3
        self.MAX_COMMON_ERRORS = 10
        self.MAX_FEED_SIZE = 4

    def __selected_levels(self, class_id):
        start = timer()
        class_customization = get_customizations(self.db, class_id)
        class_overview = class_customization.get('dashboard_customization')
        end = timer()
        logger.debug(f'Time taken by __selected_levels {end-start}')
        if class_overview:
            return class_overview.get('selected_levels', [1])
        return [1]

    def __common_errors(self, class_id):
        common_errors = self.db.get_class_errors(class_id)
        if not common_errors:
            return self.db.store_class_errors(dict(id=class_id, errors=[]))
        return common_errors

    def __all_students(self, class_):
        """Returns a list of all students in a class along with some info."""
        start = timer()
        students = []
        for student_username in class_.get("students", []):
            programs = self.db.programs_for_user(student_username)
            quiz_scores = self.db.get_quiz_stats([student_username])
            # Verify if the user did finish any quiz before getting the max() of the finished levels
            finished_quizzes = any("finished" in x for x in quiz_scores)
            highest_quiz = max([x.get("level") for x in quiz_scores if x.get("finished")]) if finished_quizzes else "-"
            students.append(
                {
                    "username": student_username,
                    "programs": len(programs),
                    "highest_level": highest_quiz,
                    "current_adventure": programs[0] if programs else "-",
                    "current_level": programs[0]['level'] if programs else '0'
                }
            )
        end = timer()
        logger.debug(f'Time taken by __all_students {end-start}')
        return students

    def __get_adventures_for_overview(self, user, class_id):
        class_ = self.db.get_class(class_id)
        # Data for student overview card
        if hedy_content.Adventures(g.lang).has_adventures():
            adventures = hedy_content.Adventures(g.lang).get_adventure_keyname_name_levels()
        else:
            adventures = hedy_content.Adventures("en").get_adventure_keyname_name_levels()

        # For authorization purposes only admins can do this lookup by the class teacher,
        # more or less impersonating the teacher. We can consider doing the lookup by the
        # teacher field in any case if we don't care about security in this private method.
        if is_admin(user):
            teacher_name = class_["teacher"]
        else:
            teacher_name = user["username"]
        teacher_adventures = self.db.get_teacher_adventures(teacher_name)
        customizations = get_customizations(self.db, class_id)
        # Array where (index-1) is the level, and the values are lists of the current adventures of the students
        last_adventures = []
        found_students = []
        # loop in reverse to ignore early levels
        for level in reversed(range(1, HEDY_MAX_LEVEL + 1)):
            _data = []
            for _student in class_.get("students", []):
                last_adventure = list(self.db.last_level_programs_for_user(_student, level).keys())
                if last_adventure and _student not in found_students:
                    _data.append({_student: last_adventure[0]})
                    found_students.append(_student)
            last_adventures.append(_data)
        # reverse back to normal level order
        last_adventures.reverse()

        return _get_available_adventures(adventures, teacher_adventures, customizations, last_adventures)

    @route("/live_stats/class/<class_id>", methods=["GET"])
    @requires_login
    def render_live_stats(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        student = _check_student_arg()
        dashboard_options_args = _build_url_args(student=student)

        students, common_errors, selected_levels, quiz_info, attempted_adventures, \
            adventures = self.get_class_live_stats(user, class_)

        return render_template(
            "class-live-stats.html",
            class_info={
                "id": class_id,
                "students": students,
                "common_errors": common_errors['errors']
            },
            class_overview={
                "selected_levels": selected_levels,
                "quiz_info": quiz_info
            },
            dashboard_options={
                "student": student
            },
            attempted_adventures=attempted_adventures,
            dashboard_options_args=dashboard_options_args,
            adventures=adventures,
            max_level=HEDY_MAX_LEVEL,
            current_page="my-profile",
            page_title=gettext("title_class live_statistics")
        )

    def get_class_live_stats(self, user, class_):
        start = timer()
        # Retrieve common errors and selected levels in class overview from the database for class
        selected_levels = self.__selected_levels(class_['id'])
        if selected_levels:
            selected_levels = [int(level) for level in selected_levels]
            selected_levels.sort()

        # identifies common errors in the class
        common_errors = self.common_exception_detection(class_['id'], user)

        students = self.__all_students(class_)
        adventures = self.__get_adventures_for_overview(user, class_['id'])

        quiz_stats = []
        for student_username in class_.get("students", []):
            quiz_stats_student = self.db.get_quiz_stats([student_username])
            quiz_in_progress = [x.get("level") for x in quiz_stats_student
                                if x.get("started") and not x.get("finished")]
            quiz_finished = [x.get("level") for x in quiz_stats_student if x.get("finished")]
            quiz_stats.append(
                {
                    "student": student_username,
                    "in_progress": quiz_in_progress,
                    "finished": quiz_finished
                }
            )
        quiz_info = _get_quiz_info(quiz_stats)

        attempted_adventures = {}
        for level in range(1, HEDY_MAX_LEVEL+1):
            programs_for_student = {}
            for _student in class_.get("students", []):
                adventures_for_student = [x['adventure_name'] for x in self.db.level_programs_for_user(_student, level)]
                if adventures_for_student:
                    programs_for_student[_student] = adventures_for_student
            if programs_for_student != []:
                attempted_adventures[level] = programs_for_student
        end = timer()
        logger.debug(f'Time taken by get_class_live_stats {end-start}')
        return students, common_errors, selected_levels, quiz_info, attempted_adventures, adventures

    @route("/live_stats/class/<class_id>/select_level", methods=["GET"])
    @requires_login
    def choose_level(self, user, class_id):
        """
        Adds or remove the current level from the UI
        """
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        selected_levels = self.__selected_levels(class_id)
        chosen_level = request.args.get("level")

        if int(chosen_level) in selected_levels:
            selected_levels.remove(int(chosen_level))
        else:
            selected_levels.append(int(chosen_level))

        customization = get_customizations(self.db, class_id)
        dashboard_customization = customization.get('dashboard_customization', {})
        dashboard_customization['selected_levels'] = selected_levels
        customization['dashboard_customization'] = dashboard_customization
        self.db.update_class_customizations(customization)

        students, common_errors, selected_levels, quiz_info, attempted_adventures, \
            adventures = self.get_class_live_stats(user, class_)

        student = _check_student_arg()
        dashboard_options_args = _build_url_args(student=student)

        return jinja_partials.render_partial(
            "partial-class-live-stats.html",
            class_info={
                "id": class_id,
                "students": students,
                "common_errors": common_errors['errors']
            },
            class_overview={
                "selected_levels": selected_levels,
                "quiz_info": quiz_info
            },
            dashboard_options={
                "student": student
            },
            attempted_adventures=attempted_adventures,
            dashboard_options_args=dashboard_options_args,
            adventures=adventures,
            max_level=HEDY_MAX_LEVEL,
            current_page="my-profile",
            page_title=gettext("title_class live_statistics")
        )

    @route("/live_stats/class/<class_id>/refresh", methods=["GET"])
    @requires_login
    def refresh_live_stats(self, user, class_id):
        """
        Partialy refresh the live statistics page, be it hiding and showing the differents parts of the page
        or refreshing the entirety of it
        """

        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        student = _check_student_arg()
        dashboard_options_args = _build_url_args(student=student)

        students, common_errors, selected_levels, quiz_info, attempted_adventures, \
            adventures = self.get_class_live_stats(user, class_)

        keyword_lang = g.keyword_lang
        # Give the template more data in case there's a student selected
        if student:
            class_students = class_.get("students", [])
            if student not in class_students:
                return utils.error_page(error=404, ui_message=gettext('not_enrolled'))

            student_programs, graph_data, graph_labels, selected_student = self.get_student_data(student, class_)

            return jinja_partials.render_partial(
                "partial-class-live-stats.html",
                dashboard_options={
                    "student": student
                },
                class_info={
                    "id": class_id,
                    "students": students,
                    "common_errors": common_errors['errors']
                },
                class_overview={
                    "selected_levels": selected_levels,
                    "quiz_info": quiz_info
                },
                attempted_adventures=attempted_adventures,
                dashboard_options_args=dashboard_options_args,
                adventures=adventures,
                max_level=HEDY_MAX_LEVEL,
                adventure_names=hedy_content.Adventures(g.lang).get_adventure_names(keyword_lang),
                student=selected_student,
                student_programs=student_programs,
                data=graph_data,
                labels=graph_labels,
                current_page='my-profile',
                page_title=gettext("title_class live_statistics")
            )
        else:
            return jinja_partials.render_partial(
                "partial-class-live-stats.html",
                class_info={
                    "id": class_id,
                    "students": students,
                    "common_errors": common_errors['errors']
                },
                class_overview={
                    "selected_levels": selected_levels,
                    "quiz_info": quiz_info
                },
                dashboard_options={
                    "student": student
                },
                attempted_adventures=attempted_adventures,
                dashboard_options_args=dashboard_options_args,
                adventures=adventures,
                max_level=HEDY_MAX_LEVEL,
                current_page="my-profile",
                page_title=gettext("title_class live_statistics")
            )

    @route("/live_stats/class/<class_id>/student", methods=["GET"])
    @requires_login
    def render_student_details____(self, user, class_id):
        """
        Shows information about an individual student when they
        are selected in the student list.
        """

        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        student = _check_student_arg()
        dashboard_options_args = _build_url_args(student=student)

        students = class_.get("students", [])
        if student not in students:
            return utils.error_page(error=404, ui_message=gettext('not_enrolled'))

        students, common_errors, selected_levels, quiz_info, attempted_adventures, \
            adventures = self.get_class_live_stats(user, class_)

        student_programs, graph_data, graph_labels, selected_student = self.get_student_data(student, class_)

        keyword_lang = g.keyword_lang

        return jinja_partials.render_partial(
            "partial-class-live-stats.html",
            dashboard_options={
                "student": student
            },
            class_info={
                "id": class_id,
                "students": students,
                "common_errors": common_errors['errors']
            },
            class_overview={
                "selected_levels": selected_levels,
                "quiz_info": quiz_info
            },
            attempted_adventures=attempted_adventures,
            dashboard_options_args=dashboard_options_args,
            adventures=adventures,
            max_level=HEDY_MAX_LEVEL,
            adventure_names=hedy_content.Adventures(g.lang).get_adventure_names(keyword_lang),
            student=selected_student,
            student_programs=student_programs,
            data=graph_data,
            labels=graph_labels,
            current_page='my-profile',
            page_title=gettext("title_class live_statistics")
        )

    def get_student_data(self, student, class_):
        """
        Returns the data for a specific student
        """
        # Get data for selected student
        programs = self.db.programs_for_user(student)
        quiz_scores = self.db.get_quiz_stats([student])
        finished_quizzes = any("finished" in x for x in quiz_scores)
        highest_quiz = max([x.get("level") for x in quiz_scores if x.get("finished")]) if finished_quizzes else "-"
        selected_student = {"username": student, "programs": len(programs), "highest_level": highest_quiz}

        # Load in all program data for that specific student
        student_programs = []
        for item in programs:
            date = utils.delta_timestamp(item['date'])
            # This way we only keep the first 10 lines to show as preview to the user
            code = "\n".join(item['code'].split("\n")[:20])
            error_class = _get_error_info(item['code'], item['level'], item['lang'])
            student_programs.append(
                {'id': item['id'],
                 'code': code,
                 'date': date,
                 'lang': item['lang'],
                 'level': item['level'],
                 'name': item['name'],
                 'adventure_name': item.get('adventure_name'),
                 'submitted': item.get('submitted'),
                 'public': item.get('public'),
                 'number_lines': item['code'].count('\n') + 1,
                 'error_message': get_error_text(error_class, item['lang']) if error_class else None,
                 'error_header': 'Oops'  # TODO: get proper header message that gets translated, e.g. Transpile_error
                 }
            )

        # get data for graph from db, db conveniently stores amount of errors for student
        graph_data = self.db.get_program_stats([selected_student['username']], None, None)
        graph_data, graph_labels = _collect_graph_data(graph_data, window_size=10)

        attempted_adventures = {}
        for level in range(1, HEDY_MAX_LEVEL+1):
            programs_for_student = {}
            for _student in class_.get("students", []):
                adventures_for_student = [x['adventure_name'] for x in self.db.level_programs_for_user(_student, level)]
                if adventures_for_student != []:
                    programs_for_student[_student] = adventures_for_student
            if programs_for_student != []:
                attempted_adventures[level] = programs_for_student

        return student_programs, graph_data, graph_labels, selected_student

    @route("/live_stats/class/<class_id>/pop_up", methods=["GET"])
    @requires_login
    def render_common_error_items(self, user, class_id):
        """
        Handles the rendering of the common error items in the common errors detection list.
        """
        student = _check_student_arg()
        dashboard_options_args = _build_url_args(student=student)

        selected_levels = self.__selected_levels(class_id)
        common_errors = self.common_exception_detection(class_id, user)

        # get id of the common error to know which data to display from database
        error_id = request.args.get("error-id", default="", type=str)
        selected_item = None
        if error_id:
            selected_item = common_errors['errors'][int(error_id)]

        class_ = self.db.get_class(class_id)
        students = self.__all_students(class_)

        adventures = self.__get_adventures_for_overview(user, class_id)

        quiz_stats = []
        for student_username in class_.get("students", []):
            quiz_stats_student = self.db.get_quiz_stats([student_username])
            quiz_in_progress = [x.get("level") for x in quiz_stats_student
                                if x.get("started") and not x.get("finished")]
            quiz_finished = [x.get("level") for x in quiz_stats_student if x.get("finished")]
            quiz_stats.append(
                {
                    "student": student_username,
                    "in_progress": quiz_in_progress,
                    "finished": quiz_finished
                }
            )
        quiz_info = _get_quiz_info(quiz_stats)

        attempted_adventures = {}
        for level in range(1, HEDY_MAX_LEVEL+1):
            programs_for_student = {}
            for _student in class_.get("students", []):
                adventures_for_student = [x['adventure_name'] for x in self.db.level_programs_for_user(_student, level)]
                if adventures_for_student != []:
                    programs_for_student[_student] = adventures_for_student
            if programs_for_student != []:
                attempted_adventures[level] = programs_for_student

        return render_template(
            "htmx-class-live-popup.html",
            class_info={
                "id": class_id,
                "students": students,
                "common_errors": common_errors['errors']
            },
            class_overview={
                "selected_levels": selected_levels,
                "quiz_info": quiz_info
            },
            dashboard_options={
                "student": student
            },
            dashboard_options_args=dashboard_options_args,
            adventures=adventures,
            attempted_adventures=attempted_adventures,
            max_level=HEDY_MAX_LEVEL,
            selected_item=selected_item,
            current_page='my-profile'
        )

    @route("/live_stats/class/<class_id>/error/<error_id>", methods=["DELETE"])
    @requires_login
    def remove_common_error_item(self, user, class_id, error_id):
        """
        Removes the common error item by setting the active flag to 0.
        """
        common_errors = self.__common_errors(class_id)
        for i in range(len(common_errors['errors'])):
            if common_errors['errors'][i]['id'] == int(error_id) and common_errors['errors'][i]['active'] == 1:
                common_errors['errors'][i]['active'] = 0
                self.db.update_class_errors(common_errors)
                break

        return make_response('', 204)

    def retrieve_exceptions_per_student(self, class_id):
        """
        Retrieves exceptions per student in the class
        :param class_id: class id
        :return: exceptions_per_user
        """
        start = timer()
        class_ = self.db.get_class(class_id)
        exceptions_per_user = {}
        students = sorted(class_.get("students", []))
        for student_username in students:
            program_stats = self.db.get_program_stats([student_username], None, None)
            if program_stats:
                # if there are multiple weeks, only get the most recent week's data
                program_stats = program_stats[-1]
                exceptions = {k: v for k, v in program_stats.items() if k.lower().endswith("exception")}
                exceptions_per_user[student_username] = exceptions
        end = timer()
        logger.debug(f'Tike taken by retrieve_exceptions_per_student {end-start}')
        return exceptions_per_user

    def new_id_calc(self, common_errors, class_id):
        """
        Calculates the new id for a new common error entry.
        :param common_errors: common errors from db
        :param class_id: class id
        :return: new id
        """
        common_error_ids = [int(x['id']) for x in common_errors['errors']]
        new_id = max(common_error_ids) + 1 if common_error_ids else 0

        # reached max common errors
        if new_id > 0 and new_id % self.MAX_COMMON_ERRORS == 0:
            # find all disables entries
            disables = [x['id'] for x in common_errors['errors'] if x['active'] == 0]
            if disables:
                # assign oldest not used id to new error
                new_id = disables[0]
            else:
                # forcefully overwrite oldest error despite not being resolved and set oldest half of the db to
                # inactive to free up space
                # Todo: could use a better way to handle this
                new_id = 0

                for i in range(self.MAX_COMMON_ERRORS // 2):
                    common_errors['errors'][i]['active'] = 0
                self.db.update_class_errors(common_errors)

        return new_id

    def common_exception_detection(self, class_id, user):
        """
        Detects misconceptions of students in the class based on errors they are making.
        """
        start = timer()
        common_errors = self.__common_errors(class_id)
        # Group the error messages by session and count their occurrences
        exceptions_per_user = self.retrieve_exceptions_per_student(class_id)  # retrieves relevant data from db
        labels = [x['label'] for x in common_errors['errors']]
        exception_type_counts = {}

        # Iterate over each error and its corresponding username in the current session group
        for username, exception_count in exceptions_per_user.items():
            for exception_name, count in exception_count.items():
                exception_type = self.exception_types[exception_name]

                if count >= self.MAX_CONTINUOUS_ERRORS:
                    # Check if the current exception type is in the dictionary
                    if exception_name not in exception_type_counts:
                        exception_type_counts[exception_type] = {}
                    # Check if the current exception is not in the exception_type_counts
                    # dictionary for the current exception_type
                    if exception_name not in exception_type_counts[exception_type]:
                        exception_type_counts[exception_type][exception_name] = {'freq': 0, 'users': []}
                    exception_type_counts[exception_type][exception_name]['freq'] += 1
                    exception_type_counts[exception_type][exception_name]['users'].append(username)

        for exception_type, exception_name in sorted(exception_type_counts.items(),
                                                     key=lambda x: sum(x[1][exception_name]['freq']
                                                                       for exception_name in x[1]),
                                                     reverse=True)[:self.MAX_FEED_SIZE]:
            sorted_exceptions = sorted(exception_name.items(), key=lambda x: x[1]['freq'], reverse=True)
            all_users = []

            for _, info in sorted_exceptions:
                users_counts = [(user, info['users'].count(user)) for user in set(info['users'])]
                sorted_users = sorted(users_counts, key=lambda x: x[1], reverse=True)
                users_only = [user for user, _ in sorted_users]
                all_users += users_only

            # checks to avoid duplicates
            if exception_type in labels:
                idx = labels.index(exception_type)
                hits = 0
                for user in all_users:
                    if user in common_errors['errors'][idx]['students']:
                        hits += 1
                if hits == len(all_users):
                    # no update needed as entry already exists
                    continue  # skip to next misconception
                elif hits > 0:
                    # update existing entry, existing student(s) was found but new ones have to be added
                    common_errors['errors'][idx]['students'] = all_users
            else:
                # make new entry
                new_id = self.new_id_calc(common_errors, class_id)
                common_errors['errors'].append({
                    'id': new_id,
                    'label': exception_type,
                    'active': 1,
                    "students": users_only
                })
        end = timer()
        logger.debug(f'Time taken by common_exception_detection {end-start}')
        return self.db.update_class_errors(common_errors)

    @route("/live_stats/class/<class_id>", methods=["POST"])
    @requires_login
    def select_levels(self, user, class_id):
        """
        Stores the selected levels in the class overview in the database.
        """
        body = request.json
        levels = [int(i) for i in body["levels"]]

        class_customization = get_customizations(self.db, class_id)
        class_customization['dashboard_customization'] = {
            'selected_levels': levels,
        }

        self.db.update_class_customizations(class_customization)

        return make_response('', 204)


def add(username, action):
    """
    Adds aggregated stats for all users and fine-grained stats for logged-in users.
    Ensures logging stats will not cause a failure.
    """
    try:
        all_id = UserType.ANONYMOUS
        if username:
            action(username)
            # g.db instead of self.db since this function is not on a class
            is_student = g.db.get_student_classes_ids(username) != []
            all_id = UserType.STUDENT if is_student else UserType.LOGGED
        action(all_id.value)
    except Exception as ex:
        # adding stats should never cause failure. Log and continue.
        querylog.log_value(server_error=ex)


def _to_response_per_level(data):
    data.sort(key=lambda el: el["level"])
    return [{"level": f"L{entry['level']}", "data": _data_to_response_per_level(entry["data"])} for entry in data]


def _data_to_response_per_level(data):
    res = {}

    _add_value_to_result(res, "successful_runs", data["successful_runs"], is_counter=True)
    _add_value_to_result(res, "failed_runs", data["failed_runs"], is_counter=True)
    res["error_rate"] = _calc_error_rate(data.get("failed_runs"), data.get("successful_runs"))
    _add_exception_data(res, data)

    _add_value_to_result(res, "anonymous_runs", data["anonymous_runs"], is_counter=True)
    _add_value_to_result(res, "logged_runs", data["logged_runs"], is_counter=True)
    _add_value_to_result(res, "student_runs", data["student_runs"], is_counter=True)
    _add_value_to_result(res, "user_type_unknown_runs", data["user_type_unknown_runs"], is_counter=True)

    _add_value_to_result(res, "abandoned_quizzes", data["total_attempts"] - data["completed_attempts"], is_counter=True)
    _add_value_to_result(res, "completed_quizzes", data["completed_attempts"], is_counter=True)

    min_, max_, avg_ = _score_metrics(data["scores"])
    _add_value_to_result(res, "quiz_score_min", min_)
    _add_value_to_result(res, "quiz_score_max", max_)
    _add_value_to_result(res, "quiz_score_avg", avg_)

    return res


def _to_response(data, values_field, series_selector, values_map=None):
    """
    Transforms aggregated data to a response convenient for charts to use
        - values_field is what shows on the X-axis, e.g. level or week number
        - series_selector determines the data series, e.g. successful runs per level or occurrences of exceptions
    """

    res = {}
    for e in data:
        values = e[values_field]
        series = series_selector(e)
        if values not in res.keys():
            res[values] = {}

        d = e["data"]
        _add_dict_to_result(res[values], "successful_runs", series, d["successful_runs"], is_counter=True)
        _add_dict_to_result(res[values], "failed_runs", series, d["failed_runs"], is_counter=True)
        _add_dict_to_result(
            res[values], "abandoned_quizzes", series, d["total_attempts"] - d["completed_attempts"], is_counter=True
        )
        _add_dict_to_result(res[values], "completed_quizzes", series, d["completed_attempts"], is_counter=True)

        _add_value_to_result(res[values], "anonymous_runs", d["anonymous_runs"], is_counter=True)
        _add_value_to_result(res[values], "logged_runs", d["logged_runs"], is_counter=True)
        _add_value_to_result(res[values], "student_runs", d["student_runs"], is_counter=True)
        _add_value_to_result(res[values], "user_type_unknown_runs", d["user_type_unknown_runs"], is_counter=True)

        min_, max_, avg_ = _score_metrics(d["scores"])
        _add_dict_to_result(res[values], "quiz_score_min", series, min_)
        _add_dict_to_result(res[values], "quiz_score_max", series, max_)
        _add_dict_to_result(res[values], "quiz_score_avg", series, avg_)

        _add_exception_data(res[values], d)

    result = [{values_field: k, "data": _add_error_rate_from_dicts(v)} for k, v in res.items()]
    result.sort(key=lambda el: el[values_field])

    return [values_map(e) for e in result] if values_map else result


def _add_value_to_result(target, key, source, is_counter=False):
    if source is not None and (source > 0 if is_counter else True):
        if not target.get(key):
            target[key] = source
        else:
            target[key] += source


def _add_dict_to_result(target, key, series, source, is_counter=False):
    if source is not None and (source > 0 if is_counter else True):
        if not target.get(key):
            target[key] = {}
        target[key][series] = source


def _score_metrics(scores):
    if not scores:
        return None, None, None
    min_result = scores[0]
    max_result = scores[0]
    total = 0
    for s in scores:
        if s < min_result:
            min_result = s
        if s > max_result:
            max_result = s
        total += s
    return min_result, max_result, total / len(scores)


def _aggregate_for_keys(data, keys):
    """
    Aggregates data by one or multiple keys/dimensions. The implementation 'serializes' the
    values of supplied keys and later 'deserializes' the original values. Improve on demand.
    """

    result = {}
    for record in data:
        key = _aggregate_key(record, keys)
        result[key] = _add_program_run_data(result.get(key), record)
        result[key] = _add_quiz_data(result.get(key), record)
    return [_split_keys_data(k, v, keys) for k, v in result.items()]


def _aggregate_key(record, keys):
    return "#".join([str(record[key.name]) for key in keys])


def _initialize():
    return {
        "failed_runs": 0,
        "successful_runs": 0,
        "anonymous_runs": 0,
        "logged_runs": 0,
        "student_runs": 0,
        "user_type_unknown_runs": 0,
        "total_attempts": 0,
        "completed_attempts": 0,
        "scores": [],
    }


def _add_program_run_data(data, rec):
    if not data:
        data = _initialize()
    value = rec.get("successful_runs") or 0
    data["successful_runs"] += value

    _add_user_type_runs(data, rec.get("id"), value)
    _add_exception_data(data, rec, True)

    return data


def _add_quiz_data(data, rec):
    if not data:
        data = _initialize()
    data["total_attempts"] += rec.get("started") or 0
    data["completed_attempts"] += rec.get("finished") or 0
    data["scores"] += rec.get("scores") or []
    return data


def _add_exception_data(entry, data, include_failed_runs=False):
    exceptions = {k: v for k, v in data.items() if k.lower().endswith("exception")}
    for k, v in exceptions.items():
        if not entry.get(k):
            entry[k] = 0
        entry[k] += v
        if include_failed_runs:
            entry["failed_runs"] += v
            _add_user_type_runs(entry, entry.get("id"), v)


def _add_user_type_runs(data, id_, value):
    if id_ == UserType.ANONYMOUS.value:
        data["anonymous_runs"] += value
    if id_ == UserType.LOGGED.value:
        data["logged_runs"] += value
    if id_ == UserType.STUDENT.value:
        data["student_runs"] += value
    if id_ == UserType.ALL.value:
        data["user_type_unknown_runs"] += value


def _split_keys_data(k, v, keys):
    values = k.split("#")
    res = {keys[i].name: keys[i].class_(values[i]) for i in range(0, len(keys))}
    res["data"] = v
    return res


def _to_response_level_name(e):
    e["level"] = f"L{e['level']}"
    return e


def _add_error_rate_from_dicts(data):
    failed = data.get("failed_runs") or {}
    successful = data.get("successful_runs") or {}
    keys = set.union(set(failed.keys()), set(successful.keys()))
    data["error_rate"] = {k: _calc_error_rate(failed.get(k), successful.get(k)) for k in keys}
    return data


def _calc_error_rate(fail, success):
    failed = fail or 0
    successful = success or 0
    return (failed * 100) / max(1, failed + successful)


def _check_student_arg():
    """
    Checks the arguments of the request and returns the values. Mainly exists to avoid code duplication.
    """

    student = request.args.get("student", default=None, type=str)
    student = None if student == "None" else student

    return student


def _get_available_adventures(adventures, teacher_adventures, customizations, last_adventures):
    """
    Returns the available adventures for all levels, given the possible adventures per level,
    the teacher (adventures) and customization. Also adds how many students are currently in
    progress for each adventure.

    { level: [ { id, name, in_progress } ] }
    """
    adventure_names = {}
    for adv_key, adv_dic in adventures.items():
        for name, _ in adv_dic.items():
            adventure_names[adv_key] = hedy_content.get_localized_name(name, g.keyword_lang)

    for adventure in teacher_adventures:
        adventure_names[adventure['id']] = adventure['name']

    selected_adventures = {}
    for level, adventure_list in customizations['sorted_adventures'].items():
        adventures_for_level = []
        for adventure in list(adventure_list):
            if adventure['name'] == 'next' or adventure['name'] not in adventure_names:
                continue
            adventure_key = adventure['name']

            students_in_progress = []
            for d in last_adventures[int(level) - 1]:
                (student, last_adventure), = d.items()
                if last_adventure == adventure_key:
                    students_in_progress.append(student)

            adventure_name = adventure_names[adventure_key]
            adventures_for_level.append(
                {
                    "id": adventure_key,
                    "name": adventure_name,
                    "in_progress": students_in_progress
                }
            )

        selected_adventures[level] = adventures_for_level

    return selected_adventures


def _get_quiz_info(quiz_stats):
    """
    Returns quiz info for each level containing the students in progress (started but not finished)
    and the students that finished the quiz.

    { level: { students_in_progress, students_finished } }
    """
    quiz_info = {}
    for level in range(1, HEDY_MAX_LEVEL + 1):
        students_in_progress, students_finished = [], []
        for stats in quiz_stats:
            if level in stats.get("in_progress"):
                students_in_progress.append(stats.get("student"))
            elif level in stats.get("finished"):
                students_finished.append(stats.get("student"))

        quiz_info[level] = {"students_in_progress": students_in_progress, "students_finished": students_finished}

    return quiz_info


def _get_error_info(code, level, lang='en'):
    """
    Returns the server error given the code written by the student. Since the database only stores whether
    the code produced an error or not, in order to get the error we have to rerun the code
    through some hedy logic.
    """
    try:
        check_program_size_is_valid(code)

        level = int(level)
        if level > HEDY_MAX_LEVEL:
            raise Exception(f'Levels over {HEDY_MAX_LEVEL} not implemented yet')

        input_string = process_input_string(code, level, lang)
        program_root = parse_input(input_string, level, lang)

        # Checks whether any error production nodes are present in the parse tree
        is_program_valid(program_root, input_string, level, lang)
    except hedy_exceptions.HedyException as exc:
        return exc
    return None


def _build_url_args(**kwargs):
    """
    Builds a string of the url arguments used in the html file for routing.
    This avoids lots of code duplication in the html file as well as making it easier to add/remove/change url
    arguments.
    """
    url_args = ""
    c = 0
    for key, value in kwargs.items():
        if c == 0:
            url_args += f"{key}={value}"
            c += 1
        else:
            url_args += f"&{key}={value}"
    return url_args


def _collect_graph_data(data, window_size=5):
    """
    Collects data to be shown in the line graph and limits it to the window size.
    """
    graph_data, labels = [], []
    c = 0
    for week in data:
        if 'chart_history' in week.keys():
            graph_data += week['chart_history']
            labels += list(range(c + 1, c + 1 + len(week['chart_history'])))
            c += len(week['chart_history'])

    slice = window_size if len(graph_data) > window_size else 0

    return graph_data[-slice:], labels[-slice:]


def get_customizations(db, class_id):
    """
    Retrieves the customizations for a specific class from the database.

    Args:
        db (Database): The database object used to retrieve the customizations.
        class_id (string): The ID of the class for which to retrieve the customizations.

    Returns:
        customizations (dict): A dictionary containing the customizations for the class.
    """
    customizations = db.get_class_customizations(class_id)
    if customizations and 'adventures' in customizations:
        # it uses the old way so convert it to the new one
        customizations['sorted_adventures'] = {str(i): [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
        for adventure, levels in customizations['adventures'].items():
            for level in levels:
                customizations['sorted_adventures'][str(level)].append(
                    {"name": adventure, "from_teacher": False})

        db.update_class_customizations(customizations)
    elif not customizations:
        # Create a new default customizations object in case it doesn't have one
        customizations = _create_customizations(db, class_id)
    return customizations


def _create_customizations(db, class_id):
    """
    Create customizations for a given class.

    Args:
        db (Database): The database object.
        class_id (int): The ID of the class.

    Returns:
        customizations (dict): The customizations for the class.
    """
    sorted_adventures = {}
    for lvl, adventures in hedy_content.ADVENTURE_ORDER_PER_LEVEL.items():
        sorted_adventures[str(lvl)] = [{'name': adventure, 'from_teacher': False} for adventure in adventures]
    customizations = {
        "id": class_id,
        "levels": [i for i in range(1, hedy.HEDY_MAX_LEVEL + 1)],
        "opening_dates": {},
        "other_settings": [],
        "level_thresholds": {},
        "sorted_adventures": sorted_adventures,
        "dashboard_customization": {
            "selected_levels": [1]
        },
    }
    db.update_class_customizations(customizations)
    return customizations
