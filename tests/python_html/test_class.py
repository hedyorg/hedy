from .fixtures.given import Given
from .fixtures.flask import Client


def test_second_teacher_of_deleted_class(client: Client, given: Given):
    # GIVEN a class with a second teacher
    teacher = given.logged_in_as_new_teacher('teacher')
    second_teacher = given.a_teacher_account('second_teacher')
    cls = given.a_class(teacher['username'])
    given.assign_second_teacher(second_teacher['username'], cls['id'])

    # WHEN the owner teacher deletes the class
    client.delete(f'/class/{cls["id"]}')
    client.post('/auth/logout')

    # THEN the second teacher can access the /for-teachers page
    client.post_json('/auth/login', second_teacher)
    client.get('/for-teachers')

