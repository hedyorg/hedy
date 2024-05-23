import uuid

from flask import jsonify, make_response, redirect, request, session
from jinja_partials import render_partial
from flask_babel import gettext

import utils
from config import config
from website.flask_helpers import render_template
from website.auth import current_user, is_teacher, requires_login, requires_teacher, \
    refresh_current_user_from_db, is_second_teacher

from .achievements import Achievements
from .database import Database
from .website_module import WebsiteModule, route

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


class ClassModule(WebsiteModule):
    """The /class/... pages."""

    def __init__(self, db: Database, achievements: Achievements):
        super().__init__("class", __name__, url_prefix="/class")

        self.db = db
        self.achievements = achievements

    @route("/", methods=["POST"])
    @requires_teacher
    def create_class(self, user):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("name"), str):
            return gettext("class_name_invalid"), 400
        if len(body.get("name")) < 1:
            return gettext("class_name_empty"), 400

        # We use this extra call to verify if the class name doesn't already exist, if so it's a duplicate
        Classes = self.db.get_teacher_classes(user["username"], True, teacher_only=True)
        for Class in Classes:
            if Class["name"] == body["name"]:
                return gettext("class_name_duplicate"), 200

        Class = {
            "id": uuid.uuid4().hex,
            "date": utils.timems(),
            "teacher": user["username"],
            "link": utils.random_id_generator(7),
            "name": body["name"],
        }

        self.db.store_class(Class)
        achievement = self.achievements.add_single_achievement(user["username"], "ready_set_education")
        if achievement:
            return {"id": Class["id"], "achievement": achievement}, 200
        return {"id": Class["id"]}, 200

    @route("/<class_id>", methods=["PUT"])
    @requires_teacher
    def update_class(self, user, class_id):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("name"), str):
            return gettext("class_name_invalid"), 400
        if len(body.get("name")) < 1:
            return gettext("class_name_empty"), 400

        Class = self.db.get_class(class_id)
        if not Class or not (utils.can_edit_class(user, Class)):
            return gettext("no_such_class"), 404

        # We use this extra call to verify if the class name doesn't already exist, if so it's a duplicate
        username = user["username"]
        if is_second_teacher(user, class_id):
            username = Class["teacher"]
        Classes = self.db.get_teacher_classes(username, True, teacher_only=True)
        for Class in Classes:
            if Class["name"] == body["name"]:
                return gettext("class_name_duplicate"), 200

        self.db.update_class(class_id, body["name"])
        achievement = self.achievements.add_single_achievement(user["username"], "on_second_thoughts")
        if achievement:
            return {"achievement": achievement}, 200
        return make_response('', 204)

    @route("/<class_id>", methods=["DELETE"])
    @requires_login
    def delete_class(self, user, class_id):
        Class = self.db.get_class(class_id)
        if not Class:
            return gettext("no_such_class"), 404
        if Class["teacher"] != user["username"]:  # only teachers can remove their classes.
            return gettext("unauthorized"), 401

        self.db.delete_class(Class)

        achievement = self.achievements.add_single_achievement(user["username"], "end_of_semester")
        if achievement:
            utils.add_pending_achievement({"achievement": achievement})
        teacher_classes = self.db.get_teacher_classes(user["username"], True)
        return render_partial('htmx-classes-table.html', teacher_classes=teacher_classes)

    @route("/<class_id>/prejoin/<link>", methods=["GET"])
    def prejoin_class(self, class_id, link):
        Class = self.db.get_class(class_id)
        if not Class or Class["link"] != link:
            return utils.error_page(error=404, ui_message=gettext("invalid_class_link"))
        if request.cookies.get(cookie_name):
            token = self.db.get_token(request.cookies.get(cookie_name))
            if token and token.get("username") in Class.get("students", []):
                return render_template(
                    "class-prejoin.html",
                    joined=True,
                    page_title=gettext("title_join-class"),
                    current_page="my-profile",
                    class_info={"name": Class["name"]},
                )
        return render_template(
            "class-prejoin.html",
            joined=False,
            page_title=gettext("title_join-class"),
            current_page="my-profile",
            class_info={"id": Class["id"], "name": Class["name"]},
        )

    @route('join/<class_id>', methods=["POST"])
    @requires_login
    def join_class_id(self, user, class_id):
        Class = self.db.get_class(class_id)
        if not Class:
            # TODO: change to invalid_class; if necessary!
            return utils.error_page(error=404, ui_message=gettext("invalid_class_link"))

        username = user['username']
        if not username:
            return gettext("join_prompt"), 403

        # We only want to remove the invite if the user joins the class with an actual pending invite
        invite = self.db.get_user_class_invite(username, class_id)

        if invite:
            invited_as = invite.get("invited_as")
            if invited_as == "second_teacher":
                self.db.add_second_teacher_to_class(Class, user)
            elif invited_as == "student":
                student_classes = self.db.get_student_classes(username)
                if len(student_classes):
                    return gettext("student_not_allowed_in_class"), 400
                self.db.add_student_to_class(Class["id"], username)

            refresh_current_user_from_db()
            self.db.remove_user_class_invite(username, class_id)
            # Also remove the pending message in this case
            session["messages"] = session["messages"] - 1 if session["messages"] else 0

        achievement = self.achievements.add_single_achievement(username, "epic_education")
        if achievement:
            utils.add_pending_achievement({"achievement": achievement, "redirect": "/programs"})
            return {"achievement": achievement}, 200
        # request.url = re.sub(r'/class/.*', '/programs', request.url)
        # return redirect(request.url, code=302)
        return {}, 302

    # Legacy function; will be gradually replaced by the join_class_id
    @route("/join", methods=["POST"])
    def join_class(self):
        body = request.json
        Class = None
        if "id" in body:
            Class = self.db.get_class(body["id"])
        if not Class or Class["id"] != body["id"]:
            return utils.error_page(error=404, ui_message=gettext("invalid_class_link"))

        username = current_user()["username"]
        if not username:
            return gettext("join_prompt"), 403

        student_classes = self.db.get_student_classes(username)
        if len(student_classes):
            return gettext("student_not_allowed_in_class"), 400

        self.db.add_student_to_class(Class["id"], username)
        refresh_current_user_from_db()
        achievement = self.achievements.add_single_achievement(username, "epic_education")

        # We only want to remove the invite if the user joins the class with an actual pending invite
        invite = self.db.get_user_class_invite(username, Class["id"])
        if invite:
            self.db.remove_user_class_invite(username, Class["id"])
            # Also remove the pending message in this case
            session["messages"] = session["messages"] - 1 if session["messages"] else 0

        if achievement:
            return {"achievement": achievement}, 200
        else:
            return make_response('', 204)

    @route("/<class_id>/student/<student_id>", methods=["DELETE"])
    @requires_login
    def leave_class(self, user, class_id, student_id):
        Class = self.db.get_class(class_id)
        if not Class or not (utils.can_edit_class(user, Class)):
            return gettext("ajax_error"), 400

        self.db.remove_student_from_class(Class["id"], student_id)
        refresh_current_user_from_db()
        achievement = None
        if Class["teacher"] == user["username"]:
            achievement = self.achievements.add_single_achievement(user["username"], "detention")
        if achievement:
            return {"achievement": achievement}, 200
        return make_response('', 204)

    @route("/<class_id>/second-teacher/<second_teacher>", methods=["DELETE"])
    @requires_login
    def remove_second_teacher(self, user, class_id, second_teacher):
        Class = self.db.get_class(class_id)
        if not Class or Class["teacher"] != user["username"]:  # only teachers can remove second teachers.
            return gettext("ajax_error"), 400
        second_teacher = self.db.user_by_username(second_teacher)
        self.db.remove_second_teacher_from_class(Class, second_teacher)

        refresh_current_user_from_db()
        achievement = None
        if Class["teacher"] == user["username"]:
            achievement = self.achievements.add_single_achievement(user["username"], "detention")
        if achievement:
            utils.add_pending_achievement({"achievement": achievement, "reload": True})
            return {"achievement": achievement}, 200
        return {}, 205


