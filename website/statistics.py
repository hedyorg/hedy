from collections import namedtuple
from datetime import date
from enum import Enum

from flask import g, jsonify, request
from flask_babel import gettext

import hedy
import utils
from website.flask_helpers import render_template
from website import querylog
from website.auth import is_admin, is_teacher, requires_admin, requires_login

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

    # [work in progress] method for implementing the version 1 of class stats page
    # Method for retrieving student information for a specific class
    @route("/stats/class/<class_id>-v1", methods=["GET"])
    @requires_login
    def render_class_stats_v1(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        students = []
        for student_username in class_.get("students", []):
            student = self.db.user_by_username(student_username)
            programs = self.db.programs_for_user(student_username)
            quizzes = self.db.get_quiz_stats([student_username])

            # find quiz and programs statistics for each student on each level
            program_runs_per_level = []
            success_runs_per_level = []
            error_runs_per_level = []
            quizzes_runs_per_level = []
            avg_quizzes_runs_per_level = []
            for level in range(1, hedy.HEDY_MAX_LEVEL + 1):
                find_program_runs_per_level(program_runs_per_level, success_runs_per_level,
                                            error_runs_per_level, programs, level)
                calc_num_programs_per_level(program_runs_per_level, success_runs_per_level, error_runs_per_level, level)

                find_quizzes_per_level(quizzes_runs_per_level, quizzes, level)
                # calc_avg_quizzes_per_level(avg_quizzes_runs_per_level, quizzes_runs_per_level, level)

            average_quizzes = calc_average_quizzes(avg_quizzes_runs_per_level)
            success_rate_overall = find_success_rate_overall(quizzes)

            finished_quizzes = any("finished" in x for x in quizzes)
            highest_level_quiz = max(
                [x.get("level") for x in quizzes if x.get("finished")]) if finished_quizzes else "-"
            highest_level_quiz_score = (
                [x.get("scores") for x in quizzes if x.get("level") == highest_level_quiz]) if finished_quizzes else "-"

            success_rate_highest_level = calc_highest_success_rate(finished_quizzes, highest_level_quiz, quizzes)

            students.append(
                {
                    "username": student_username,
                    "last_login": student["last_login"],
                    "programs": len(programs),
                    "program_runs_per_level": program_runs_per_level,
                    "success_rate_highest_level": success_rate_highest_level,
                    "success_rate_overall": success_rate_overall,
                    "avg_quizzes_runs_per_level": avg_quizzes_runs_per_level,
                    "average_quiz": average_quizzes,
                    "highest_level_quiz": highest_level_quiz,
                    "highest_level_quiz_score": highest_level_quiz_score,
                }
            )

        students = sorted(students, key=lambda d: d.get("username", 0))

        return render_template(
            "class-stats-v1.html",
            class_info={
                "id": class_id,
                "students": students,
                "name": class_["name"],
            },
            current_page="my-profile",
            page_title=gettext("title_class statistics"),
            javascript_page_options=dict(page='class-stats-v1'),
        )

    # [work in progress] method for implementing the version 2 of class stats page
    # Method for retrieving student information for a specific class
    @route("/stats/class/<class_id>-v2", methods=["GET"])
    @requires_login
    def render_class_stats_v2(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))

        class_ = self.db.get_class(class_id)
        if not class_ or (class_["teacher"] != user["username"] and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        levels = [i for i in range(1, hedy.HEDY_MAX_LEVEL + 1)]

        students = []
        for student_username in class_.get("students", []):
            print(f'Student: {student_username}')
            student = self.db.user_by_username(student_username)
            programs = self.db.programs_for_user(student_username)
            quizzes = self.db.get_quiz_stats([student_username])

            # find quiz and programs statistics for each student on each level
            program_runs_per_level = []
            success_runs_per_level = []
            error_runs_per_level = []
            quizzes_runs_per_level = []
            avg_quizzes_runs_per_level = []

            for level in range(1, hedy.HEDY_MAX_LEVEL + 1):
                find_program_runs_per_level(program_runs_per_level, success_runs_per_level,
                                            error_runs_per_level, programs, level)
                calc_num_programs_per_level(program_runs_per_level, success_runs_per_level, error_runs_per_level, level)

                find_quizzes_per_level(quizzes_runs_per_level, quizzes, level)
                calc_avg_quizzes_per_level(avg_quizzes_runs_per_level, quizzes_runs_per_level, level)

            success_rate_overall = find_success_rate_overall(quizzes)

            finished_quizzes = any("finished" in x for x in quizzes)
            highest_level_quiz = max(
                [x.get("level") for x in quizzes if x.get("finished")]) if finished_quizzes else "-"
            highest_level_quiz_score = (
                [x.get("scores") for x in quizzes if x.get("level") == highest_level_quiz]) if finished_quizzes else "-"

            success_rate_highest_level = calc_highest_success_rate(finished_quizzes, highest_level_quiz, quizzes)

            students.append(
                {
                    "username": student_username,
                    "last_login": student["last_login"],
                    "programs": len(programs),
                    "success_runs_per_level": success_runs_per_level,
                    "error_runs_per_level": error_runs_per_level,
                    "success_rate_highest_level": success_rate_highest_level,
                    "success_rate_overall": success_rate_overall,
                    "avg_quizzes_runs_per_level": avg_quizzes_runs_per_level,
                    "highest_level_quiz": highest_level_quiz,
                    "highest_level_quiz_score": highest_level_quiz_score,
                }
            )

        students = sorted(students, key=lambda d: d.get("username", 0))

        return render_template(
            "class-stats-v2.html",
            class_info={
                "id": class_id,
                "students": students,
                "name": class_["name"],
                "levels": levels,
            },
            current_page="my-profile",
            page_title=gettext("title_class statistics"),
            javascript_page_options=dict(page='class-stats-v2'),
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


# append the programs obtained on each level
def find_program_runs_per_level(program_runs_per_level, success_runs_per_level, error_runs_per_level, programs, level):
    program_runs_per_level.append([])
    success_runs_per_level.append([])
    error_runs_per_level.append([])
    for program in programs:
        if program['level'] == level:
            program_runs_per_level[level - 1].append([program['name'], str(program.get("error"))])
            if str(program.get("error")) == "True":
                success_runs_per_level[level - 1].append(program['name'])
            elif str(program.get("error")) == "False":
                error_runs_per_level[level - 1].append(program['name'])


# append the quizzes obtained on each level
def find_quizzes_per_level(quizzes_per_level, quizzes, level):
    quizzes_per_level.append([])
    for quiz_score in quizzes:
        if quiz_score['level'] == level:
            # if a quiz level is repeated in a different week, you need to handle it differently.
            if len(quiz_score["scores"]) == 1:
                quizzes_per_level[level - 1].append(quiz_score["scores"][0])
            else:
                weekly_quiz_scores = quiz_score["scores"]
                quizzes_per_level[level - 1] = weekly_quiz_scores


def calc_avg_quizzes_per_level(avg_quizzes_ran_per_level, quizzes_ran_per_level, level):
    if not quizzes_ran_per_level[level - 1]:
        avg_quizzes_ran_per_level.append(0)
    else:
        quizzes_per_level = quizzes_ran_per_level[level - 1]
        if len(quizzes_ran_per_level[level - 1]) == 1:
            avg_quizzes_ran_per_level.append(quizzes_per_level[0])
        if len(quizzes_ran_per_level[level - 1]) > 1:
            avg_quiz = sum(quizzes_per_level) / len(quizzes_per_level)
            avg_quizzes_ran_per_level.append(int(avg_quiz))

    return avg_quizzes_ran_per_level


# count the number of programs that the student has run each level
def calc_num_programs_per_level(programs_ran_per_level, success_runs_per_level, error_runs_per_level, level):
    if len(programs_ran_per_level[level - 1]) != 0:
        successful_runs = 0
        unsuccessful_runs = 0
        for program in programs_ran_per_level[level - 1]:
            if str(program[1]) == "True":
                unsuccessful_runs += 1
            else:
                successful_runs += 1
        success_runs_per_level[level - 1] = successful_runs
        error_runs_per_level[level - 1] = unsuccessful_runs
    else:
        success_runs_per_level[level - 1] = 0
        error_runs_per_level[level - 1] = 0

    return success_runs_per_level, error_runs_per_level


def find_success_rate_overall(quizzes):
    success_rate_overall = "-"
    if len(quizzes) != 0:
        num_finished_quizzes = 0
        success_rate_overall = 0
        for index in range(1, len(quizzes) + 1):
            finished_quiz = quizzes[index - 1]['finished']
            started_quiz = quizzes[index - 1]['started']

            num_finished_quizzes += finished_quiz
            success_rate_overall += finished_quiz / started_quiz * 100

        success_rate_overall /= num_finished_quizzes
        success_rate_overall = round(success_rate_overall, ndigits=0)
    return success_rate_overall


def calc_highest_success_rate(finished_quizzes, highest_level_quiz, quizzes):
    success_rate_highest_level = '-'
    if finished_quizzes:
        highest_level_started = ([x.get("started") for x in quizzes if x.get("level") == highest_level_quiz])
        highest_level_finished = ([x.get("finished") for x in quizzes if x.get("level") == highest_level_quiz])
        success_rate_highest_level = (highest_level_finished[0] / highest_level_started[0] * 100)
        success_rate_highest_level = round(success_rate_highest_level, ndigits=0)
    return success_rate_highest_level


def calc_average_quizzes(average_quizzes_ran_per_level):
    average_quizzes = "-"
    num_quizzes = 0
    total_quiz_scores = 0
    for i in range(1, len(average_quizzes_ran_per_level) + 1):
        if average_quizzes_ran_per_level[i - 1] != 0:
            num_quizzes += 1
            total_quiz_scores += average_quizzes_ran_per_level[i - 1]
    if num_quizzes != 0:
        average_quizzes = total_quiz_scores / num_quizzes
    return average_quizzes
