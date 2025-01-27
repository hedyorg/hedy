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
