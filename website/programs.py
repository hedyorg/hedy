import copy
import uuid
from typing import Optional

from flask import g, request, jsonify
from flask_babel import gettext
import jinja_partials
import hedy_content

import hedy
import utils
from config import config
from website.auth import (
    current_user,
    email_base_url,
    is_admin,
    requires_admin,
    requires_login,
    requires_teacher,
    send_email,
)

from .achievements import Achievements
from .database import Database
from .statistics import StatisticsModule
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

    def __init__(self, db: Database, achievements: Achievements, statistics: StatisticsModule):
        self.db = db
        self.achievements = achievements
        self.statistics = statistics

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
            # FIXME: This should turn into a conditional update
            current_prog = self.db.program_by_id(program_id)
            if not current_prog:
                raise RuntimeError(f'No program with id: {program_id}')
            if current_prog['username'] != updates['username']:
                raise NotYourProgramError('Cannot overwrite other user\'s program')

            program = self.db.update_program(program_id, updates)
        else:
            updates['id'] = uuid.uuid4().hex
            program = self.db.store_program(updates)

        # update if a program is modified or not, this can only be done after a program is stored
        # because is_program_modified needs a program
        full_adventures = hedy_content.Adventures("en").get_adventures(g.keyword_lang)
        teacher_adventures = self.db.get_teacher_adventures(current_user()["username"])
        program_to_check = copy.deepcopy(program)
        program_to_check['adventure_name'] = short_name

        is_modified = self.statistics.is_program_modified(program_to_check, full_adventures, teacher_adventures)
        # a program can be saved already but not yet modified,
        # and if it was already modified and now is so again, count should not increase.
        if is_modified and not program.get('is_modified'):
            self.db.increase_user_program_count(user["username"])
        program['is_modified'] = is_modified
        program = self.db.update_program(program['id'], program)

        querylog.log_value(program_id=program['id'],
                           adventure_name=adventure_name, error=error, code_lines=len(code.split('\n')))

        return program


