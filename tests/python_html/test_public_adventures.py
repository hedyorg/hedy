# https://werkzeug.palletsprojects.com/en/stable/test/
from .fixtures.given import Given
from .fixtures.flask import Client
import pytest


def test_cloning_public_adventure(client: Client, given: Given):
    # GIVEN
    t1 = given.a_teacher_account()
    t2 = given.a_teacher_account()
    t3 = given.a_teacher_account()
    given.logged_in_as(t3)

    # Adventure owned by t1, authored by t2
    public_adv = given.some_saved_adventure(t1['username'], author=t2['username'], public=1)

    # WHEN - t3 clones it
    client.post(f'/public-adventures/clone/{public_adv["id"]}')

    # THEN - now t3 owns an adventure still authored by t2
    advs = given.db.get_teacher_adventures(t3['username'])
    assert advs[0]['author'] == t2['username']


def test_preview_public_adventure_without_solution_example(client: Client, given: Given):
    # GIVEN
    teacher = given.a_teacher_account()
    given.logged_in_as(teacher)
    public_adv = given.some_saved_adventure(teacher['username'], public=1, solution_example=None)

    # WHEN
    response = client.get(f'/public-adventures/preview/{public_adv["id"]}', headers={'Hx-Request': 'true'})

    # THEN
    assert response.status_code == 200
    assert 'An adventure' in response.get_data(as_text=True)
