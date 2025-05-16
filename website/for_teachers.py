import collections
from difflib import SequenceMatcher
import os
import re
import uuid

from bs4 import BeautifulSoup
from flask import g, make_response, request, session, url_for, redirect
from jinja_partials import render_partial
from website.flask_helpers import gettext_with_fallback as gettext
import jinja_partials

import hedy
import hedy_content
import hedyweb
import utils
from safe_format import safe_format
from datetime import date

from website.server_types import SortedAdventure
from website.flask_helpers import render_template
from website.newsletter import add_class_customized_to_subscription
from website.auth import (
    is_admin,
    is_teacher,
    is_super_teacher,
    requires_login,
    requires_teacher,
    store_new_student_account,
    prepare_user_db,
    remember_current_user,
)
from .database import Database
from .auth_pages import AuthModule
from .website_module import WebsiteModule, route
from website.frontend_types import halve_adventure_content
SLIDES = collections.defaultdict(hedy_content.NoSuchSlides)
for lang in hedy_content.ALL_LANGUAGES.keys():
    SLIDES[lang] = hedy_content.Slides(lang)


WORKBOOKS = collections.defaultdict(hedy_content.NoSuchWorkbooks)
for lang in hedy_content.ALL_LANGUAGES.keys():
    WORKBOOKS[lang] = hedy_content.Workbooks(lang)


