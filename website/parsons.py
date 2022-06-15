import copy
import random

from flask import g, jsonify
from flask_babel import gettext


def routes(app, database, achievements, parsons):
    global DATABASE
    global ACHIEVEMENTS
    global PARSONS

    DATABASE = database
    ACHIEVEMENTS = achievements
    PARSONS = parsons

    @app.route('/parsons/get-exercise/<int:level>/<int:exercise>', methods=['GET'])
    def get_parsons_exercise(level, exercise):
        print(exercise)
        print(level)
        if exercise > PARSONS[g.lang].get_highest_exercise_level(level) or exercise < 1:
            return gettext('exercise_doesnt_exist'), 400

        exercise = PARSONS[g.lang].get_parsons_data_for_level_exercise(level, exercise, g.keyword_lang)
        return jsonify(exercise), 200