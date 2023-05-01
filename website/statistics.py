from collections import namedtuple
from datetime import date
from enum import Enum

from flask import g, jsonify, request
from flask_babel import gettext

import utils
from website.flask_helpers import render_template
from website import querylog
from website.auth import is_admin, is_teacher, requires_admin, requires_login

import exceptions as hedy_exceptions
from hedy import check_program_size_is_valid, parse_input, is_program_valid, process_input_string, HEDY_MAX_LEVEL
import hedy_content
from . import dynamo
from .database import Database
from .website_module import WebsiteModule, route

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

    @route("/stats/class/<class_id>", methods=["GET"])
    @requires_login
    def render_class_stats(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        students = sorted(class_.get("students", []))
        return render_template(
            "class-stats.html",
            class_info={"id": class_id, "students": students},
            current_page="my-profile",
            page_title=gettext("title_class statistics"),
            javascript_page_options=dict(page='class-stats'),
        )

    @route("/logs/class/<class_id>", methods=["GET"])
    @requires_login
    def render_class_logs(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        students = sorted(class_.get("students", []))
        return render_template(
            "class-logs.html",
            class_info={"id": class_id, "students": students},
            current_page="my-profile",
            page_title=gettext("title_class logs"),
        )

    @route("/class-stats/<class_id>", methods=["GET"])
    @requires_login
    def get_class_stats(self, user, class_id):
        start_date = request.args.get("start", default=None, type=str)
        end_date = request.args.get("end", default=None, type=str)

        cls = self.db.get_class(class_id)
        students = cls.get("students", [])
        if not cls or not students or (cls["teacher"] != user["username"] and not is_admin(user)):
            return "No such class or class empty", 403

        program_data = self.db.get_program_stats(students, start_date, end_date)
        quiz_data = self.db.get_quiz_stats(students, start_date, end_date)
        data = program_data + quiz_data

        per_level_data = _aggregate_for_keys(data, [level_key])
        per_week_data = _aggregate_for_keys(data, [week_key, level_key])
        per_level_per_student = _aggregate_for_keys(data, [username_key, level_key])
        per_week_per_student = _aggregate_for_keys(data, [username_key, week_key])

        response = {
            "class": {
                "per_level": _to_response_per_level(per_level_data),
                "per_week": _to_response(per_week_data, "week", lambda e: f"L{e['level']}"),
            },
            "students": {
                "per_level": _to_response(per_level_per_student, "level", lambda e: e["id"], _to_response_level_name),
                "per_week": _to_response(per_week_per_student, "week", lambda e: e["id"]),
            },
        }
        return jsonify(response)

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


class LiveStatisticsModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("live-stats", __name__)
        self.db = db
        self.__error_db_load()

    def __error_db_load(self):
        """Loads the error data from the json file. Function mainly exists in order to
        quickly call it again whenever the database needs to be read again for updating purposes.
        """
        self.common_error_db = dynamo.MemoryStorage("radboard_error_data.json")
        self.ERRORS = dynamo.Table(self.common_error_db, "common_errors", "class_id")

    @route("/live_stats/class/<class_id>", methods=["GET"])
    @requires_login
    def render_live_stats(self, user, class_id):

        collapse, show_c1, show_c2, show_c3 = _check_dashboard_display_args()
        # Retrieve common errors from the database for class
        common_errors = self.ERRORS.get({"class_id": class_id})

        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        students = sorted(class_.get("students", []))
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
                }
            )
        return render_template(
            "class-live-stats.html",
            class_info={"id": class_id, "students": students, "common_errors": common_errors},
            dashboard_options={"show_c1": show_c1, "show_c2": show_c2, "show_c3": show_c3, "collapse": collapse},
            current_page="my-profile",
            page_title=gettext("title_class live_statistics")
        )

    @route("/live_stats/class/<class_id>/student", methods=["GET"])
    @requires_login
    def render_student_details(self, user, class_id):
        """ Shows information about an individual student when they
        are selected in the student list.
        """
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))

        collapse, show_c1, show_c2, show_c3 = _check_dashboard_display_args()
        # Retrieve common errors from the database for class
        common_errors = self.ERRORS.get({"class_id": class_id})

        class_ = self.db.get_class(class_id)
        students = sorted(class_.get("students", []))

        # retrieve username of student in question via args
        student = request.args.get("student", default=None, type=str)
        if student not in students:
            return utils.error_page(error=403, ui_message=gettext('not_enrolled'))

        # get data for all students
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
                }
            )

        # Get data for selected student
        programs = self.db.programs_for_user(student)
        quiz_scores = self.db.get_quiz_stats([student])
        finished_quizzes = any("finished" in x for x in quiz_scores)
        highest_quiz = max([x.get("level") for x in quiz_scores if x.get("finished")]) if finished_quizzes else "-"
        selected_student = {"username": student, "programs": len(programs), "highest_level": highest_quiz}

        # load in all program data for that specific student
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
                 'error_message': _translate_error(error_class, item['lang']) if error_class else None,
                 'error_header': 'Oops'  # TODO: get proper header message, e.g. Transpile_error
                 }
            )

        adventure_names = hedy_content.Adventures(g.lang).get_adventure_names()

        return render_template(
            "student-space.html",
            class_info={"id": class_id, "students": students,
                        "common_errors": common_errors},
            dashboard_options={"show_c1": show_c1, "show_c2": show_c2, "show_c3": show_c3, "collapse": collapse},
            student=selected_student,
            student_programs=student_programs,
            adventure_names=adventure_names,
            current_page='my-profile',
            page_title=gettext("title_class live_statistics")
        )

    @route("/live_stats/class/<class_id>/pop_up", methods=["GET"])
    @requires_login
    def render_common_error_items(self, user, class_id):
        """
        Handles the rendering of the common error items in the common errors detection list.
        """

        collapse, show_c1, show_c2, show_c3 = _check_dashboard_display_args()
        # Retrieve common errors from the database for class
        common_errors = self.ERRORS.get({"class_id": class_id})

        class_ = self.db.get_class(class_id)
        students = sorted(class_.get("students", []))

        # retrieve username of student in question via args
        selected_student = request.args.get("student", default=None, type=str)

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
                }
            )

        return render_template(
            "class-live-popup.html",
            class_info={"id": class_id, "students": students,
                        "common_errors": common_errors},
            dashboard_options={"show_c1": show_c1, "show_c2": show_c2, "show_c3": show_c3, "collapse": collapse},
            student=selected_student,
            current_page='my-profile'
        )

    @route("/live_stats/class/<class_id>/error/<error_id>", methods=["DELETE"])
    @requires_login
    def remove_common_error_item(self, user, class_id, error_id):
        """"
        Removes the common error item by setting the active flag to 0.
        """
        common_errors = dynamo.Table(self.common_error_db, "common_errors", "class_id").get({"class_id": class_id})
        for i in range(len(common_errors['errors'])):
            if common_errors['errors'][i]['id'] == error_id and common_errors['errors'][i]['active'] == 1:
                common_errors['errors'][i]['active'] = 0
                self.ERRORS.put(common_errors)
                self.__error_db_load()
                break

        return {}, 200


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


