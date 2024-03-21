import collections
import json
import os
import uuid

from flask import g, jsonify, request, session, url_for, redirect
from jinja_partials import render_partial
from flask_babel import gettext

import hedy
import hedy_content
import hedyweb
import utils
from safe_format import safe_format
from website.server_types import SortedAdventure
from website.flask_helpers import render_template
from website.auth import (
    is_admin,
    is_teacher,
    requires_login,
    requires_teacher,
    store_new_student_account,
    validate_student_signup_data,
)

from .achievements import Achievements
from .database import Database
from .website_module import WebsiteModule, route
from datetime import date

SLIDES = collections.defaultdict(hedy_content.NoSuchSlides)
for lang in hedy_content.ALL_LANGUAGES.keys():
    SLIDES[lang] = hedy_content.Slides(lang)


class ForTeachersModule(WebsiteModule):
    def __init__(self, db: Database, achievements: Achievements):
        super().__init__("teachers", __name__, url_prefix="/for-teachers")
        self.db = db
        self.achievements = achievements

    @route("/", methods=["GET"])
    @requires_teacher
    def for_teachers_page(self, user):
        welcome_teacher = session.get("welcome-teacher") or False
        session.pop("welcome-teacher", None)

        teacher_classes = self.db.get_teacher_classes(user["username"], True)
        adventures = []
        teacher_adventures = self.db.get_teacher_adventures(user["username"])
        # Get the adventures that are created by my second teachers.
        second_teacher_adventures = self.db.get_second_teacher_adventures(teacher_classes, user["username"])
        # second_teacher_adventures = self.db.get_second_teacher_adventures(user)
        for adventure in list(teacher_adventures) + second_teacher_adventures:
            adventures.append(
                {
                    "id": adventure.get("id"),
                    "name": adventure.get("name"),
                    "creator": adventure.get("creator"),
                    "author": adventure.get("author"),
                    "date": utils.localized_date_format(adventure.get("date")),
                    "level": adventure.get("level"),
                    "levels": adventure.get("levels"),
                }
            )

        keyword_language = request.args.get('keyword_language', default=g.keyword_lang, type=str)
        slides = []
        for level in range(hedy.HEDY_MAX_LEVEL + 1):
            if SLIDES[g.lang].get_slides_for_level(level, keyword_language):
                slides.append(level)

        return render_template(
            "for-teachers.html",
            current_page="for-teachers",
            page_title=gettext("title_for-teacher"),
            teacher_classes=teacher_classes,
            teacher_adventures=adventures,
            welcome_teacher=welcome_teacher,
            slides=slides,
            javascript_page_options=dict(
                page='for-teachers',
                welcome_teacher=welcome_teacher,
            ))

    @route("/manual", methods=["GET"], defaults={'section_key': 'intro'})
    @route("/manual/<section_key>", methods=["GET"])
    def get_teacher_manual(self, section_key):
        content = hedyweb.PageTranslations("for-teachers").get_page_translations(g.lang)

        # Code very defensively around types here -- Weblate has a tendency to mess up the YAML,
        # so the structure cannot be trusted.
        page_title = content.get('title', '')
        sections = {section['key']: section for section in content['teacher-guide']}
        section_titles = [(section['key'], section.get('title', '')) for section in content['teacher-guide']]
        try:
            current_section = sections[section_key]
        except KeyError:
            current_section = content['teacher-guide'][0]

        if not current_section:
            return utils.error_page(error=404, ui_message=gettext("page_not_found"))

        intro = current_section.get('intro')

        # Some pages have 'subsections', others have 'levels'. We're going to treat them ~the same.
        # Give levels a 'title' field as well (doesn't have it in the YAML).
        subsections = current_section.get('subsections', [])
        for subsection in subsections:
            subsection.setdefault('title', '')
        levels = current_section.get('levels', [])
        for level in levels:
            level['title'] = gettext('level') + ' ' + str(level['level'])

        subsection_titles = [x.get('title', '') for x in subsections + levels]

        return render_template("teacher-manual.html",
                               current_page="teacher-manual",
                               page_title=page_title,
                               section_titles=section_titles,
                               section_key=section_key,
                               section_title=current_section['title'],
                               intro=intro,
                               subsection_titles=subsection_titles,
                               subsections=subsections,
                               levels=levels)

    @route("/class/<class_id>", methods=["GET"])
    @requires_login
    def get_class(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        session['class_id'] = class_id
        students = []
        survey_id = ""
        description = ""
        questions = []
        survey_later = ""
        total_questions = ""

        if Class.get("students"):
            survey_id, description, questions, total_questions, survey_later = self.class_survey(class_id)

        for student_username in Class.get("students", []):
            student = self.db.user_by_username(student_username)
            programs = self.db.programs_for_user(student_username)
            # Fixme: The get_quiz_stats function requires a list of ids -> doesn't work on single string
            quiz_scores = self.db.get_quiz_stats([student_username])
            # Verify if the user did finish any quiz before getting the max() of the finished levels
            finished_quizzes = any("finished" in x for x in quiz_scores)
            highest_quiz = max([x.get("level") for x in quiz_scores if x.get("finished")]) if finished_quizzes else "-"
            students.append(
                {
                    "username": student_username,
                    "last_login": student["last_login"],
                    "programs": len(programs),
                    "highest_level": highest_quiz,
                }
            )

        # Sort the students by their last login
        students = sorted(students, key=lambda d: d.get("last_login", 0), reverse=True)
        # After sorting: replace the number value by a string format date
        for student in students:
            student["last_login"] = utils.localized_date_format(student.get("last_login", 0))

        if utils.is_testing_request(request):
            return jsonify({"students": students, "link": Class["link"], "name": Class["name"], "id": Class["id"]})

        achievement = None
        if len(students) > 20:
            achievement = self.achievements.add_single_achievement(user["username"], "full_house")
        if achievement:
            achievement = json.dumps(achievement)

        invites = []
        for invite in self.db.get_class_invitations(Class["id"]):
            invites.append(
                {
                    "username": invite["username"],
                    "invited_as_text": invite["invited_as_text"],
                    "timestamp": utils.localized_date_format(invite["timestamp"], short_format=True),
                    "expire_timestamp": utils.localized_date_format(invite["ttl"], short_format=True),
                }
            )

            """
            class_info=class_info, GOT IT
                    max_level=max_level, 
                    adventure_names=adventure_names, 
                    adventures_default_order=adventures_default_order,
                    class_id=class_id, GOT IT 
                    level='1', 
                    class_adventures=class_adventures,
                    ticked_adventures=ticked_adventures,
                    student_adventures=student_adventures,
                    matrix_values=matrix_values
            """

        student_overview_table, class_, class_adventures_formatted, ticked_adventures, \
            adventure_names, student_adventures = self.get_grid_info(user, class_id, 1)

        teacher = user if Class["teacher"] == user["username"] else self.db.user_by_username(Class["teacher"])
        second_teachers = [teacher] + Class.get("second_teachers", [])
        print("HELLO")
        print(student_adventures)
        print(class_adventures_formatted)
        return render_template(
            "class-overview.html",
            current_page="for-teachers",
            page_title=gettext("title_class-overview"),
            achievement=achievement,
            invites=invites,
            class_info={
                "students": students,
                "link": os.getenv("BASE_URL", "") + "/hedy/l/" + Class["link"],
                "teacher": Class["teacher"],
                "second_teachers": second_teachers,
                "name": Class["name"],
                "id": Class["id"],
            },
            javascript_page_options=dict(page="class-overview"),
            survey_id=survey_id,
            description=description,
            questions=questions,
            total_questions=total_questions,
            survey_later=survey_later,
            adventure_table={
                'students': student_overview_table,
                'adventures': class_adventures_formatted,
                'student_adventures': student_adventures,
                'level': '1'
            }
        )

    def get_grid_info(self, user, class_id, level):
        class_ = self.db.get_class(class_id)
        if hedy_content.Adventures(g.lang).has_adventures():
            adventures = hedy_content.Adventures(g.lang).get_adventure_keyname_name_levels()
        else:
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
                current_program = {}
                for _, program in programs.items():
                    # Old programs sometimes don't have adventures associated to them
                    # So skip them
                    if 'adventure_name' not in program:
                        continue
                    name = adventure_names.get(program['adventure_name'], program['adventure_name'])
                    customized_level = class_adventures_formatted.get(str(program['level']))
                    if name in customized_level:
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

    @route("/class/<class_id>/preview", methods=["GET"])
    @requires_login
    def preview_class_as_teacher(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))
        session["preview_class"] = {
            "id": Class["id"],
            "name": Class["name"],
        }
        return redirect("/hedy")

    @route("/clear-preview-class", methods=["GET"])
    # Note: we explicitly do not need login here, anyone can exit preview mode
    def clear_preview_class(self):
        try:
            del session["preview_class"]
        except KeyError:
            pass
        return redirect("/for-teachers")

    @route("/class/<class_id>/programs/<username>", methods=["GET", "POST"])
    @requires_teacher
    def public_programs(self, user, class_id, username):
        Class = self.db.get_class(class_id)
        if not Class:
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        from_user = username or request.args.get("user")
        if not from_user and not is_admin(user):
            return utils.error_page(error=404, ui_message=gettext("no_programs"))

        allowed_to_edit = session.get("class_id", False) and utils.can_edit_class(user, Class)

        if from_user and not utils.can_edit_class(user, Class):
            return utils.error_page(error=403, ui_message=gettext('not_teacher'))

        # We request our own page -> also get the public_profile settings
        public_profile = None
        if allowed_to_edit:
            public_profile = self.db.get_public_profile_settings(from_user)

        level = request.args.get('level', default=None, type=str) or None
        adventure = request.args.get('adventure', default=None, type=str) or None
        page = request.args.get('page', default=None, type=str)
        filter = request.args.get('filter', default=None, type=str)
        submitted = True if filter == 'submitted' else None

        result = self.db.filtered_programs_for_user(from_user,
                                                    level=level,
                                                    adventure=adventure,
                                                    submitted=submitted,
                                                    pagination_token=page,
                                                    public=True,
                                                    limit=10)

        programs = []
        for item in result:
            date = utils.delta_timestamp(item['date'])
            # This way we only keep the first 4 lines to show as preview to the user
            preview_code = "\n".join(item['code'].split("\n")[:4])
            programs.append(
                {'id': item['id'],
                 'preview_code': preview_code,
                 'code': item['code'],
                 'date': date,
                 'level': item['level'],
                 'name': item['name'],
                 'adventure_name': item.get('adventure_name'),
                 'submitted': item.get('submitted'),
                 'public': item.get('public'),
                 'number_lines': item['code'].count('\n') + 1
                 }
            )

        keyword_lang = g.keyword_lang
        adventure_names = hedy_content.Adventures(g.lang).get_adventure_names(keyword_lang)

        next_page_url = url_for('programs_page', **dict(request.args, page=result.next_page_token)
                                ) if result.next_page_token else None

        return render_template(
            'programs.html',
            programs=programs,
            page_title=gettext('title_programs'),
            current_page='for-teachers',
            from_user=from_user,
            public_profile=public_profile,
            adventure_names=adventure_names,
            max_level=hedy.HEDY_MAX_LEVEL,
            next_page_url=next_page_url,
            class_id=class_id,
            second_teachers_programs=True)

    @route("/customize-class/<class_id>", methods=["GET"])
    @requires_login
    def get_class_customization_page(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        session['class_id'] = class_id
        customizations, adventures, adventure_names, available_adventures, min_level = \
            self.get_class_info(user, class_id)

        return render_template(
            "customize-class.html",
            page_title=gettext("title_customize-class"),
            class_info={"name": Class["name"], "id": Class["id"], "teacher": Class["teacher"]},
            max_level=hedy.HEDY_MAX_LEVEL,
            customizations=customizations,
            adventures=adventures,
            adventure_names=adventure_names,
            available_adventures=available_adventures,
            custom_adventures=list(dict.fromkeys(
                [item for sublist in available_adventures.values() for item in sublist if item.is_teacher_adventure])),
            adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
            current_page="for-teachers",
            min_level=min_level,
            class_id=class_id,
            javascript_page_options=dict(
                page='customize-class',
                class_id=class_id
            ))

    @route("/load-survey/<class_id>", methods=["POST"])
    def load_survey(self, class_id):
        survey_id, description, questions, total_questions, survey_later = self.class_survey(class_id)
        return render_partial('htmx-survey.html', survey_id=survey_id, description=description,
                              questions=questions, survey_later=survey_later, click='yes')

    def class_survey(self, class_id):
        description = ""
        survey_id = "class" + '_' + class_id
        description = gettext("class_survey_description")
        survey_later = gettext("class_survey_later")
        questions = []
        total_questions = 4

        survey = self.db.get_survey(survey_id)
        if not survey:
            self.db.store_survey(dict(id=f"{survey_id}"))
            survey = self.db.get_survey(survey_id)
        elif survey.get('skip') is True or survey.get('skip') == date.today().isoformat():
            return "", "", "", "", ""

        questions.append(gettext("class_survey_question1"))
        questions.append(gettext("class_survey_question2"))
        questions.append(gettext("class_survey_question3"))
        questions.append(gettext("class_survey_question4"))
        unanswered_questions, translate_db = utils.get_unanswered_questions(survey, questions)
        if translate_db:
            self.db.add_survey_responses(survey_id, translate_db)
        return survey_id, description, unanswered_questions, total_questions, survey_later

    @route("/get-customization-level", methods=["GET"])
    @requires_login
    def change_dropdown_level(self, user):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(session['class_id'])
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        level = request.args.get('level')
        customizations, adventures, adventure_names, available_adventures, _ = self.get_class_info(
            user, session['class_id'])

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/add-adventure/level/<level>", methods=["POST"])
    @requires_login
    def add_adventure(self, user, level):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(session['class_id'])
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        adventure_id = request.form.get('adventure_id')
        customizations, adventures, adventure_names, available_adventures, _ = self.get_class_info(
            user, session['class_id'])
        teacher_adventures = list(self.db.get_teacher_adventures(user["username"]))
        second_teacher_adventures = self.db.get_second_teacher_adventures([Class], user["username"])
        teacher_adventures += second_teacher_adventures
        is_teacher_adventure = self.is_adventure_from_teacher(adventure_id, teacher_adventures)

        customizations['sorted_adventures'][level].append({'name': adventure_id, 'from_teacher': is_teacher_adventure})
        sorted_adventure = SortedAdventure(short_name=adventure_id,
                                           long_name=adventure_names[adventure_id],
                                           is_teacher_adventure=is_teacher_adventure,
                                           is_command_adventure=adventure_id in hedy_content.KEYWORDS_ADVENTURES)

        adventures[int(level)].append(sorted_adventure)
        self.db.update_class_customizations(customizations)
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/remove-adventure", methods=["POST"])
    @requires_login
    def remove_adventure_from_class(self, user):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(session['class_id'])
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        adventure_id = request.args.get('adventure_id')
        level = request.args.get('level')
        teacher_adventures = list(self.db.get_teacher_adventures(user["username"]))
        second_teacher_adventures = self.db.get_second_teacher_adventures([Class], user["username"])
        teacher_adventures += second_teacher_adventures

        is_teacher_adventure = self.is_adventure_from_teacher(adventure_id, teacher_adventures)
        customizations, adventures, adventure_names, available_adventures, _ = self.get_class_info(
            user, session['class_id'])
        customizations['sorted_adventures'][level].remove({'name': adventure_id, 'from_teacher': is_teacher_adventure})
        sorted_adventure = SortedAdventure(short_name=adventure_id,
                                           long_name=adventure_names[adventure_id],
                                           is_teacher_adventure=is_teacher_adventure,
                                           is_command_adventure=adventure_id in hedy_content.KEYWORDS_ADVENTURES)
        adventures[int(level)].remove(sorted_adventure)
        self.db.update_class_customizations(customizations)
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/sort-adventures", methods=["POST"])
    @requires_login
    def sort_adventures_in_class(self, user):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(session['class_id'])
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        customizations, adventures, adventure_names, available_adventures, _ = self.get_class_info(
            user, session['class_id'])
        level = request.args.get('level')
        adventures_from_request = request.form.getlist('adventure')
        teacher_adventures = list(self.db.get_teacher_adventures(user["username"]))
        second_teacher_adventures = self.db.get_second_teacher_adventures([Class], user["username"])
        teacher_adventures += second_teacher_adventures
        customizations['sorted_adventures'][level] = []
        adventures[int(level)] = []
        for adventure in adventures_from_request:
            is_teacher_adventure = self.is_adventure_from_teacher(adventure, teacher_adventures)
            customizations['sorted_adventures'][level].append({'name': adventure, 'from_teacher': is_teacher_adventure})
            sorted_adventure = SortedAdventure(short_name=adventure,
                                               long_name=adventure_names[adventure],
                                               is_teacher_adventure=is_teacher_adventure,
                                               is_command_adventure=adventure in hedy_content.KEYWORDS_ADVENTURES)
            adventures[int(level)].append(sorted_adventure)

        self.db.update_class_customizations(customizations)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    def get_class_info(self, user, class_id):
        if hedy_content.Adventures(g.lang).has_adventures():
            default_adventures = hedy_content.Adventures(g.lang).get_adventure_keyname_name_levels()
        else:
            default_adventures = hedy_content.Adventures("en").get_adventure_keyname_name_levels()

        teacher_adventures = list(self.db.get_teacher_adventures(user["username"]))
        second_teacher_adventures = self.db.get_second_teacher_adventures(
            [self.db.get_class(class_id)], user["username"])
        teacher_adventures += second_teacher_adventures
        customizations = self.db.get_class_customizations(class_id)

        # Initialize the data structures that will hold the adventures for each level
        adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL+1)}

        min_level = 1
        adventure_names = {}
        for adv_key, adv_dic in default_adventures.items():
            for name, _ in adv_dic.items():
                adventure_names[adv_key] = hedy_content.get_localized_name(name, g.keyword_lang)

        for adventure in teacher_adventures:
            adventure_names[adventure['id']] = adventure['name']

        if customizations:
            # in case this class has thew new way to select adventures
            if 'sorted_adventures' in customizations:
                # remove from customizations adventures that we have removed
                self.purge_customizations(customizations['sorted_adventures'], default_adventures, teacher_adventures)
            # it uses the old way so convert it to the new one
            elif 'adventures' in customizations:
                customizations['sorted_adventures'] = {str(i): [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
                for adventure, levels in customizations['adventures'].items():
                    for level in levels:
                        customizations['sorted_adventures'][str(level)].append(
                            {"name": adventure, "from_teacher": False})
            customizations["updated_by"] = user["username"]
            self.db.update_class_customizations(customizations)
            min_level = 1 if customizations['levels'] == [] else min(customizations['levels'])
        else:
            # Since it doesn't have customizations loaded, we create a default customization object.
            # This makes further updating with HTMX easier
            adventures_to_db = {}
            for level, default_adventures in hedy_content.ADVENTURE_ORDER_PER_LEVEL.items():
                adventures_to_db[str(level)] = [{'name': adventure, 'from_teacher': False}
                                                for adventure in default_adventures]

            customizations = {
                "id": class_id,
                "levels": [i for i in range(1, hedy.HEDY_MAX_LEVEL + 1)],
                "opening_dates": {},
                "other_settings": [],
                "level_thresholds": {},
                "sorted_adventures": adventures_to_db,
                "updated_by": user["username"],
            }
            self.db.update_class_customizations(customizations)

        for level, sorted_adventures in customizations['sorted_adventures'].items():
            for adventure in sorted_adventures:
                if adventure['name'] in adventure_names:
                    sorted_adventure = SortedAdventure(short_name=adventure['name'],
                                                       long_name=adventure_names[adventure['name']],
                                                       is_command_adventure=adventure['name']
                                                       in hedy_content.KEYWORDS_ADVENTURES,
                                                       is_teacher_adventure=adventure['from_teacher'])
                adventures[int(level)].append(sorted_adventure)

        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return customizations, adventures, adventure_names, available_adventures, min_level

    # Remove adventures from customizations that aren't in use anymore
    # They can be default and therefore we removed then, or from the teacher
    # and tehrefore removed by the user
    def purge_customizations(self, sorted_adventures, adventures, teacher_adventures):
        teacher_adventures_set = {adventure['id'] for adventure in teacher_adventures}
        for _, adventure_list in sorted_adventures.items():
            for adventure in list(adventure_list):
                if adventure['name'] not in adventures and adventure['name'] not in teacher_adventures_set:
                    adventure_list.remove(adventure)

    def get_unused_adventures(self, adventures, teacher_adventures_db, adventure_names):
        available_adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL+1)}
        default_adventures = {i: set() for i in range(1, hedy.HEDY_MAX_LEVEL+1)}
        teacher_adventures = {i: set() for i in range(1, hedy.HEDY_MAX_LEVEL+1)}

        for level, level_default_adventures in hedy_content.ADVENTURE_ORDER_PER_LEVEL.items():
            for short_name in level_default_adventures:
                adventure = SortedAdventure(short_name=short_name,
                                            long_name=adventure_names.get(short_name, short_name),
                                            is_teacher_adventure=False,
                                            is_command_adventure=short_name in hedy_content.KEYWORDS_ADVENTURES)
                default_adventures[level].add(adventure)

        for teacher_adventure in teacher_adventures_db:
            adventure = SortedAdventure(short_name=teacher_adventure['id'],
                                        long_name=teacher_adventure['name'],
                                        is_teacher_adventure=True,
                                        is_command_adventure=False,)
            # levels=teacher_adventure.get("levels", []))
            for level in teacher_adventure.get("levels", [teacher_adventure.get("level")]):
                teacher_adventures[int(level)].add(adventure)

        for level in range(1, hedy.HEDY_MAX_LEVEL + 1):
            adventures_set = set(adventures[level])
            available_teacher_adventures = teacher_adventures[level].difference(adventures_set)
            available_default_adventures = default_adventures[level].difference(adventures_set)
            available_adventures[level] = list(available_teacher_adventures.union(available_default_adventures))
            available_adventures[level].sort(key=lambda item: item.long_name.upper())

        return available_adventures

    def is_adventure_from_teacher(self, adventure_id, teacher_adventures):
        is_teacher_adventure = False
        for adventure in teacher_adventures:
            if adventure_id == adventure['id']:
                is_teacher_adventure = True
        return is_teacher_adventure

    @route("/restore-customizations", methods=["POST"])
    @requires_teacher
    def restore_customizations_to_default(self, user):
        class_id = session['class_id']
        level = request.args.get('level')

        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))
        teacher_adventures = list(self.db.get_teacher_adventures(user["username"]))
        second_teacher_adventures = self.db.get_second_teacher_adventures([Class], user["username"])
        teacher_adventures += second_teacher_adventures

        customizations, adventures, adventure_names, available_adventures, _ = self.get_class_info(
            user, session['class_id'])

        db_adventures = {str(i): [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
        adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}

        for lvl, default_adventures in hedy_content.ADVENTURE_ORDER_PER_LEVEL.items():
            for adventure in default_adventures:
                db_adventures[str(lvl)].append({'name': adventure, 'from_teacher': False})
                sorted_adventure = SortedAdventure(short_name=adventure,
                                                   long_name=adventure_names.get(adventure, adventure),
                                                   is_command_adventure=adventure in hedy_content.KEYWORDS_ADVENTURES,
                                                   is_teacher_adventure=False)
                adventures[lvl].append(sorted_adventure)

        for adventure in teacher_adventures:
            available_adventures[int(adventure['level'])].append(
                {"name": adventure['id'], "from_teacher": True})

        customizations = {
            "id": class_id,
            "levels": [i for i in range(1, hedy.HEDY_MAX_LEVEL + 1)],
            "opening_dates": {},
            "other_settings": [],
            "level_thresholds": {},
            "sorted_adventures": db_adventures,
            "restored_by": user["username"],
        }

        self.db.update_class_customizations(customizations)
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/restore-adventures/level/<level>", methods=["POST"])
    @requires_teacher
    def restore_adventures_to_default(self, user, level):
        class_id = session['class_id']
        Class = self.db.get_class(class_id)

        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        customizations, adventures, adventure_names, available_adventures, _ = self.get_class_info(
            user, session['class_id'])

        teacher_adventures = list(self.db.get_teacher_adventures(user["username"]))
        second_teacher_adventures = self.db.get_second_teacher_adventures([Class], user["username"])
        teacher_adventures += second_teacher_adventures

        db_adventures = {str(i): [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
        adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
        for lvl, default_adventures in hedy_content.ADVENTURE_ORDER_PER_LEVEL.items():
            for adventure in default_adventures:
                db_adventures[str(lvl)].append({'name': adventure, 'from_teacher': False})
                sorted_adventure = SortedAdventure(short_name=adventure,
                                                   long_name=adventure_names[adventure],
                                                   is_command_adventure=adventure in hedy_content.KEYWORDS_ADVENTURES,
                                                   is_teacher_adventure=False)
                adventures[lvl].append(sorted_adventure)

        customizations['sorted_adventures'] = db_adventures
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)
        self.db.update_class_customizations(customizations)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.ADVENTURE_ORDER_PER_LEVEL,
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/restore-adventures-modal/level/<level>", methods=["GET"])
    @requires_teacher
    def get_restore_adventures_modal(self, user, level):
        Class = self.db.get_class(session['class_id'])
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        modal_text = gettext('reset_adventure_prompt')
        htmx_endpoint = f'/for-teachers/restore-adventures/level/{level}'
        htmx_target = "#adventure-dragger"
        htmx_swap = "outerHTML"
        htmx_indicator = "#indicator"
        return render_partial('modal/htmx-modal-confirm.html',
                              modal_text=modal_text,
                              htmx_endpoint=htmx_endpoint,
                              htmx_target=htmx_target,
                              htmx_swap=htmx_swap,
                              htmx_indicator=htmx_indicator)

    @route("/customize-class/<class_id>", methods=["POST"])
    @requires_teacher
    def update_customizations(self, user, class_id):
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("levels"), list):
            return "Levels must be a list", 400
        if not isinstance(body.get("other_settings"), list):
            return "Other settings must be a list", 400
        if not isinstance(body.get("opening_dates"), dict):
            return "Opening dates must be a dict", 400
        if not isinstance(body.get("level_thresholds"), dict):
            return "Level thresholds must be a dict", 400
        # Values are always strings from the front-end -> convert to numbers
        levels = [int(i) for i in body["levels"]]

        opening_dates = body["opening_dates"].copy()
        for level, timestamp in body.get("opening_dates").items():
            if len(timestamp) < 1:
                opening_dates.pop(level)
            else:
                try:
                    opening_dates[level] = utils.datetotimeordate(timestamp)
                except BaseException:
                    return "One or more of your opening dates is invalid", 400

        level_thresholds = {}
        for name, value in body.get("level_thresholds").items():
            # We only manually check for the quiz threshold, if we add more -> generalize this code
            if name == "quiz":
                try:
                    value = int(value)
                except BaseException:
                    return "Quiz threshold value is invalid", 400
                if value < 0 or value > 100:
                    return "Quiz threshold value is invalid", 400
            level_thresholds[name] = value

        customizations = self.db.get_class_customizations(class_id)
        dashboard = customizations.get('dashboard_customization', {})
        live_statistics_levels = dashboard.get('selected_levels', [1])

        customizations = {
            "id": class_id,
            "levels": levels,
            "opening_dates": opening_dates,
            "other_settings": body["other_settings"],
            "level_thresholds": level_thresholds,
            "sorted_adventures": customizations["sorted_adventures"],
            "dashboard_customization": {
                "selected_levels": live_statistics_levels
            },
            "updated_by": user["username"]
        }

        self.db.update_class_customizations(customizations)

        achievement = self.achievements.add_single_achievement(user["username"], "my_class_my_rules")
        if achievement:
            return {"achievement": achievement, "success": gettext("class_customize_success")}, 200
        return {"success": gettext("class_customize_success")}, 200

    @route("/create-accounts/<class_id>", methods=["GET"])
    @requires_teacher
    def create_accounts(self, user, class_id):
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=403, ui_message=gettext("no_such_class"))

        return render_template("create-accounts.html", current_class=Class)

    @route("/create-accounts", methods=["POST"])
    @requires_teacher
    def store_accounts(self, user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("accounts"), list):
            return "accounts should be a list!", 400

        if len(body.get("accounts", [])) < 1:
            return gettext("no_accounts"), 400

        usernames = []

        # Validation for correct types and duplicates
        for account in body.get("accounts", []):
            validation = validate_student_signup_data(account)
            if validation:
                return validation, 400
            if account.get("username").strip().lower() in usernames:
                return {"error": gettext("unique_usernames"), "value": account.get("username")}, 200
            usernames.append(account.get("username").strip().lower())

        # Validation for duplicates in the db
        classes = self.db.get_teacher_classes(user["username"], False)
        for account in body.get("accounts", []):
            if account.get("class") and account["class"] not in [i.get("name") for i in classes]:
                return "not your class", 404
            if self.db.user_by_username(account.get("username").strip().lower()):
                return {"error": gettext("usernames_exist"), "value": account.get("username").strip().lower()}, 200

        # the following is due to the fact that the current user may be a second user.
        teacher = classes[0].get("teacher") if len(classes) else user["username"]
        # Now -> actually store the users in the db
        for account in body.get("accounts", []):
            # Set the current teacher language and keyword language as new account language
            account["language"] = g.lang
            account["keyword_language"] = g.keyword_lang
            store_new_student_account(self.db, account, teacher)
            if account.get("class"):
                class_id = [i.get("id") for i in classes if i.get("name") == account.get("class")][0]
                self.db.add_student_to_class(class_id, account.get("username").strip().lower())
        return {"success": gettext("accounts_created")}, 200

    @route("/customize-adventure/view/<adventure_id>", methods=["GET"])
    @requires_login
    def view_adventure(self, user, adventure_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_adventure_error"))
        adventure = self.db.get_adventure(adventure_id)
        if not adventure:
            return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))
        if adventure["creator"] != user["username"] and not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_adventure_error"))

        # Add level to the <pre> tag to let syntax highlighting know which highlighting we need!
        adventure["content"] = adventure["content"].replace(
            "<pre>", "<pre class='no-copy-button' level='" + str(adventure["level"]) + "'>"
        )
        adventure["content"] = safe_format(adventure["content"], **hedy_content.KEYWORDS.get(g.keyword_lang))

        return render_template(
            "view-adventure.html",
            adventure=adventure,
            page_title=gettext("title_view-adventure"),
            current_page="for-teachers",
        )

    @route("/customize-adventure/<adventure_id>", methods=["GET"])
    @requires_teacher
    def get_adventure_info(self, user, adventure_id):
        if not adventure_id:
            return gettext("adventure_empty"), 400
        if not isinstance(adventure_id, str):
            return gettext("adventure_name_invalid"), 400

        adventure = self.db.get_adventure(adventure_id)
        if adventure["creator"] != user["username"] and not is_teacher(user):
            return utils.error_page(error=403, ui_message=gettext("retrieve_adventure_error"))
        # Now it gets a bit complex, we want to get the teacher classes as well as the customizations
        # This is a quite expensive retrieval, but we should be fine as this page is not called often
        # We only need the name, id and if it already has the adventure set as data to the front-end
        Classes = self.db.get_teacher_classes(user["username"])
        class_data = []
        for Class in Classes:
            customizations = self.db.get_class_customizations(Class.get("id"))
            for level in adventure.get("levels", []):
                # TODO: change name to id in sorted_adventures (probably it's only teachers' adventures!)
                if customizations and any(adv for adv in customizations.get("sorted_adventures", {}).get(level)
                                          if adv.get("name") == adventure.get("id")):
                    temp = {"name": Class.get("name"), "id": Class.get("id"),
                            "teacher": Class.get("teacher"), "students": Class.get("students", []),
                            "date": Class.get("date")}
                    class_data.append(temp)
                    break

        return render_template(
            "customize-adventure.html",
            page_title=gettext("title_customize-adventure"),
            adventure=adventure,
            adventure_classes=class_data,
            username=user["username"],
            max_level=hedy.HEDY_MAX_LEVEL,
            current_page="for-teachers",
            # TODO: update tags to be {name, canEdit} where canEdit is true if currentUser is the creator.
            adventure_tags=adventure.get("tags", []),
            js=dict(
                content=adventure.get("content"),
                lang=g.lang,
            )
        )

    @route("/customize-adventure", methods=["POST"])
    @requires_teacher
    def update_adventure(self, user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("id"), str):
            return gettext("adventure_id_invalid"), 400
        if not isinstance(body.get("name"), str):
            return gettext("adventure_name_invalid"), 400
        if not isinstance(body.get("levels"), list) or (isinstance(body.get("levels"), list) and not body["levels"]):
            return gettext("level_invalid"), 400
        if not isinstance(body.get("content"), str):
            return gettext("content_invalid"), 400
        if len(body.get("content")) < 20:
            return gettext("adventure_length"), 400
        if not isinstance(body.get("public"), bool) and not isinstance(body.get("public"), int):
            return gettext("public_invalid"), 400
        if not isinstance(body.get("language"), str) or body.get("language") not in hedy_content.ALL_LANGUAGES.keys():
            # we're incrementally integrating language into adventures; i.e., not all adventures have a language field.
            body["language"] = g.lang
            # return gettext("language_invalid"), 400

        current_adventure = self.db.get_adventure(body["id"])
        if not current_adventure:
            return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))
        # TODO: instead of not allowing the teacher, let them update the adventure in their relevant classes only.
        elif current_adventure["creator"] != user["username"]:
            return gettext("unauthorized"), 403

        adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in adventures:
            if adventure["name"] == body["name"] and adventure["id"] != body["id"]:
                return gettext("adventure_duplicate"), 400

        # We want to make sure the adventure is valid and only contains correct placeholders
        # Try to parse with our current language, if it fails -> return an error to the user
        # NOTE: format() instead of safe_format() on purpose!
        try:
            body["content"].format(**hedy_content.KEYWORDS.get(g.keyword_lang))
        except BaseException:
            return gettext("something_went_wrong_keyword_parsing"), 400

        adventure = {
            "date": utils.timems(),
            "creator": user["username"],
            "name": body["name"],
            "level": body["levels"][0],  # TODO: this should be removed gradually.
            "levels": body["levels"],
            "content": body["content"],
            "public": 1 if body["public"] else 0,
            "language": body["language"],
        }

        self.db.update_adventure(body["id"], adventure)

        tags = self.db.read_tags(current_adventure.get("tags", []))
        for tag in tags:
            for tag_adventure in tag["tagged_in"]:
                if tag_adventure["id"] == current_adventure["id"]:
                    tag_adventure["public"] = body["public"]
                    tag_adventure["language"] = body["language"]
            self.db.update_tag(tag["id"], {"tagged_in": tag["tagged_in"]})

        return {"success": gettext("adventure_updated")}, 200

    @route("/customize-adventure/<adventure_id>", methods=["DELETE"])
    @requires_teacher
    def delete_adventure(self, user, adventure_id):
        adventure = self.db.get_adventure(adventure_id)
        if not adventure:
            return utils.error_page(error=404, ui_message=gettext("retrieve_adventure_error"))
        elif adventure["creator"] != user["username"]:
            return gettext("unauthorized"), 403

        self.db.delete_adventure(adventure_id)
        tags = self.db.read_tags(adventure.get("tags", []))
        for tag in tags:
            tagged_in = list(filter(lambda t: t["id"] != adventure_id, tag["tagged_in"]))
            if len(tag["tagged_in"]) != len(tagged_in):  # only update if this adventure was tagged.
                self.db.update_tag(tag["id"], {"tagged_in": tagged_in})
        return {}, 200

    @route("/preview-adventure", methods=["POST"])
    def parse_preview_adventure(self):
        body = request.json
        try:
            code = safe_format(body.get("code"), **hedy_content.KEYWORDS.get(g.keyword_lang))
        except BaseException:
            return gettext("something_went_wrong_keyword_parsing"), 400
        return {"code": code}, 200

    @route("/create-adventure", methods=["POST"])
    @requires_teacher
    def create_adventure(self, user):
        adventure_id = uuid.uuid4().hex
        name = "AdventureX"
        adventures = self.db.get_teacher_adventures(user["username"])

        for adventure in adventures:
            if adventure["name"] == name:
                name += 'X'
                continue

        adventure = {
            "id": adventure_id,
            "date": utils.timems(),
            "creator": user["username"],
            "name": name,
            "level": 1,
            "content": "",
            "language": g.lang,
        }
        self.db.store_adventure(adventure)
        return adventure["id"], 200


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