class ForTeachersModule(WebsiteModule):
    def __init__(self, db: Database, auth: AuthModule):
        super().__init__("teachers", __name__, url_prefix="/for-teachers")
        self.db = db
        self.auth = auth

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
                    "why": adventure.get("why"),
                    "why_class": render_why_class(adventure),
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

    @route("/workbooks/<level>", methods=["GET"])
    def get_workbooks(self, level):
        try:
            level = int(level)
        except ValueError:
            return utils.error_page(error=404, ui_message="Workbook does not exist")

        workbook_for_level = WORKBOOKS[g.lang].get_workbook_for_level(level, g.lang)
        if not workbook_for_level:
            return utils.error_page(error=404, ui_message="Workbook does not exist")

        line = '_' * 30
        for exercise in workbook_for_level['exercises']:
            if exercise['type'] == 'output':
                exercise['title'] = gettext('workbook_output_question_title')
                exercise['icon'] = '💻'
                exercise['text'] = gettext('workbook_output_question_text')

                if 'answer' in exercise.keys():
                    a = len(exercise['answer'].split('\n'))
                    exercise['lines'] = [line for x in range(a)]
                else:
                    pass

            if exercise['type'] == 'circle':
                exercise['title'] = gettext('workbook_circle_question_title')
                exercise['icon'] = '◯'
                goal = exercise['goal']
                exercise['text'] = safe_format(gettext('workbook_circle_question_text'), goal=goal)

            elif exercise['type'] == 'input':
                exercise['title'] = gettext('workbook_input_question_title')
                exercise['icon'] = '🧑‍💻'
                exercise['text'] = gettext('workbook_input_question_text')

                if 'answer' in exercise.keys():
                    exercise['lines'] = [line for x in exercise['answer'].split('\n')]
                else:
                    pass

                if 'output' in exercise.keys():
                    exercise['output'] = [x for x in exercise['output'].split('\n')]
                else:
                    pass

            elif exercise['type'] == 'MC-code':
                exercise['title'] = gettext('workbook_multiple_choice_question_title')
                exercise['icon'] = '🤔'
                exercise['text'] = gettext('workbook_multiple_choice_question_text')
                # let op! op een dag willen we misschien wel ander soorten MC, dan moet
                # deze tekst anders
                if 'options' in exercise.keys():
                    exercise['options'] = '〇  ' + '  〇  '.join(exercise['options'])
                else:
                    exercise['options'] = 'NO OPTIONS GIVEN!'

            elif exercise['type'] == 'define':
                exercise['title'] = gettext('workbook_define_question_title')  # ''
                exercise['icon'] = '📖'
                word = exercise['word']
                exercise['text'] = safe_format(gettext('workbook_define_question_text'), word=word)
                exercise['lines'] = [line for x in range(int(exercise['lines']))]

            elif exercise['type'] == 'question':
                exercise['title'] = gettext('workbook_open_question_title')  # ''
                exercise['icon'] = '✍️'
                exercise['lines'] = [line for x in range(int(exercise['lines']))]

        return render_template("workbooks.html",
                               current_page="teacher-manual",
                               level=level,
                               page_title=f'Workbook {level}',
                               workbook=workbook_for_level)

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
        levels = hedy_content.deep_translate_keywords(levels, g.keyword_lang)
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
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        session['class_id'] = class_id

        students = Class.get("students", [])
        invites = self.db.get_class_invites(class_id=class_id)
        level = Class.get('last_viewed_level', 1)
        student_overview_table, _, class_adventures_formatted, \
            _, student_adventures, graph_students, students_info = self.get_grid_info(user, class_id, level)

        teacher = user if Class["teacher"] == user["username"] else self.db.user_by_username(Class["teacher"])
        second_teachers = [teacher] + Class.get("second_teachers", [])

        if utils.is_testing_request(request):
            return make_response({
                "students": graph_students,
                # TODO: remove once we deploy new redesign
                "link": Class["link"],
                "name": Class["name"],
                "id": Class["id"]
            }, 200)

        return render_template(
            "class-overview.html",
            current_page="for-teachers",
            page_title=gettext("title_class-overview"),
            invites=invites,
            level=level,
            class_info={
                "students": len(students),
                # TODO: remove once we deploy new redesign
                "link": os.getenv("BASE_URL", "") + "/hedy/l/" + Class["link"],
                "teacher": Class["teacher"],
                "second_teachers": second_teachers,
                "name": Class["name"],
                "id": Class["id"],
            },
            javascript_page_options=dict(
                page="class-overview"
            ),
            adventure_table={
                'students': student_overview_table,
                'adventures': class_adventures_formatted,
                'student_adventures': student_adventures,
                'graph_options': {
                    'level': level,
                    'graph_students': graph_students
                }
            },
            students_info=students_info
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
                    adventure_list.append({'name': adventure_names[adventure['name']], 'id': adventure['name']})
            class_adventures_formatted[key] = adventure_list

        student_adventures = {}
        graph_students = []

        students_info = {}
        for student_username in students:
            student = self.db.user_by_username(student_username)
            # Fixme: The get_quiz_stats function requires a list of ids -> doesn't work on single string
            quiz_scores = self.db.get_quiz_stats([student_username])
            # Verify if the user did finish any quiz before getting the max() of the finished levels
            finished_quizzes = any("finished" in x for x in quiz_scores)
            highest_quiz = max([x.get("level") for x in quiz_scores if x.get("finished")]) if finished_quizzes else "-"
            students_info[student_username] = {
                "last_login": student["last_login"],
                "highest_level": highest_quiz,
                "adventures_ticked": 0
            }

        for student, info in students_info.items():
            info["last_login"] = utils.localized_date_format(info.get("last_login", 0))

        for student in students:
            programs = self.db.last_level_programs_for_user(student, level)
            program_stats = self.db.get_program_stats_per_level(student, level)
            adventures_tried = 0
            number_of_errors = 0
            successful_runs = 0
            # We use the program stats to get the number of errors, and successful runs in this level
            for stat in program_stats:
                successful_runs += stat.get('successful_runs', 0)
                for key in stat:
                    if "Exception" in key:
                        number_of_errors += stat[key]

            # and we use the stored programs to get the numbers of adventures tried by the student
            # and also to populate the table
            for _, program in programs.items():
                # Old programs sometimes don't have adventures associated to them
                # So skip them
                if 'adventure_name' not in program:
                    continue
                adventures_tried += 1
                name = adventure_names.get(program['adventure_name'], program['adventure_name'])
                customized_level = class_adventures_formatted.get(str(program['level']))
                if next((adventure for adventure in customized_level if adventure["name"] == name), False)\
                        and program.get('is_modified'):
                    student_adventure_id = f"{student}-{program['adventure_name']}-{level}"
                    current_adventure = self.db.student_adventure_by_id(student_adventure_id)
                    if not current_adventure:
                        # store the adventure in case it's not in the table
                        current_adventure = self.db.store_student_adventure(
                            dict(id=f"{student_adventure_id}", ticked=False, program_id=program['id']))

                    current_program = dict(level=str(program['level']), name=name,
                                           program=program['id'], ticked=current_adventure['ticked'])

                    if current_adventure['ticked']:
                        students_info[student]['adventures_ticked'] += 1

                    student_adventures[student_adventure_id] = current_program
            graph_students.append(
                {
                    "username": student,
                    "programs": len(programs),
                    "adventures_tried": adventures_tried,
                    "number_of_errors": number_of_errors,
                    "successful_runs": successful_runs
                }
            )
        return students, class_, class_adventures_formatted, adventure_names, \
            student_adventures, graph_students, students_info

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
                    adventure_snippets.append(pre.text)

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

    @route("/check_adventure", methods=["POST"])
    @requires_login
    def check_adventure(self, user):
        level = request.args.get('level')
        student_name = request.args.get('student_name', type=str)
        adventure_name = request.args.get('adventure_name', type=str)
        program_id = request.args.get('program_id', type=str)
        student_adventure_id = f"{student_name}-{adventure_name}-{level}"
        current_adventure = self.db.student_adventure_by_id(student_adventure_id)
        if not current_adventure:
            # store the adventure in case it's not in the table
            current_adventure = self.db.store_student_adventure(
                dict(id=f"{student_adventure_id}", ticked=False, program_id=program_id))

        self.db.update_student_adventure(student_adventure_id, current_adventure['ticked'])

        return make_response({'message': 'success'})

    @route("/grid_overview/<class_id>/change_checkbox", methods=["POST"])
    @requires_login
    def change_checkbox(self, user, class_id):
        level = request.args.get("level")
        student_name = request.args.get("student", type=str)
        adventure_name = request.args.get("adventure", type=str)

        students, class_, class_adventures_formatted, adventure_names, _, _, _ = (
            self.get_grid_info(user, class_id, level)
        )

        adventure_names = {value: key for key, value in adventure_names.items()}
        student_adventure_id = f"{student_name}-{adventure_name}-{level}"
        current_adventure = self.db.student_adventure_by_id(student_adventure_id)
        if not current_adventure:
            return utils.error_page(error=404, ui_message=gettext("no_programs"))

        self.db.update_student_adventure(student_adventure_id, current_adventure["ticked"])
        (
            student_overview_table,
            class_,
            class_adventures_formatted,
            adventure_names,
            student_adventures,
            _,
            students_info,
        ) = self.get_grid_info(user, class_id, level)

        return jinja_partials.render_partial(
            "customize-grid/partial-grid-tables.html",
            level=level,
            class_info={
                "id": class_id,
                "students": students,
                "name": class_["name"],
                "link": class_["link"],
            },
            adventure_table={
                "students": student_overview_table,
                "adventures": class_adventures_formatted,
                "student_adventures": student_adventures,
                "level": level,
            },
            students_info=students_info,
        )

    @route("/class/<class_id>/remove_student_modal/<student_id>", methods=["GET"])
    @requires_teacher
    def get_remove_student_modal(self, user, class_id, student_id):
        level = request.args.get('level')
        Class = self.db.get_class(session['class_id'])
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        modal_text = gettext('remove_student_prompt')
        htmx_endpoint = f'/for-teachers/class/{class_id}/remove_student/{student_id}?level={level}'
        htmx_target = "#adventure_overview"
        hyperscript = "on htmx:afterRequest wait 150ms then hedyApp.initializeGraph()"

        return render_partial('modal/htmx-modal-confirm.html',
                              modal_text=modal_text,
                              htmx_endpoint=htmx_endpoint,
                              htmx_target=htmx_target,
                              hyperscript=hyperscript)

    @route("/class/<class_id>/remove_student/<student_id>", methods=["POST"])
    @requires_login
    def leave_class(self, user, class_id, student_id):
        # We use the level to redraw the adventure table in the level
        # the teacher was using before
        level = request.args.get('level')
        Class = self.db.get_class(class_id)
        if not Class or not (utils.can_edit_class(user, Class)):
            return make_response(gettext("ajax_error"), 400)

        self.db.remove_student_from_class(Class["id"], student_id)
        students, class_, class_adventures_formatted, \
            adventure_names, student_adventures, graph_students, students_info = self.get_grid_info(
                user, class_id, level)

        return jinja_partials.render_partial("customize-grid/partial-grid-levels.html",
                                             level=level,
                                             class_info={"id": class_id, "students": students, "name": class_["name"]},
                                             max_level=hedy.HEDY_MAX_LEVEL,
                                             class_adventures=class_adventures_formatted,
                                             adventure_names=adventure_names,
                                             student_adventures=student_adventures,
                                             adventure_table={
                                                 'students': students,
                                                 'adventures': class_adventures_formatted,
                                                 'student_adventures': student_adventures,
                                                 'graph_options': {
                                                     'level': level,
                                                     'graph_students': graph_students
                                                 }
                                             },
                                             students_info=students_info
                                             )

    @route("/grid_overview/<class_id>/level", methods=["GET"])
    @requires_login
    def change_dropdown_level_class_overview(self, user, class_id):
        level = request.args.get('level')
        students, class_, class_adventures_formatted, \
            adventure_names, student_adventures, graph_students, students_info = self.get_grid_info(
                user, class_id, level)
        adventure_names = {value: key for key, value in adventure_names.items()}
        self.db.update_last_viewed_level_in_class(class_id, int(level))
        return jinja_partials.render_partial("customize-grid/partial-grid-levels.html",
                                             level=level,
                                             class_info={"id": class_id, "students": students, "name": class_["name"]},
                                             max_level=hedy.HEDY_MAX_LEVEL,
                                             class_adventures=class_adventures_formatted,
                                             adventure_names=adventure_names,
                                             student_adventures=student_adventures,
                                             adventure_table={
                                                 'students': students,
                                                 'adventures': class_adventures_formatted,
                                                 'student_adventures': student_adventures,
                                                 'graph_options': {
                                                     'level': level,
                                                     'graph_students': graph_students
                                                 }
                                             },
                                             students_info=students_info
                                             )

    @route("/get_student_programs/<student>", methods=["GET"])
    @requires_teacher
    def show_students_programs(self, user, student):
        result = self.db.programs_for_user(student)

        if hedy_content.Adventures(g.lang).has_adventures():
            adventures = hedy_content.Adventures(g.lang).get_adventure_keyname_name_levels()
        else:
            adventures = hedy_content.Adventures("en").get_adventure_keyname_name_levels()

        adventure_names = {}
        for adv_key, adv_dic in adventures.items():
            for name, _ in adv_dic.items():
                adventure_names[adv_key] = hedy_content.get_localized_name(name, g.keyword_lang)

        teacher_adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in teacher_adventures:
            adventure_names[adventure['id']] = adventure['name']
        programs = []
        for item in result:
            date = utils.delta_timestamp(item['date'])
            # This way we only keep the first 4 lines to show as preview to the user
            preview_code = "\n".join(item['code'].split("\n")[:4])
            if item.get('is_modified', True):
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
        return jinja_partials.render_partial("incl/programs_loop.html",
                                             programs=programs,
                                             adventure_names=adventure_names,
                                             student=student
                                             )

    @route("/class/<class_id>/preview", methods=["GET"])
    @requires_login
    def preview_class_as_teacher(self, user, class_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
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
        utils.remove_class_preview()
        return redirect("/for-teachers")

    @route("/preview-teacher-mode", methods=["GET"])
    def preview_teacher_mode(self):
        id = uuid.uuid4().hex[:5]
        username = f"testteacher_{id}"
        user = self.db.user_by_username(username)
        if not user:
            user_pass = os.getenv("PREVIEW_TEACHER_MODE_PASSWORD", "")
            username, hashed, _ = prepare_user_db(username, user_pass)
            user = {
                "username": username,
                "password": hashed,
                "is_teacher": 1,
                "created": utils.timems(),
                "last_login": utils.timems(),
            }
            self.db.store_user(user)
        else:
            self.db.forget_user(username)

        session["preview_teacher_mode"] = {
            "username": username,
        }
        remember_current_user(user)
        return redirect("/for-teachers")

    @route("/exit-preview-teacher-mode", methods=["GET"])
    # Note: we explicitly do not need login here, anyone can exit preview mode
    def exit_teacher_mode(self):
        self.auth.logout()
        return redirect("/hedy")

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
            return utils.error_page(error=401, ui_message=gettext('not_teacher'))

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

        next_page_url = url_for('app.programs_page', **dict(request.args, page=result.next_page_token)
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
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        session['class_id'] = class_id
        customizations, adventures, adventure_names, available_adventures, min_level = \
            self.get_class_info(user, class_id, migrate_customizations=True)

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
            adventures_default_order=hedy_content.adventures_order_per_level(),
            current_page="for-teachers",
            min_level=min_level,
            class_id=class_id,
            javascript_page_options=dict(
                page='customize-class',
                class_id=class_id
            ))

    # Disabling the load-survey route until the survey UI is redesigned
    # Explicitly not removing the code because it should be used again after the redesign
    # @route("/load-survey/<class_id>", methods=["POST"])
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
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
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
                              adventures_default_order=hedy_content.adventures_order_per_level(),
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @staticmethod
    def reorder_adventures(adventures: list, from_sorted_adv_class=False):
        """This method ensures that the last two adventures are puzzle and quiz, if they exist."""
        quiz_adv = None
        parsons_adv = None
        for i, adv in enumerate(adventures):
            name = adv.short_name if from_sorted_adv_class else adv.get("name")
            if name == "parsons":
                parsons_adv = adv
            if name == "":
                quiz_adv = adv

        if parsons_adv:
            adventures.remove(parsons_adv)
            adventures.append(parsons_adv)
        if quiz_adv:
            adventures.remove(quiz_adv)
            adventures.append(quiz_adv)

    @route("/add-adventure/level/<level>", methods=["POST"])
    @requires_login
    def add_adventure(self, user, level):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
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
        # Always keep the last two puzzle and quize, if exist.
        self.reorder_adventures(adventures[int(level)], from_sorted_adv_class=True)
        self.reorder_adventures(customizations['sorted_adventures'][level])

        # Remove hide_quiz or hide_parsons if the added adv. is quiz or parsons
        if adventure_id == "quiz" and 'other_settings' in customizations \
                and 'hide_quiz' in customizations['other_settings']:
            customizations["other_settings"].remove("hide_quiz")
        if adventure_id == "parsons" and 'other_settings' in customizations \
                and 'hide_parsons' in customizations['other_settings']:
            customizations["other_settings"].remove("hide_parsons")

        self.db.update_class_customizations(customizations)
        add_class_customized_to_subscription(user['email'])
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.adventures_order_per_level(),
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/remove-adventure", methods=["POST"])
    @requires_login
    def remove_adventure_from_class(self, user):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
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
        add_class_customized_to_subscription(user['email'])
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.adventures_order_per_level(),
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    @route("/sort-adventures", methods=["POST"])
    @requires_login
    def sort_adventures_in_class(self, user):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
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

        # Always keep the last two puzzle and quize, if exist.
        self.reorder_adventures(adventures[int(level)], from_sorted_adv_class=True)
        self.reorder_adventures(customizations['sorted_adventures'][level])
        self.db.update_class_customizations(customizations)
        add_class_customized_to_subscription(user['email'])

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.adventures_order_per_level(),
                              available_adventures=available_adventures,
                              class_id=session['class_id'])

    def migrate_quizzes_parsons_tabs(self, customizations, parsons_hidden, quizzes_hidden):
        """If the puzzles/quizzes were not migrated yet which is possible if the teacher didn't tweak
            the class customizations, if this is the case, we need to add them if possible."""
        migrated = customizations.get("quiz_parsons_tabs_migrated")
        if not migrated and customizations.get("sorted_adventures"):
            for level, sorted_adventures in customizations["sorted_adventures"].items():
                last_two_adv_names = [adv["name"] for adv in sorted_adventures[-2:]]
                parson_in_level = "parsons" in last_two_adv_names
                quiz_in_level = "quiz" in last_two_adv_names
                # In some levels, we don't need quiz/parsons
                level_accepts_parsons = "parsons" in hedy_content.adventures_order_per_level()[int(level)]
                level_accepts_quiz = "quiz" in hedy_content.adventures_order_per_level()[int(level)]
                if not parson_in_level and not parsons_hidden and level_accepts_parsons:
                    sorted_adventures.append(
                        {"name": "parsons", "from_teacher": False})

                if not quiz_in_level and not quizzes_hidden and level_accepts_quiz:
                    sorted_adventures.append(
                        {"name": "quiz", "from_teacher": False})
                # Need to reorder, for instance, in case parsons was hidden and the other was not.
                ForTeachersModule.reorder_adventures(sorted_adventures)

            # Mark current customization as being migrated so that we don't do this step next time.
            customizations["quiz_parsons_tabs_migrated"] = 1
            self.db.update_class_customizations(customizations)

    def get_class_info(self, user, class_id, migrate_customizations=False):
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

        # START HERE
        # Check how to deal with usages of this endpoint through other endpoints

        if not utils.is_redesign_enabled():
            # Add quiz and parsons as adventure names so that we can show them as tabs.
            adventure_names["quiz"] = gettext("quiz_tab")
            adventure_names["parsons"] = gettext("parsons_title")
            default_adventures["quiz"] = {}
            default_adventures["parsons"] = {}

        if migrate_customizations:
            parsons_hidden = False
            quizzes_hidden = False
            if customizations:
                if not utils.is_redesign_enabled():
                    parsons_hidden = (
                        "other_settings" in customizations
                        and "hide_parsons" in customizations["other_settings"]
                    )
                    quizzes_hidden = (
                        "other_settings" in customizations
                        and "hide_quiz" in customizations["other_settings"]
                    )
                if quizzes_hidden:
                    del default_adventures["quiz"]
                if parsons_hidden:
                    del default_adventures["parsons"]

                # in case this class has thew new way to select adventures
                if 'sorted_adventures' in customizations:
                    # remove from customizations adventures that we have removed
                    self.purge_customizations(customizations['sorted_adventures'],
                                              default_adventures, teacher_adventures)
                # it uses the old way so convert it to the new one
                elif 'adventures' in customizations:
                    customizations['sorted_adventures'] = {str(i): [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
                    for adventure, levels in customizations['adventures'].items():
                        for level in levels:
                            customizations['sorted_adventures'][str(level)].append(
                                {"name": adventure, "from_teacher": False})

                            customizations['sorted_adventures'][str(level)].append(
                                {"name": "quiz", "from_teacher": False})
                            customizations['sorted_adventures'][str(level)].append(
                                {"name": "parsons", "from_teacher": False})
                customizations["updated_by"] = user["username"]
                self.db.update_class_customizations(customizations)
                min_level = 1 if customizations['levels'] == [] else min(customizations['levels'])
            else:
                # Since it doesn't have customizations loaded, we create a default customization object.
                # This makes further updating with HTMX easier
                adventures_to_db = {}
                for level, default_adventures in hedy_content.adventures_order_per_level().items():
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
                    "quiz_parsons_tabs_migrated": True,
                }
                self.db.update_class_customizations(customizations)
            self.migrate_quizzes_parsons_tabs(customizations, parsons_hidden, quizzes_hidden)

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

        for level, level_default_adventures in hedy_content.adventures_order_per_level().items():
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

        for lvl, default_adventures in hedy_content.adventures_order_per_level().items():
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
            "updated_by": user["username"]
        }

        self.db.update_class_customizations(customizations)
        available_adventures = self.get_unused_adventures(adventures, teacher_adventures, adventure_names)

        return render_partial('customize-class/partial-sortable-adventures.html',
                              level=level,
                              customizations=customizations,
                              adventures=adventures,
                              max_level=hedy.HEDY_MAX_LEVEL,
                              adventure_names=adventure_names,
                              adventures_default_order=hedy_content.adventures_order_per_level(),
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
        for lvl, default_adventures in hedy_content.adventures_order_per_level().items():
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
                              adventures_default_order=hedy_content.adventures_order_per_level(),
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
        htmx_target = "#adventure_dragger"
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
            return make_response(gettext("ajax_error"), 400)
        if not isinstance(body.get("levels"), list):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("other_settings"), list):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("opening_dates"), dict):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("level_thresholds"), dict):
            return make_response(gettext("request_invalid"), 400)
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
                    return make_response(gettext("request_invalid"), 400)

        level_thresholds = {}
        for name, value in body.get("level_thresholds").items():
            # We only manually check for the quiz threshold, if we add more -> generalize this code
            if name == "quiz":
                try:
                    value = int(value)
                except BaseException:
                    return make_response(gettext("request_invalid"), 400)
                if value < 0 or value > 100:
                    return make_response(gettext("request_invalid"), 400)
            level_thresholds[name] = value

        customizations = self.db.get_class_customizations(class_id)
        dashboard = customizations.get("dashboard_customization", {})
        live_statistics_levels = dashboard.get("selected_levels", [1])

        # Remove quiz and parsons if we need to hide them  all.
        hide_quiz = "hide_quiz" in body["other_settings"]
        hide_parsons = "hide_parsons" in body["other_settings"]
        for level, adventures in customizations["sorted_adventures"].items():
            if hide_parsons or hide_quiz:
                customizations["sorted_adventures"][level] = [
                    adventure
                    for adventure in adventures
                    if not (adventure["name"] == "parsons" and hide_parsons)
                    and not (adventure["name"] == "quiz" and hide_quiz)
                ]

            if (
                not hide_parsons
                and "other_settings" in customizations
                and "hide_parsons" in customizations["other_settings"]
            ):  # if so, we should toggle parsons.
                customizations["sorted_adventures"][level].append(
                    {"name": "parsons", "from_teacher": False}
                )

            if (
                not hide_quiz
                and "other_settings" in customizations
                and "hide_quiz" in customizations["other_settings"]
            ):  # if so, we should toggle quizes.
                customizations["sorted_adventures"][level].append(
                    {"name": "quiz", "from_teacher": False}
                )

        customizations = {
            "id": class_id,
            "levels": levels,
            "opening_dates": opening_dates,
            "other_settings": body["other_settings"],
            "level_thresholds": level_thresholds,
            "sorted_adventures": customizations["sorted_adventures"],
            "dashboard_customization": {"selected_levels": live_statistics_levels},
            "updated_by": user["username"],
        }

        self.db.update_class_customizations(customizations)
        add_class_customized_to_subscription(user["email"])
        response = {"success": gettext("class_customize_success")}

        return make_response(response, 200)

    @route("/create-accounts/<class_id>", methods=["GET"])
    @requires_teacher
    def create_accounts(self, user, class_id):
        Class = self.db.get_class(class_id)
        if not Class:
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))
        if not utils.can_edit_class(user, Class) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("no_such_class"))

        return render_template(
            "create-accounts.html",
            current_class=Class,
            javascript_page_options=dict(page='create-accounts'))

    @route("/create-accounts", methods=["POST"])
    @requires_teacher
    def store_accounts(self, user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return make_response(gettext("ajax_error"), 400)
        if not isinstance(body.get("class"), str):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("generate_passwords"), bool):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("accounts"), str):
            return make_response(gettext("request_invalid"), 400)

        # Validate number of accounts
        lines = [line.strip() for line in body["accounts"].split("\n") if line.strip()]
        if not lines:
            return make_response(gettext("no_accounts"), 400)
        elif len(lines) > 100:
            return make_response(gettext('too_many_accounts'), 400)

        separator = ';'
        if body["generate_passwords"]:
            # If usernames contain a separator, probably the user forgot to check the auto-generate passwords
            usernames_with_separator = [usr for usr in lines if separator in usr]
            if usernames_with_separator:
                err = safe_format(gettext('username_contains_separator'), usernames=', '.join(usernames_with_separator))
                return make_response({"error": err}, 400)

            # Currently usernames cannot contain '@' and ':'
            invalid_symbols_in_username = ['@', ':']
            invalid_usernames = [usr for usr in lines if any(sym in usr for sym in invalid_symbols_in_username)]
            if invalid_usernames:
                err = safe_format(gettext('username_contains_invalid_symbol'),
                                  usernames=', '.join(invalid_usernames))
                return make_response({"error": err}, 400)

            accounts = [(user.lower(), utils.random_password_generator()) for user in lines]
        else:

            accounts, incorrect_lines = self._extract_account_info(lines, separator)
            if incorrect_lines:
                # If lines don't have separators, probably the user forgot to uncheck the auto-generate passwords
                if all([separator not in line for line in incorrect_lines]):
                    err = safe_format(gettext('all_rows_missing_separator'), rows=', '.join(incorrect_lines))
                    return make_response({"error": err}, 400)
                else:
                    # If only some lines don't have separators, then the user made an error somewhere
                    err = safe_format(gettext('some_rows_missing_separator'), rows=', '.join(incorrect_lines))
                    return make_response({"error": err}, 400)

            # Validate passwords length
            invalid_passwords = [pwd for (_, pwd) in accounts if len(pwd) < 6]
            if invalid_passwords:
                err = safe_format(gettext('passwords_too_short'), passwords=', '.join(invalid_passwords))
                return make_response({"error": err}, 400)

        # Validate usernames length
        invalid_usernames = [usr for (usr, _) in accounts if len(usr) < 3]
        if invalid_usernames:
            err = safe_format(gettext('usernames_too_short'), usernames=', '.join(invalid_usernames))
            return make_response({"error": err}, 400)

        # Validate that the user supplied no duplicate usernames
        usernames = [usr for (usr, _) in accounts]
        duplicates_in_input = [usr for usr in usernames if usernames.count(usr) > 1]
        if duplicates_in_input:
            err = safe_format(gettext('provided_username_duplicates'),
                              usernames=', '.join(list(set(duplicates_in_input))))
            return make_response({"error": err}, 400)

        # Validate that the usernames do not exist in the db
        duplicates_in_db = [usr for (usr, _) in accounts if self.db.user_by_username(usr)]
        if duplicates_in_db:
            err = safe_format(gettext('usernames_unavailable'), usernames=', '.join(duplicates_in_db))
            return make_response({"error": err}, 400)

        # Validate the class
        classes = self.db.get_teacher_classes(user["username"], False)
        classes = [c for c in classes if c["id"] == body["class"]]
        if not classes:
            return make_response(gettext("request_invalid"), 404)
        # Note that the teacher creating the account might be a second teacher for the class
        # In this case, we link the student account to the main teacher
        class_ = classes[0]
        teacher = class_.get("teacher")

        # Now, actually store the users in the db
        for usr, pwd in accounts:
            # Set the current teacher language and keyword language as new account language
            user = {'username': usr, 'password': pwd, 'language': g.lang, 'keyword_language': g.keyword_lang}
            store_new_student_account(self.db, user, teacher)
            self.db.add_student_to_class(body["class"], usr)
        response = {"accounts": [{"username": usr, "password": pwd} for usr, pwd in accounts]}
        return make_response(response, 200)

    @staticmethod
    def _extract_account_info(lines, separator):
        correct_lines: list[tuple[str, str]] = []
        incorrect_lines = []
        for line in lines:
            account = line.split(separator)
            if len(account) < 2:
                incorrect_lines.append(line)
            else:
                usr = account[0].strip()
                pwd = separator.join(account[1:]).strip()
                if not usr or not pwd:
                    incorrect_lines.append(line)
                else:
                    correct_lines.append((usr.lower(), pwd))
        return correct_lines, incorrect_lines

    @route("/customize-adventure/view/<adventure_id>", methods=["GET"])
    @requires_login
    def view_adventure(self, user, adventure_id):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_adventure_error"))
        adventure = self.db.get_adventure(adventure_id)
        if not adventure:
            return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))
        if adventure["creator"] != user["username"] and not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_adventure_error"))

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

    @staticmethod
    def create_basic_adventure(user, adventure_id=None):
        if not adventure_id:
            adventure_id = uuid.uuid4().hex
        return {
            "id": adventure_id,
            "date": utils.timems(),
            "creator": user["username"],
            "name": "",
            "classes": [],
            "levels": [],
            "content": "",
            "public": 0,
            "language": g.lang,
        }

    @route("/customize-adventure", methods=["GET"])
    @requires_teacher
    def get_new_adventure(self, user):
        class_id = request.args.get("class_id")
        level = request.args.get("level")

        adventure_id = uuid.uuid4().hex
        adventure = self.create_basic_adventure(user, adventure_id)

        if level:
            adventure["level"] = int(level)
            adventure["levels"] = [level]

        if class_id:
            session['class_id'] = class_id
            adventure["classes"] = [class_id]

        session["new_adventure"] = adventure
        return redirect(f"/for-teachers/customize-adventure/{adventure['id']}?new_adventure=1")

    @route("/customize-adventure/<adventure_id>", methods=["GET"])
    @requires_teacher
    def get_adventure_info(self, user, adventure_id,):
        if not adventure_id:
            return make_response(gettext("adventure_empty"), 400)
        if not isinstance(adventure_id, str):
            return make_response(gettext("adventure_name_invalid"), 400)

        adventure = self.db.get_adventure(adventure_id)
        if not adventure and request.args.get("new_adventure"):
            adventure = session.get("new_adventure", self.create_basic_adventure(user, adventure_id))

        if not adventure:
            return utils.error_page(error=404, ui_message=gettext("retrieve_adventure_error"))
        if adventure["creator"] != user["username"] and not is_teacher(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_adventure_error"))

        adventure['content'] = safe_format(adventure['content'],
                                           **hedy_content.KEYWORDS.get(g.keyword_lang))
        adventure['solution_example'] = safe_format(adventure.get('solution_example', ''),
                                                    **hedy_content.KEYWORDS.get(g.keyword_lang))

        # We don't change adventure["content"] because it's used in the editor, while this is for previwing only.
        preview_content, adventure["example_code"] = halve_adventure_content(adventure["content"])

        # Now it gets a bit complex, we want to get the teacher classes as well as the customizations
        # This is a quite expensive retrieval, but we should be fine as this page is not called often
        # We only need the name, id and if it already has the adventure set as data to the front-end
        Classes = self.db.get_teacher_classes(user["username"])
        class_data = []
        for Class in Classes:
            customizations = self.db.get_class_customizations(Class.get("id"))
            for level in adventure.get("levels", []):
                # TODO: change name to id in sorted_adventures (probably it's only teachers' adventures!)
                if customizations and customizations.get("sorted_adventures") and \
                    any(adv for adv in customizations.get("sorted_adventures", {}).get(level, [])
                        if adv.get("name") == adventure.get("id")):
                    temp = {"name": Class.get("name"), "id": Class.get("id"),
                            "teacher": Class.get("teacher"), "students": Class.get("students", []),
                            "date": Class.get("date"), "classes": Class.get("classes")}
                    class_data.append(temp)
                    # Class["from_teacher"] = True
                    break

        return render_template(
            "customize-adventure.html",
            page_title=gettext("title_customize-adventure"),
            adventure=adventure,
            adventure_classes=class_data,
            all_classes=Classes,
            username=user["username"],
            max_level=hedy.HEDY_MAX_LEVEL,
            # TODO: update tags to be {name, canEdit} where canEdit is true if currentUser is the creator.
            adventure_tags=adventure.get("tags", []),
            level=adventure.get("level", ""),
            content=preview_content,
            js=dict(
                content=adventure.get("content"),
                lang=g.lang,
            ),
            javascript_page_options=dict(
                page='customize-adventure',
                lang=g.lang,
                level=adventure.get("level", ""),
                adventures=[adventure],
                initial_tab='',
                current_user_name=user['username'],
            )
        )

    @route("/customize-adventure", methods=["POST"])
    @requires_teacher
    def update_adventure(self, user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return make_response(gettext("ajax_error"), 400)
        if not isinstance(body.get("id"), str):
            return make_response(gettext("adventure_id_invalid"), 400)
        if not isinstance(body.get("name"), str):
            return make_response(gettext("adventure_name_invalid"), 400)
        if not isinstance(body.get("levels"), list) or (isinstance(body.get("levels"), list) and not body["levels"]):
            return make_response(gettext("level_invalid"), 400)
        if not isinstance(body.get("content"), str):
            return make_response(gettext("content_invalid"), 400)
        if len(body.get("content")) < 20:
            return make_response(gettext("adventure_length"), 400)
        if not isinstance(body.get("public"), bool) and not isinstance(body.get("public"), int):
            return make_response(gettext("public_invalid"), 400)
        if 'formatted_content' in body and not isinstance(body.get("formatted_content"), str):
            return make_response(gettext("content_invalid"), 400)
        if not isinstance(body.get("language"), str) or body.get("language") not in hedy_content.ALL_LANGUAGES.keys():
            # we're incrementally integrating language into adventures; i.e., not all adventures have a language field.
            body["language"] = g.lang
            # return gettext("language_invalid"), 400

        current_adventure = self.db.get_adventure(body["id"])
        if not current_adventure:
            current_adventure = session.get("new_adventure", self.create_basic_adventure(user, body["id"]))

        # TODO: instead of not allowing the teacher, let them update the adventure in their relevant classes only.
        elif current_adventure["creator"] != user["username"]:
            return make_response(gettext("unauthorized"), 401)
        current_classes = {}
        if body.get("classes"):
            current_classes = current_adventure.get('classes', [])
        current_levels = []
        if not current_adventure.get('level'):
            current_levels = current_adventure.get('levels', [])

        adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in adventures:
            if adventure["name"] == body["name"] and adventure["id"] != body["id"]:
                return make_response(gettext("adventure_duplicate"), 400)

        # We want to make sure the adventure is valid and only contains correct placeholders
        # Try to parse with our current language, if it fails -> return an error to the user
        # NOTE: format() instead of safe_format() on purpose!
        try:
            body['content'].format(**hedy_content.KEYWORDS.get(g.keyword_lang))
            if 'formatted_solution_code' in body:
                body['formatted_solution_code'].format(**hedy_content.KEYWORDS.get(g.keyword_lang))
        except BaseException:
            return make_response(gettext("something_went_wrong_keyword_parsing"), 400)

        adventure = {
            "date": utils.timems(),
            "creator": user["username"],
            "name": body["name"],
            "classes": body["classes"],
            "level": int(body["levels"][0]),  # TODO: this should be removed gradually.
            "levels": body["levels"],
            "public": 1 if body["public"] else 0,
            "language": body["language"],
            "content": body["content"],
            "solution_example": body.get("formatted_solution_code"),
        }

        self.db.update_adventure(body["id"], adventure)

        tags = self.db.read_tags(current_adventure.get("tags", []))
        for tag in tags:
            for tag_adventure in tag["tagged_in"]:
                if tag_adventure["id"] == current_adventure["id"]:
                    tag_adventure["public"] = body["public"]
                    tag_adventure["language"] = body["language"]
            self.db.update_tag(tag["id"], {"tagged_in": tag["tagged_in"]})

        if current_levels and current_classes:
            for old_class in current_classes:
                for level in current_levels:
                    if old_class not in body["classes"] or level not in body["levels"]:
                        self.add_adventure_to_class_level(user, old_class, body["id"], level, True)

        for class_id in body["classes"]:
            for level in body["levels"]:
                if level not in current_levels and class_id in current_classes:
                    self.add_adventure_to_class_level(user, class_id, body["id"], level, False)
                elif class_id not in current_classes:
                    self.add_adventure_to_class_level(user, class_id, body["id"], level, False)

        return make_response({"success": gettext("adventure_updated")}, 200)

    @route("/customize-adventure/<adventure_id>", methods=["DELETE"])
    @route("/customize-adventure/<adventure_id>/<owner>", methods=["DELETE"])
    @requires_teacher
    def delete_adventure(self, user, adventure_id, owner=None):
        adventure = self.db.get_adventure(adventure_id)
        if not adventure:
            return utils.error_page(error=404, ui_message=gettext("retrieve_adventure_error"))
        elif adventure["creator"] != user["username"]:
            # in case the current user is a super teacher, they may delete any adventure.
            if not (is_super_teacher(user) and adventure["creator"] == owner):
                return make_response(gettext("unauthorized"), 401)

        self.db.delete_adventure(adventure_id)
        tags = self.db.read_tags(adventure.get("tags", []))
        for tag in tags:
            tagged_in = list(filter(lambda t: t["id"] != adventure_id, tag["tagged_in"]))
            if len(tag["tagged_in"]) != len(tagged_in):  # only update if this adventure was tagged.
                self.db.update_tag(tag["id"], {"tagged_in": tagged_in})

        teacher_classes = self.db.get_teacher_classes(user["username"], True)
        adventures = []
        teacher_adventures = self.db.get_teacher_adventures(user["username"])
        # Get the adventures that are created by my second teachers. This may be confusing to people so
        # annotate the adventures.
        second_teacher_adventures = self.db.get_second_teacher_adventures(teacher_classes, user["username"])
        for adventure in list(teacher_adventures) + second_teacher_adventures:
            adventures.append(
                {
                    "id": adventure.get("id"),
                    "name": adventure.get("name"),
                    "creator": adventure.get("creator"),
                    "author": adventure.get("author"),
                    "date": utils.localized_date_format(adventure.get("date")),
                    "level": adventure.get("level", ""),
                    "levels": adventure.get("levels"),
                    "why": adventure.get("why"),
                    "why_class": render_why_class(adventure),
                }
            )
        return render_partial('htmx-adventures-table.html', teacher_adventures=teacher_adventures)

    @route("/preview-adventure", methods=["POST"])
    def parse_preview_adventure(self):
        body = request.json
        try:
            code = safe_format(body.get("code"), **hedy_content.KEYWORDS.get(g.keyword_lang))
        except BaseException:
            return make_response(gettext("something_went_wrong_keyword_parsing"), 400)
        return make_response({"code": code}, 200)

    def add_adventure_to_class_level(self, user, class_id, adventure_id, level, remove_adv):
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and not is_admin(user)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        customizations, _, _, _, _ = self.get_class_info(
            user, class_id, migrate_customizations=True)

        is_teacher_adventure = True

        if not remove_adv and any(adventure['name'] == adventure_id
                                  for adventure in customizations['sorted_adventures'][level]):
            return
        if not remove_adv:
            customizations['sorted_adventures'][level].append(
                {'name': adventure_id, 'from_teacher': is_teacher_adventure})
        elif {'name': adventure_id, 'from_teacher': is_teacher_adventure} in customizations['sorted_adventures'][level]:
            customizations['sorted_adventures'][level].remove(
                {'name': adventure_id, 'from_teacher': is_teacher_adventure})

        self.reorder_adventures(customizations['sorted_adventures'][level])
        self.db.update_class_customizations(customizations)
        add_class_customized_to_subscription(user['email'])

    @route("/create-adventure/", methods=["POST"])
    @route("/create-adventure/<class_id>", methods=["POST"])
    @route("/create-adventure/<class_id>/<level>", methods=["POST"])
    @requires_teacher
    def create_adventure(self, user, class_id=None, level=None):
        if not is_teacher(user) and not is_admin(user):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))

        adventure_id = uuid.uuid4().hex
        name = "AdventureX"
        adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in adventures:
            if adventure["name"] == name:
                name += 'X'
                continue

        if not level:
            level = "1"

        session['class_id'] = class_id
        adventure = {
            "id": adventure_id,
            "date": utils.timems(),
            "creator": user["username"],
            "name": name,
            "classes": [class_id] if class_id is not None else [],
            "level": int(level),
            "levels": [level],
            "content": "",
            "public": 0,
            "language": g.lang,
        }
        self.db.store_adventure(adventure)
        if class_id:
            self.add_adventure_to_class_level(user, class_id, adventure_id, str(level), False)

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
    for lvl, adventures in hedy_content.adventures_order_per_level().items():
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


def render_why_class(adventure):
    return safe_format(
        gettext('see_adventure_shared_class'),
        class_name=adventure.get("why_class"),
        creator=adventure.get('creator'))
