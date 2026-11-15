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


def test_filter_public_adventures_by_teacher_username(client: Client, given: Given):
    # GIVEN
    t1 = given.a_teacher_account()
    t2 = given.a_teacher_account()
    given.some_saved_adventure(t1['username'], name='T1 Public Adventure', public=1)
    given.some_saved_adventure(t1['username'], name='T1 Private Adventure', public=0)
    given.some_saved_adventure(t2['username'], name='T2 Public Adventure', public=1)
    given.logged_in_as_new_teacher()

    # WHEN - filtering by t1's username (case-insensitive)
    html = client.get(f'/public-adventures/?creator={t1["username"].upper()}').get_data(as_text=True)

    # THEN - only t1's public adventure is listed
    assert 'T1 Public Adventure' in html
    assert 'T1 Private Adventure' not in html
    assert 'T2 Public Adventure' not in html
