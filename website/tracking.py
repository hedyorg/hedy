
from flask import request
# from flask_babel import gettext
# import jinja_partials
# import uuid

# import utils
from config import config
from website.auth import requires_login

from .database import Database
from .website_module import WebsiteModule, route

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


class TrackingModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("tracking", __name__, url_prefix="/tracking")

        self.db = db

    def index_teacher(self, user):
        return {}

    @route("/", methods=["POST"])
    @requires_login
    def index(self, user):
        # /tracking/
        user = self.db.user_by_username(user["username"])
        if user.get("is_teacher"):
            return self.index_teacher(user)

        print("\n\n\n TRACKING index \n\n")
        data = request.json
        print(data)
        print(user)
        """
        TODO for you:
            - create a db for tracking
            - for each id, log it in the DB.
                - make sure not to overwrite existing fields in the db
            - student:
                - class_id
                - user gender
                - user language
                - user birth_year
                - current timestamp

        """
        return {}
