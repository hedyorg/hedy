import uuid
from typing import Optional

from flask import g, request, jsonify
from flask_babel import gettext

import hedy
import utils
from config import config
from website.auth import current_user, email_base_url, is_admin, requires_admin, requires_login, send_email

from .achievements import Achievements
from .database import Database
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

    def __init__(self, db: Database, achievements: Achievements):
        self.db = db
        self.achievements = achievements

    @querylog.timed
    def store_user_program(self,
                           user,
                           level: int,
                           name: str,
                           code: str,
                           error: bool,
                           program_id: Optional[str] = None,
                           adventure_name: Optional[str] = None,
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
            self.db.increase_user_program_count(user["username"])

        self.db.increase_user_save_count(user["username"])
        self.achievements.increase_count("saved")
        self.achievements.verify_save_achievements(user["username"], adventure_name)

        querylog.log_value(program_id=program['id'],
                           adventure_name=adventure_name, error=error, code_lines=len(code.split('\n')))

        return program


class ProgramsModule(WebsiteModule):
    """Flask routes that deal with manipulating programs."""

    def __init__(self, db: Database, achievements: Achievements):
        super().__init__("programs", __name__, url_prefix="/programs")
        self.logic = ProgramsLogic(db, achievements)
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
            self.db.set_favourite_program(user["username"], None)

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
            adventure_name=body.get('adventure_name'))

        return jsonify({
            "message": gettext("save_success_detail"),
            "share_message": gettext("copy_clipboard"),
            "name": program["name"],
            "id": program['id'],
            "save_info": SaveInfo.from_program(Program.from_database_row(program)),
            "achievements": self.achievements.get_earned_achievements(),
        })

    @route("/share", methods=["POST"])
    @requires_login
    def share_unshare_program(self, user):
        body = request.json
        if not isinstance(body, dict):
            return "body must be an object", 400
        if not isinstance(body.get("id"), str):
            return "id must be a string", 400
        if not isinstance(body.get("public"), bool):
            return "public must be a boolean", 400

        result = self.db.program_by_id(body["id"])
        if not result or result["username"] != user["username"]:
            return "No such program!", 404

        # This only happens in the situation were a user un-shares their favourite program -> Delete from public profile
        public_profile = self.db.get_public_profile_settings(current_user()["username"])
        if (
            public_profile
            and "favourite_program" in public_profile
            and public_profile["favourite_program"] == body["id"]
        ):
            self.db.set_favourite_program(user["username"], None)

        program = self.db.set_program_public_by_id(body["id"], bool(body["public"]))
        achievement = self.achievements.add_single_achievement(user["username"], "sharing_is_caring")

        resp = {
            "id": body["id"],
            "public": bool(body["public"]),
            "save_info": SaveInfo.from_program(Program.from_database_row(program)),
        }

        if bool(body["public"]):
            resp["message"] = gettext("share_success_detail")
        else:
            resp["message"] = gettext("unshare_success_detail")
        if achievement:
            resp["achievement"] = achievement
        return jsonify(resp)

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

        program = self.db.submit_program_by_id(body["id"])
        self.db.increase_user_submit_count(user["username"])
        self.achievements.increase_count("submitted")
        self.achievements.verify_submit_achievements(user["username"])

        response = {
            "message": gettext("submitted"),
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

        result = self.db.program_by_id(body["id"])
        if not result or result["username"] != user["username"]:
            return "No such program!", 404

        if self.db.set_favourite_program(user["username"], body["id"]):
            return jsonify({"message": gettext("favourite_success")})
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
