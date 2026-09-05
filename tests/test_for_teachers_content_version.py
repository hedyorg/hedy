import unittest

import website_content as hedy_content
from website.for_teachers import _create_customizations


class FakeDatabase:
    def __init__(self):
        self.saved_customizations = None

    def update_class_customizations(self, customizations):
        self.saved_customizations = customizations.copy()


class TestCreateCustomizationsContentVersion(unittest.TestCase):
    def test_default_adventures_use_latest_content_version(self):
        db = FakeDatabase()

        customizations = _create_customizations(db, "class-1", include_adventures=True)

        self.assertEqual(hedy_content.LAST_CONTENT_VERSION, customizations["content_version"])
        self.assertEqual(hedy_content.LAST_CONTENT_VERSION, db.saved_customizations["content_version"])
        self.assertTrue(customizations["sorted_adventures"])

    def test_empty_adventures_use_latest_content_version(self):
        db = FakeDatabase()

        customizations = _create_customizations(db, "class-2", include_adventures=False)

        self.assertEqual(hedy_content.LAST_CONTENT_VERSION, customizations["content_version"])
        self.assertEqual(hedy_content.LAST_CONTENT_VERSION, db.saved_customizations["content_version"])
        self.assertTrue(all(not adventures for adventures in customizations["sorted_adventures"].values()))
