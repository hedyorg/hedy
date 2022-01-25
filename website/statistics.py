from collections import namedtuple
from flask import request, jsonify

import hedyweb
from flask_helpers import render_template
from website.auth import requires_login, is_admin, is_teacher

import utils

DATABASE = None

"""The Key tuple is used to aggregate the raw data by level, time or username."""
Key = namedtuple('Key', ['name', 'class_'])
level_key = Key('level', int)
username_key = Key('id', str)
week_key = Key('week', str)


def routes(app, db):
    global DATABASE
    DATABASE = db

    @app.route('/stats/class/<class_id>', methods=['GET'])
    @requires_login
    def render_class_stats(user, class_id):
        if not is_teacher(user):
            return utils.error_page(error=403, ui_message='retrieve_class')

        class_ = DATABASE.get_class(class_id)
        if not class_ or (class_['teacher'] != user['username'] and not is_admin(user)):
            return utils.error_page(error=404, ui_message='no_such_class')

        return render_template('class-stats.html', class_info={'id': class_id},
                               current_page='my-profile', page_title=hedyweb.get_page_title('class statistics'))

    @app.route('/class-stats/<class_id>', methods=['GET'])
    @requires_login
    def get_class_stats(user, class_id):
        start_date = request.args.get('start', default=None, type=str)
        end_date = request.args.get('end', default=None, type=str)

        cls = DATABASE.get_class(class_id)
        if not cls or (cls['teacher'] != user['username'] and not is_admin(user)):
            return utils.error_page(error=403, ui_message='no_such_class')

        data = DATABASE.get_class_program_stats(cls['students'], start_date, end_date)

        per_level_data = _aggregate_for_keys(data, [level_key])
        per_week_data = _aggregate_for_keys(data, [week_key, level_key])
        per_level_per_student = _aggregate_for_keys(data, [username_key, level_key])
        per_week_per_student = _aggregate_for_keys(data, [username_key, week_key])

        response = {
            'class': {
                'per_level': _to_response_per_level(per_level_data),
                'per_week': _to_response(per_week_data, 'week', lambda e: f"L{e['level']}")
            },
            'students': {
                'per_level': _to_response(per_level_per_student, 'level', lambda e: e['id'], _to_response_level_name),
                'per_week': _to_response(per_week_per_student, 'week', lambda e: e['id'])
            }
        }
        return jsonify(response)

    @app.route('/program-stats', methods=['GET'])
    @requires_login
    def get_program_stats(user):
        start_date = request.args.get('start', default=None, type=str)
        end_date = request.args.get('end', default=None, type=str)

        if not is_admin(user):
            return utils.error_page(error=403, ui_message='unauthorized')

        data = DATABASE.get_all_program_stats(start_date, end_date)
        per_level_data = _aggregate_for_keys(data, [level_key])
        per_week_data = _aggregate_for_keys(data, [week_key, level_key])

        response = {
            'per_level': _to_response_per_level(per_level_data),
            'per_week': _to_response(per_week_data, 'week', lambda e: f"L{e['level']}")
        }
        return jsonify(response)


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
            res[values] = {'successful_runs': {}, 'failed_runs': {}}
        res[values]['successful_runs'][series] = e['data']['successful_runs']
        res[values]['failed_runs'][series] = e['data']['failed_runs']
        _add_exception_data(res[values], e['data'])

    result = [{values_field: k, 'data': _add_error_rate_from_dicts(v)} for k, v in res.items()]
    result.sort(key=lambda el: el[values_field])

    return [values_map(e) for e in result] if values_map else result


def _aggregate_for_keys(data, keys):
    """
    Aggregates data by one or multiple keys/dimensions. The implementation 'serializes' the
    values of supplied keys and later 'deserializes' the original values. Improve on demand.
    """

    result = {}
    for record in data:
        key = _aggregate_key(record, keys)
        result[key] = _add_program_run_data(result.get(key), record)
    return [_split_keys_data(k, v, keys) for k, v in result.items()]


def _aggregate_key(record, keys):
    return '#'.join([str(record[key.name]) for key in keys])


def _add_program_run_data(data, rec):
    if not data:
        data = {'failed_runs': 0, 'successful_runs': 0}
    data['successful_runs'] += rec.get('successful_runs') or 0
    _add_exception_data(data, rec, True)
    return data


def _add_exception_data(entry, data, include_failed_runs=False):
    exceptions = {k: v for k, v in data.items() if k.lower().endswith('exception')}
    for k, v in exceptions.items():
        if not entry.get(k):
            entry[k] = 0
        entry[k] += v
        if include_failed_runs:
            entry['failed_runs'] += v


def _split_keys_data(k, v, keys):
    values = k.split('#')
    res = {keys[i].name: keys[i].class_(values[i]) for i in range(0, len(keys))}
    res['data'] = v
    return res


def _to_response_level_name(e):
    e['level'] = f"L{e['level']}"
    return e


def _to_response_per_level(data):
    data.sort(key=lambda el: el['level'])
    return [{'level': f"L{entry['level']}", 'data': _add_error_rate(entry['data'])} for entry in data]


def _add_error_rate(data):
    data['error_rate'] = _calc_error_rate(data.get('failed_runs'), data.get('successful_runs'))
    return data


def _add_error_rate_from_dicts(data):
    failed = data.get('failed_runs') or {}
    successful = data.get('successful_runs') or {}
    keys = set.union(set(failed.keys()), set(successful.keys()))
    data['error_rate'] = {k: _calc_error_rate(failed.get(k), successful.get(k)) for k in keys}
    return data


def _calc_error_rate(fail, success):
    failed = fail or 0
    successful = success or 0
    return (failed * 100) / max(1, failed + successful)
