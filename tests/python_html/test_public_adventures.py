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


def a_logged_in_super_teacher(given: Given):
    super_teacher = given.a_teacher_account()
    given.db.update_user(super_teacher['username'], {'is_super_teacher': 1})
    given.logged_in_as(super_teacher)
    return super_teacher


def test_super_teacher_can_change_public_adventure_language(client: Client, given: Given):
    # GIVEN
    owner = given.a_teacher_account()
    a_logged_in_super_teacher(given)
    public_adv = given.some_saved_adventure(owner['username'], public=1, language='en', tags=['language-tag'])
    given.db.create_tag({
        'id': 'language-tag-id',
        'name': 'language-tag',
        'tagged_in': [{'id': public_adv['id'], 'public': 1, 'language': 'en'}],
        'popularity': 1,
    })

    # WHEN
    response = client.post(f'/public-adventures/change-language/{public_adv["id"]}', data={'language': 'nl'})

    # THEN - the adventure and the tag copy now have the new language
    assert response.status_code == 200
    assert given.db.get_adventure(public_adv['id'])['language'] == 'nl'
    assert given.db.read_tag('language-tag')['tagged_in'][0]['language'] == 'nl'


def test_change_public_adventure_language_rejects_unknown_language(client: Client, given: Given):
    # GIVEN
    owner = given.a_teacher_account()
    a_logged_in_super_teacher(given)
    public_adv = given.some_saved_adventure(owner['username'], public=1, language='en')

    # WHEN
    response = client.post(f'/public-adventures/change-language/{public_adv["id"]}',
                           data={'language': 'not-a-language'}, check=False)

    # THEN
    assert response.status_code == 400
    assert given.db.get_adventure(public_adv['id'])['language'] == 'en'


def test_regular_teacher_cannot_change_public_adventure_language(client: Client, given: Given):
    # GIVEN
    owner = given.a_teacher_account()
    given.logged_in_as_new_teacher()
    public_adv = given.some_saved_adventure(owner['username'], public=1, language='en')

    # WHEN
    response = client.post(f'/public-adventures/change-language/{public_adv["id"]}',
                           data={'language': 'nl'}, check=False)

    # THEN
    assert response.status_code == 401
    assert given.db.get_adventure(public_adv['id'])['language'] == 'en'


def test_language_dropdown_only_shown_to_super_teachers(client: Client, given: Given):
    # GIVEN
    owner = given.a_teacher_account()
    public_adv = given.some_saved_adventure(owner['username'], public=1, language='en')
    preview_url = f'/public-adventures/preview/{public_adv["id"]}'

    # WHEN / THEN - a super teacher gets the dropdown with the current language selected
    a_logged_in_super_teacher(given)
    html = client.get(preview_url, headers={'Hx-Request': 'true'}).get_data(as_text=True)
    assert 'change_adventure_language' in html
    assert '<option value="en" selected>' in html

    # WHEN / THEN - a regular teacher does not
    given.logged_in_as_new_teacher()
    html = client.get(preview_url, headers={'Hx-Request': 'true'}).get_data(as_text=True)
    assert 'change_adventure_language' not in html