class MiscClassPages(WebsiteModule):
    """All the pages that have to do with the teacher interface or classes, but
    are not mounted under the '/class' URL space.
    """

    def __init__(self, db: Database, achievements: Achievements):
        # Note: explicitly no 'url_prefix'
        super().__init__("miscclass", __name__)
        self.db = db
        self.achievements = achievements

    @route("/classes", methods=["GET"])
    @requires_teacher
    def get_classes(self, user):
        return jsonify(self.db.get_teacher_classes(user["username"], True))

    @route("/duplicate_class", methods=["POST"])
    @requires_teacher
    def duplicate_class(self, user):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("name"), str):
            return gettext("class_name_invalid"), 400
        if len(body.get("name")) < 1:
            return gettext("class_name_empty"), 400

        Class = self.db.get_class(body.get("id"))
        if not Class or not utils.can_edit_class(user, Class):  # only teachers can duplicate a class
            return gettext("no_such_class"), 404

        # second_teachers = Class.get("second_teachers")

        # We use this extra call to verify if the class name doesn't already exist, if so it's a duplicate
        # Todo TB: This is a duplicate function, might be nice to perform some clean-up to reduce these parts
        Classes = self.db.get_teacher_classes(user["username"], True, teacher_only=True)
        for Class in Classes:
            if Class["name"] == body.get("name"):
                return gettext("class_name_duplicate"), 400

        # All the class settings are still unique, we are only concerned with copying the customizations
        # Shortly: Create a class like normal: concern with copying the customizations
        class_id = uuid.uuid4().hex

        new_class = {
            "id": class_id,
            "date": utils.timems(),
            "teacher": user["username"],
            "link": utils.random_id_generator(7),
            "name": body.get("name"),
            "created_by": user["username"],
        }

        self.db.store_class(new_class)
        # TODO: duplicate students and second teachers.
        # if second_teachers:
        #     for st in second_teachers:
        #         self.db.add_second_teacher_to_class(new_class, st)

        # Get the customizations of the current class -> if they exist, update id and store again
        customizations = self.db.get_class_customizations(body.get("id"))
        if customizations:
            customizations["id"] = class_id
            self.db.update_class_customizations(customizations)

        new_second_teachers = {}
        if body.get("second_teacher") is True:
            new_second_teachers = Class.get("second_teachers")

        achievement = self.achievements.add_single_achievement(current_user()["username"], "one_for_money")
        if achievement:
            return {"achievement": achievement}, 200
        if new_second_teachers:
            return {"id": new_class["id"], "second_teachers": new_second_teachers}, 200
        return {"id": new_class["id"]}, 200

    @route("/invite-student", methods=["POST"])
    @requires_teacher
    def invite_student(self, user):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("class_id"), str):
            return "class id must be a string", 400
        if len(body.get("username")) < 1:
            return gettext("username_empty"), 400

        username = body.get("username").lower()
        class_id = body.get("class_id")

        Class = self.db.get_class(class_id)
        if not Class or not (utils.can_edit_class(user, Class)):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        user = self.db.user_by_username(username)
        if not user:
            return gettext("student_not_existing"), 400
        if "students" in Class and user["username"] in Class["students"]:
            return gettext("student_already_in_class"), 400
        else:
            student_classes = self.db.get_student_classes(username)
            if len(student_classes):
                return gettext("student_not_allowed_in_class"), 400
        if self.db.get_user_invitations(user["username"]):
            return gettext("student_already_invite"), 400

        # So: The class and student exist and are currently not a combination -> invite!
        data = {
            "username": username,
            "class_id": class_id,
            "timestamp": utils.times(),
            "ttl": utils.times() + invite_length,
            "invited_as": 'student',
            "invited_as_text": gettext("student"),
        }
        self.db.add_class_invite(data)
        return make_response('', 204)

    @route("/invite-second-teacher", methods=["POST"])
    @requires_teacher
    def invite_second_teaceher(self, user):
        teacher = user
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("class_id"), str):
            return "class id must be a string", 400
        if len(body.get("username")) < 1:
            return gettext("username_empty"), 400

        username = body.get("username").lower()
        class_id = body.get("class_id")

        user = self.db.user_by_username(username)
        if not user:
            return gettext("teacher_invalid"), 400  # TODO: change to teacher not existing
        # existing_invitation = self.db.get_user_invitations(user["username"])
        invite = self.db.get_user_class_invite(username, class_id)
        if invite:
            return gettext("student_already_invite"), 400
        if is_second_teacher(user, class_id):
            return "Already a second teacher.", 400

        Class = self.db.get_class(class_id)
        if not Class:
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))
        elif Class["teacher"] != teacher["username"] or not is_teacher(user):
            return gettext("teacher_invalid"), 400
        elif Class["teacher"] == username:  # this check is almost never the case; but just in case.
            return "You cannot add yourself as a second teacher!", 400

        data = {
            "username": username,
            "class_id": class_id,
            "timestamp": utils.times(),
            "ttl": utils.times() + invite_length,
            "invited_as": "second_teacher",
            "invited_as_text": gettext("second_teacher"),
        }
        self.db.add_class_invite(data)
        return make_response('', 204)

    @route("/remove_student_invite", methods=["POST"])
    @requires_login
    def remove_invite(self, user):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("class_id"), str):
            return "class id must be a string", 400

        username = body.get("username")
        class_id = body.get("class_id")

        # Fixme TB -> Sure the user is also allowed to remove their invite, but why the 'retrieve_class_error'?
        if not is_teacher(user) and username != user.get("username"):
            return utils.error_page(error=401, ui_message=gettext("retrieve_class_error"))
        Class = self.db.get_class(class_id)
        if not Class or (not utils.can_edit_class(user, Class) and username != user.get("username")):
            return utils.error_page(error=404, ui_message=gettext("no_such_class"))

        self.db.remove_user_class_invite(username, class_id)
        return make_response('', 204)

    @route("/hedy/l/<link_id>", methods=["GET"])
    def resolve_class_link(self, link_id):
        Class = self.db.resolve_class_link(link_id)
        if not Class:
            return utils.error_page(error=404, ui_message=gettext("invalid_class_link"))
        return redirect(
            request.url.replace("/hedy/l/" + link_id, "/class/" + Class["id"] + "/prejoin/" + link_id), code=302
        )
