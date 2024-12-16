"""
Configuration file for py.test

Mostly just defines where the fixtures are for the Python/HTML
tests.
"""

pytest_plugins = [
   "tests.python_html.fixtures.flask",
   "tests.python_html.fixtures.given",
]