import copy
import uuid
from typing import Optional

from flask import g, make_response, request
from website.flask_helpers import gettext_with_fallback as gettext
import jinja_partials
import hedy_content

import hedy
import utils
from config import config
from website.auth import (
    current_user,
    email_base_url,
    is_admin,
    requires_login,
    requires_teacher,
    send_email,
)

from .database import Database
from .for_teachers import ForTeachersModule
from .website_module import WebsiteModule, route
from .frontend_types import SaveInfo, Program
from . import querylog


class ProgramsLogic:
    """Logic for storing/saving programs.

    This used to be inside the class below, which also handles flask
    routes, and is being extracted out piece by piece.

    This could maybe have been in the Database class, but it also uses
    Achievements and stuff.
    """

    def __init__(self, db: Database, for_teachers: ForTeachersModule):
        self.db = db
        self.for_teachers = for_teachers

    @querylog.timed
    def store_user_program(self,
                           user,
                           level: int,
                           name: str,
                           code: str,
                           error: bool,
                           program_id: Optional[str] = None,
                           adventure_name: Optional[str] = None,
                           short_name: Optional[str] = None,
                           set_public: Optional[bool] = None):
        """Store a user program (either new or overwrite an existing one).

        Returns the program record.
        """

        # Some user input and a bunch of metadata
        updates = {
            "session": utils.session_id(),
            "date": utils.timems(),
            "lang": g.lang,
            "version": utils.version(),
            "level": level,
            "code": code,
            "name": name,
            "username": user["username"],
            "error": error,
            "adventure_name": adventure_name,
        }

        if set_public is not None:
            updates['public'] = 1 if set_public else 0

        if program_id:
            # Updates an existing program
            # FIXME: This should turn into a conditional update
            current_prog = self.db.program_by_id(program_id)
            if not current_prog:
                raise RuntimeError(f'No program with id: {program_id}')
            if current_prog['username'] != updates['username']:
                raise NotYourProgramError('Cannot overwrite other user\'s program')

            program = self.db.update_program(program_id, updates)
        else:
            # Creates a new program
            updates['id'] = uuid.uuid4().hex
            program = self.db.store_program(updates)

        # update if a program is modified or not, this can only be done after a program is stored
        # because is_program_modified needs a program
        full_adventures = hedy_content.Adventures("en").get_adventures(g.keyword_lang)
        teacher_adventures = self.db.get_teacher_adventures(current_user()["username"])
        program_to_check = copy.deepcopy(program)
        program_to_check['adventure_name'] = short_name

        is_modified = self.for_teachers.is_program_modified(program_to_check, full_adventures, teacher_adventures)
        # a program can be saved already but not yet modified,
        # and if it was already modified and now is so again, count should not increase.
        if is_modified and not program.get('is_modified'):
            self.db.increase_user_program_count(user["username"])
        program = self.db.update_program(program['id'], {'is_modified': is_modified})

        querylog.log_value(program_id=program['id'],
                           adventure_name=adventure_name, error=error, code_lines=len(code.split('\n')))

        return program


