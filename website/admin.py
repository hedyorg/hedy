from datetime import date

from flask_babel import gettext

from website import statistics
from website.auth import requires_login, current_user, is_admin, pick
import utils
from flask import request
from flask_helpers import render_template


def routes(app, database):
    global DATABASE
    DATABASE = database

    @app.route('/admin', methods=['GET'])
    def get_admin_page():
        if not utils.is_testing_request(request) and not is_admin(current_user()):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))
        return render_template('admin/admin.html', page_title=gettext('title_admin'))

    @app.route('/admin/users', methods=['GET'])
    @requires_login
    def get_admin_users_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        category = request.args.get('filter', default=None, type=str)
        category = None if category == "null" else category

        substring = request.args.get('substring', default=None, type=str)
        start_date = request.args.get('start', default=None, type=str)
        end_date = request.args.get('end', default=None, type=str)
        language = request.args.get('language', default=None, type=str)
        keyword_language = request.args.get('keyword_language', default=None, type=str)

        substring = None if substring == "null" else substring
        start_date = None if start_date == "null" else start_date
        end_date = None if end_date == "null" else end_date
        language = None if language == "null" else language
        keyword_language = None if keyword_language == "null" else keyword_language

        filtering = False
        if substring or start_date or end_date or language or keyword_language or category == "all":
            filtering = True

        # After hitting 1k users, it'd be wise to add pagination.
        users = DATABASE.all_users(filtering)
        userdata = []
        fields = [
            'username', 'email', 'birth_year', 'country',
            'gender', 'created', 'last_login', 'verification_pending',
            'is_teacher', 'program_count', 'prog_experience', 'experience_languages', 'language', 'keyword_language'
        ]

        for user in users:
            data = pick(user, *fields)
            data['email_verified'] = not bool(data['verification_pending'])
            data['is_teacher'] = bool(data['is_teacher'])
            data['created'] = utils.datetotimeordate (utils.mstoisostring(data['created'])) if data['created'] else '?'
            if filtering and category == "language":
                if language != data['language']:
                    continue
            if filtering and category == "keyword_language":
                if keyword_language != data['keyword_language']:
                    continue
            if filtering and category == "email":
                if substring not in data['email']:
                    continue
            if filtering and category == "created":
                if (start_date and utils.datetotimeordate(start_date) >= data['created']) or (end_date and utils.datetotimeordate(end_date) <= data['created']):
                    continue
            if data['last_login']:
                data['last_login'] = utils.datetotimeordate(utils.mstoisostring(data['last_login'])) if data['last_login'] else '?'
                if filtering and category == "last_login":
                    if (start_date and utils.datetotimeordate(start_date) >= data['last_login']) or (end_date and utils.datetotimeordate(end_date) <= data['last_login']):
                        continue
            userdata.append(data)

        return render_template('admin/admin-users.html', users=userdata, page_title=gettext('title_admin'),
                               filter=category, start_date=start_date, end_date=end_date, email_filter=substring,
                               language_filter=language, keyword_language_filter=keyword_language,
                               program_count=DATABASE.all_programs_count(), user_count=DATABASE.all_users_count())

    @app.route('/admin/classes', methods=['GET'])
    @requires_login
    def get_admin_classes_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        classes = [{
            "name": Class.get('name'),
            "teacher": Class.get('teacher'),
            "students": len(Class.get('students')) if 'students' in Class else 0,
            "stats": statistics.get_general_class_stats(Class.get('students', [])),
            "id": Class.get('id')
        } for Class in DATABASE.all_classes()]

        classes = sorted(classes, key=lambda d: d.get('stats').get('week').get('runs'), reverse=True)

        return render_template('admin/admin-classes.html', classes=classes, page_title=gettext('title_admin'))

    @app.route('/admin/adventures', methods=['GET'])
    @requires_login
    def get_admin_adventures_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        adventures = [{
            "id": adventure.get('id'),
            "creator": adventure.get('creator'),
            "name": adventure.get('name'),
            "level": adventure.get('level'),
            "public": "Yes" if adventure.get('public') else "No",
            "date": utils.datetotimeordate(utils.mstoisostring(adventure.get('date')))
        } for adventure in DATABASE.all_adventures()]
        adventures = sorted(adventures, key=lambda d: d['date'], reverse=True)

        return render_template('admin/admin-adventures.html', adventures=adventures, page_title=gettext('title_admin'))

    @app.route('/admin/stats', methods=['GET'])
    @requires_login
    def get_admin_stats_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))
        return render_template('admin/admin-stats.html', page_title=gettext('title_admin'))

    @app.route('/admin/achievements', methods=['GET'])
    @requires_login
    def get_admin_achievements_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        stats = {}
        achievements = hedyweb.AchievementTranslations().get_translations("en").get("achievements")
        for achievement in achievements.keys():
            stats[achievement] = {}
            stats[achievement]["name"] = achievements.get(achievement).get("title")
            stats[achievement]["description"] = achievements.get(achievement).get("text")
            stats[achievement]["count"] = 0

        user_achievements = DATABASE.get_all_achievements()
        total = len(user_achievements)
        for user in user_achievements:
            for achieved in user.get("achieved", []):
                stats[achieved]["count"] += 1

        return render_template('admin/admin-achievements.html', stats=stats,
                               total=total, page_title=gettext('title_admin'))

