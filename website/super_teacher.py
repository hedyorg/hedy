
from flask import render_template


from website.auth import requires_teacher

from .database import Database
from .website_module import WebsiteModule, route


class SuperTeacherModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("super_teacher", __name__, url_prefix="/super-teacher")
        self.db = db

    @route("/", methods=["GET"])
    @requires_teacher
    def get_super_teacher_page(self, user):
        print("\n\n\n\n\n TESTING HERE?")
        return render_template('super-teacher/super_teacher.html')
