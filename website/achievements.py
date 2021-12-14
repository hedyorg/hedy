from website.auth import requires_login, is_teacher
import utils
import uuid
from flask import request
import hedyweb
TRANSLATIONS = hedyweb.Translations ()
from config import config
cookie_name     = config ['session'] ['cookie_name']


def routes(app, database):
    global DATABASE
    DATABASE = database

    @app.route('/achievements', methods=['POST'])
    @requires_login
    def update_achievements(user):
        return None