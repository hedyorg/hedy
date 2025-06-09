# https://werkzeug.palletsprojects.com/en/stable/test/
from .fixtures.given import Given
from .fixtures.flask import Client


def test_programs_page_loads_with_lots_of_programs(client: Client, given: Given):
    """Smoke test of the programs page, if there are enough programs for pagination."""
    # GIVEN
    user = given.logged_in_as_new_student()
    for _ in range(20):
        given.some_saved_program(user['username'])

    # WHEN
    client.get('/programs')

    # THEN - it succeeds
