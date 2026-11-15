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


def test_super_teacher_can_make_public_adventure_private(client: Client, given: Given):
    # GIVEN
    owner = given.a_teacher_account()
    super_teacher = given.a_teacher_account()
    given.db.update_user(super_teacher['username'], {'is_super_teacher': 1})
    given.logged_in_as(super_teacher)

    public_adv = given.some_saved_adventure(owner['username'], public=1, tags=['moderation-tag'])
    given.db.create_tag({
        'id': 'moderation-tag-id',
        'name': 'moderation-tag',
        'tagged_in': [{'id': public_adv['id'], 'public': 1, 'language': 'en'}],
        'popularity': 1,
    })

    # WHEN
    response = client.post(f'/public-adventures/make-private/{public_adv["id"]}')

    # THEN - the adventure is private, still owned by its creator, and the tag copy is in sync
    assert response.status_code == 200
    adventure = given.db.get_adventure(public_adv['id'])
    assert adventure['public'] == 0
    assert adventure['creator'] == owner['username']
    assert given.db.read_tag('moderation-tag')['tagged_in'][0]['public'] == 0


def test_regular_teacher_cannot_make_public_adventure_private(client: Client, given: Given):
    # GIVEN
    owner = given.a_teacher_account()
    given.logged_in_as_new_teacher()
    public_adv = given.some_saved_adventure(owner['username'], public=1)

    # WHEN
    response = client.post(f'/public-adventures/make-private/{public_adv["id"]}', check=False)

    # THEN
    assert response.status_code == 401
    assert given.db.get_adventure(public_adv['id'])['public'] == 1