class ProgramsModule(WebsiteModule):
    """Flask routes that deal with manipulating programs."""

    def __init__(self, db: Database, for_teachers: ForTeachersModule):
        super().__init__("programs", __name__, url_prefix="/programs")
        self.logic = ProgramsLogic(db, for_teachers)
        self.db = db

    @route("/list", methods=["GET"])
    @requires_login
    def list_programs(self, user):
        # Filter by level, adventure, submitted, paginated.
        return make_response({"programs": self.db.programs_for_user(user["username"]).records})

    @route("/delete/", methods=["POST"])
    @requires_login
    def delete_program(self, user):
        body = request.json
        if not isinstance(body.get("id"), str):
            return make_response(gettext("request_invalid"), 400)

        result = self.db.program_by_id(body["id"])

        if not result or (result["username"] != user["username"] and not is_admin(user)):
            return make_response(gettext("request_invalid"), 404)
        self.db.delete_program_by_id(body["id"])
        self.db.increase_user_program_count(user["username"], -1)

        # This only happens in the situation were a user deletes their favourite program -> Delete from public profile
        public_profile = self.db.get_public_profile_settings(current_user()["username"])
        if (
            public_profile
            and "favourite_program" in public_profile
            and public_profile["favourite_program"] == body["id"]
        ):
            self.db.set_favourite_program(user["username"], body["id"], None)

        resp = {"message": gettext("delete_success")}
        return make_response(resp, 200)

    @route("/duplicate-check", methods=["POST"])
    def check_duplicate_program(self):
        body = request.json
        if not isinstance(body, dict):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("name"), str):
            return make_response(gettext("request_invalid"), 400)

        if not current_user()["username"]:
            return make_response(gettext("save_prompt"), 403)

        programs = self.db.programs_for_user(current_user()["username"])
        for program in programs:
            if program["name"] == body["name"]:
                return make_response({"duplicate": True, "message": gettext("overwrite_warning")})
        return make_response({"duplicate": False}, 200)

    @route("/", methods=["POST"])
    @requires_login
    def save_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("code"), str):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("name"), str):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("level"), int):
            return make_response(gettext("request_invalid"), 400)
        if 'program_id' in body and not isinstance(body.get("program_id"), str):
            return make_response(gettext("request_invalid"), 400)
        if 'shared' in body and not isinstance(body.get("shared"), bool):
            return make_response(gettext("request_invalid"), 400)
        if "adventure_name" in body:
            if not isinstance(body.get("adventure_name"), str):
                return make_response(gettext("request_invalid"), 400)

        error = None
        program_id = body.get('program_id')

        # We don't NEED to pass this in, but it saves the database a lookup if we do.
        program_public = body.get("shared")

        if program_public:
            # If a program is marked as public, we need to know whether it contains
            # an error or not. Parse it here and add the status.
            # WARNING: compiling is expensive! We may regret doing this on every save, especially
            # when saves become common!
            try:
                hedy.transpile(body.get("code"), body.get("level"), g.lang)
                error = False
            except BaseException:
                error = True
                if not body.get("force_save", True):
                    return make_response({"parse_error": True, "message": gettext("save_parse_warning")})

        program = self.logic.store_user_program(
            program_id=program_id,
            level=body['level'],
            code=body['code'],
            name=body['name'],
            user=user,
            error=error,
            set_public=program_public,
            adventure_name=body.get('adventure_name'),
            short_name=body.get('short_name', body.get('adventure_name')))

        return make_response({
            "message": gettext("save_success_detail"),
            "share_message": gettext("copy_clipboard"),
            "name": program["name"],
            "id": program['id'],
            "save_info": SaveInfo.from_program(Program.from_database_row(program))
        }, 200)

    @route("/share/<program_id>", methods=['POST'], defaults={'second_teachers_programs': False})
    @route("/share/<program_id>/<second_teachers_programs>", methods=["POST"])
    @requires_login
    def share_unshare_program(self, user, program_id, second_teachers_programs):
        program = self.db.program_by_id(program_id)
        if not program or program["username"] != user["username"]:
            return make_response(gettext("request_invalid"), 404)

        # This only happens in the situation were a user un-shares their favourite program -> Delete from public profile
        public_profile = self.db.get_public_profile_settings(current_user()["username"])
        if (
            public_profile
            and "favourite_program" in public_profile
            and public_profile["favourite_program"] == program_id
        ):
            self.db.set_favourite_program(user["username"], program_id, None)

        if program.get("public"):
            public = 0
        else:
            public = 1
        program = self.db.set_program_public_by_id(program_id, public)

        keyword_lang = g.keyword_lang
        adventure_names = hedy_content.Adventures(g.lang).get_adventure_names(keyword_lang)
        program["date"] = utils.delta_timestamp(program["date"])
        program["preview_code"] = "\n".join(program["code"].split("\n")[:4])
        program["number_lines"] = program["code"].count('\n') + 1
        return jinja_partials.render_partial('htmx-program.html',
                                             program=program,
                                             adventure_names=adventure_names,
                                             public_profile=public_profile,
                                             second_teachers_programs=second_teachers_programs == 'True')

    @route("/submit", methods=["POST"])
    @requires_login
    def submit_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("id"), str):
            return make_response(gettext("request_invalid"), 400)

        result = self.db.program_by_id(body["id"])
        if not result or result["username"] != user["username"]:
            return make_response(gettext("request_invalid"), 400)

        program = self.db.submit_program_by_id(body["id"], True)
        self.db.increase_user_submit_count(user["username"])

        response = {
            "message": gettext("submitted"),
            "save_info": SaveInfo.from_program(Program.from_database_row(program))
        }
        return make_response(response, 200)

    @route("/unsubmit", methods=["POST"])
    @requires_teacher
    def unsubmit_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("id"), str):
            return make_response(gettext("request_invalid"), 400)

        result = self.db.program_by_id(body["id"])
        if not result:
            return make_response(gettext("request_invalid"), 400)

        program = self.db.submit_program_by_id(body["id"], False)

        response = {
            "message": gettext("unsubmitted"),
            "save_info": SaveInfo.from_program(Program.from_database_row(program))
        }
        return make_response(response, 200)

    @route("/set_favourite", methods=["POST"])
    @requires_login
    def set_favourite_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("id"), str):
            return make_response(gettext("request_invalid"), 400)
        if not isinstance(body.get("set"), bool):
            return make_response(gettext("request_invalid"), 400)

        result = self.db.program_by_id(body["id"])
        if not result or result["username"] != user["username"]:
            return make_response(gettext("request_invalid"), 400)

        if self.db.set_favourite_program(user["username"], body["id"], body["set"]):
            message = gettext("favourite_success") if body["set"] else gettext("unfavourite_success")
            return make_response({"message": message}, 200)
        else:
            return make_response(gettext("request_invalid"), 400)

    @route("/report", methods=["POST"])
    @requires_login
    def report_program(self, user):
        body = request.json

        # Make sure the program actually exists and is public
        program = self.db.program_by_id(body.get("id"))
        if not program or program.get("public") != 1:
            return make_response(gettext("report_failure"), 400)

        link = email_base_url() + "/hedy/" + body.get("id") + "/view"
        send_email(
            config["email"]["sender"],
            "The following program is reported by " + user["username"],
            link,
            '<a href="' + link + '">Program link</a>',
        )

        return make_response({"message": gettext("report_success")}, 200)


class NotYourProgramError(RuntimeError):
    pass