def _determine_bool(bool_str):
    if bool_str == "True":
        return True
    return False


def _check_dashboard_display_args():
    """
    Checks the arguments of the request and returns the values. Mainly exists to avoid code duplication.
    """
    collapse = request.args.get("collapse", default="True", type=str)
    collapse = _determine_bool(collapse)

    show_c1 = request.args.get("show_c1", default="True", type=str)
    show_c1 = _determine_bool(show_c1)

    show_c2 = request.args.get("show_c2", default="True", type=str)
    show_c2 = _determine_bool(show_c2)

    show_c3 = request.args.get("show_c3", default="True", type=str)
    show_c3 = _determine_bool(show_c3)

    return collapse, show_c1, show_c2, show_c3


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

        # checks whether any error production nodes are present in the parse tree
        is_program_valid(program_root, input_string, level, lang)
    except hedy_exceptions.HedyException as exc:
        return exc
    return None


def _translate_error(error_class, lang):
    """
    Translates the error code to the given language.
    This is because the error code needs to be passed through the translation things in order to give more info on the
    student details
    screen.

    A part of this code is duplicate from app.hedy_error_to_response but importing app.py leads to circular
    imports and moving those functions to util.py is cumbersome (but not impossible) given the integration with other
    functions in app.py
    """
    class_args = error_class.arguments

    error_template = gettext('' + str(error_class.error_code))

    # check if argument is substring of error_template, if so replace
    for k, v in class_args.items():
        if f'{{{k}}}' in error_template:
            error_template = error_template.replace(f'{{{k}}}', str(v))

    return error_template


def get_general_class_stats(students):
    # g.db instead of self.db since this function is not on a class
    current_week = g.db.to_year_week(date.today())
    data = g.db.get_program_stats(students, None, None)
    successes = 0
    errors = 0
    weekly_successes = 0
    weekly_errors = 0

    for entry in data:
        entry_successes = int(entry.get("successful_runs", 0))
        entry_errors = sum([v for k, v in entry.items() if k.lower().endswith("exception")])
        successes += entry_successes
        errors += entry_errors
        if entry.get("week") == current_week:
            weekly_successes += entry_successes
            weekly_errors += entry_errors

    return {
        "week": {"runs": weekly_successes + weekly_errors, "fails": weekly_errors},
        "total": {"runs": successes + errors, "fails": errors},
    }