class ProgramsModule(WebsiteModule):
    """Flask routes that deal with manipulating programs."""

    def __init__(self, db: Database, achievements: Achievements, statistics: StatisticsModule):
        super().__init__("programs", __name__, url_prefix="/programs")
        self.logic = ProgramsLogic(db, achievements, statistics)
        self.db = db
        self.achievements = achievements

    @route("/list", methods=["GET"])
    @requires_login
    def list_programs(self, user):
        # Filter by level, adventure, submitted, paginated.
        return {"programs": self.db.programs_for_user(user["username"]).records}

    @route("/delete/", methods=["POST"])
    @requires_login
    def delete_program(self, user):
        body = request.json
        if not isinstance(body.get("id"), str):
            return "program id must be a string", 400

        result = self.db.program_by_id(body["id"])

        if not result or (result["username"] != user["username"] and not is_admin(user)):
            return "", 404
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

        achievement = self.achievements.add_single_achievement(user["username"], "do_you_have_copy")

        resp = {"message": gettext("delete_success")}
        if achievement:
            resp["achievement"] = achievement
        return jsonify(resp)

    @route("/duplicate-check", methods=["POST"])
    def check_duplicate_program(self):
        body = request.json
        if not isinstance(body, dict):
            return "body must be an object", 400
        if not isinstance(body.get("name"), str):
            return "name must be a string", 400

        if not current_user()["username"]:
            return gettext("save_prompt"), 403

        programs = self.db.programs_for_user(current_user()["username"])
        for program in programs:
            if program["name"] == body["name"]:
                return jsonify({"duplicate": True, "message": gettext("overwrite_warning")})
        return jsonify({"duplicate": False})

    @route("/", methods=["POST"])
    @requires_login
    def save_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return "body must be an object", 400
        if not isinstance(body.get("code"), str):
            return "code must be a string", 400
        if not isinstance(body.get("name"), str):
            return "name must be a string", 400
        if not isinstance(body.get("level"), int):
            return "level must be an integer", 400
        if 'program_id' in body and not isinstance(body.get("program_id"), str):
            return "program_id must be a string", 400
        if 'shared' in body and not isinstance(body.get("shared"), bool):
            return "shared must be a boolean", 400
        if "adventure_name" in body:
            if not isinstance(body.get("adventure_name"), str):
                return "if present, adventure_name must be a string", 400

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
                    return jsonify({"parse_error": True, "message": gettext("save_parse_warning")})

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

        return jsonify({
            "message": gettext("save_success_detail"),
            "share_message": gettext("copy_clipboard"),
            "name": program["name"],
            "id": program['id'],
            "save_info": SaveInfo.from_program(Program.from_database_row(program)),
            "achievements": self.achievements.get_earned_achievements(),
        })

    @route("/share/<program_id>", methods=['POST'], defaults={'second_teachers_programs': False})
    @route("/share/<program_id>/<second_teachers_programs>", methods=["POST"])
    @requires_login
    def share_unshare_program(self, user, program_id, second_teachers_programs):
        program = self.db.program_by_id(program_id)
        if not program or program["username"] != user["username"]:
            return "No such program!", 404

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
        achievement = self.achievements.add_single_achievement(user["username"], "sharing_is_caring")
        if achievement:
            utils.add_pending_achievement({"achievement": achievement})

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
            return "body must be an object", 400
        if not isinstance(body.get("id"), str):
            return "id must be a string", 400

        result = self.db.program_by_id(body["id"])
        if not result or result["username"] != user["username"]:
            return "No such program!", 404

        program = self.db.submit_program_by_id(body["id"], True)
        self.db.increase_user_submit_count(user["username"])
        self.achievements.increase_count("submitted")
        self.achievements.verify_submit_achievements(user["username"])

        response = {
            "message": gettext("submitted"),
            "save_info": SaveInfo.from_program(Program.from_database_row(program)),
            "achievements": self.achievements.get_earned_achievements(),
        }
        return jsonify(response)

    @route("/unsubmit", methods=["POST"])
    @requires_teacher
    def unsubmit_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return "body must be an object", 400
        if not isinstance(body.get("id"), str):
            return "id must be a string", 400

        result = self.db.program_by_id(body["id"])
        if not result:
            return "No such program!", 404

        program = self.db.submit_program_by_id(body["id"], False)

        response = {
            "message": gettext("unsubmitted"),
            "save_info": SaveInfo.from_program(Program.from_database_row(program)),
            "achievements": self.achievements.get_earned_achievements(),
        }
        return jsonify(response)

    @route("/set_favourite", methods=["POST"])
    @requires_login
    def set_favourite_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return "body must be an object", 400
        if not isinstance(body.get("id"), str):
            return "id must be a string", 400
        if not isinstance(body.get("set"), bool):
            return "set must be a bool", 400

        result = self.db.program_by_id(body["id"])
        if not result or result["username"] != user["username"]:
            return "No such program!", 404

        if self.db.set_favourite_program(user["username"], body["id"], body["set"]):
            message = gettext("favourite_success") if body["set"] else gettext("unfavourite_success")
            return jsonify({"message": message})
        else:
            return "You can't set a favourite program without a public profile", 400

    @route("/set_hedy_choice", methods=["POST"])
    @requires_admin
    def set_hedy_choice(self, user):
        body = request.json
        if not isinstance(body, dict):
            return "body must be an object", 400
        if not isinstance(body.get("id"), str):
            return "id must be a string", 400
        if not isinstance(body.get("favourite"), int):
            return "favourite must be a integer", 400

        favourite = True if body.get("favourite") == 1 else False

        result = self.db.program_by_id(body["id"])
        if not result:
            return "No such program!", 404

        self.db.set_program_as_hedy_choice(body["id"], favourite)
        if favourite:
            return jsonify({"message": 'Program successfully set as a "Hedy choice" program.'}), 200
        return jsonify({"message": 'Program successfully removed as a "Hedy choice" program.'}), 200

    @route("/report", methods=["POST"])
    @requires_login
    def report_program(self, user):
        body = request.json

        # Make sure the program actually exists and is public
        program = self.db.program_by_id(body.get("id"))
        if not program or program.get("public") != 1:
            return gettext("report_failure"), 400

        link = email_base_url() + "/hedy/" + body.get("id") + "/view"
        send_email(
            config["email"]["sender"],
            "The following program is reported by " + user["username"],
            link,
            '<a href="' + link + '">Program link</a>',
        )

        return {"message": gettext("report_success")}, 200


class NotYourProgramError(RuntimeError):
    pass
