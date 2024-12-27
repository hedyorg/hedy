# https://werkzeug.palletsprojects.com/en/stable/test/
from .fixtures.given import Given
from .fixtures.flask import Client
import bs4


def test_explore_page_loads_with_lots_of_programs(client: Client, given: Given):
    """Smoke test of the explore page, if there are enough programs for pagination."""
    # GIVEN
    user = given.logged_in_as_student()
    for _ in range(50):
      given.some_saved_program(user['username'], public=1)

    # WHEN
    response = client.get('/explore')

    # THEN - it succeeds, renders a lot of adventures and a next button
    soup = bs4.BeautifulSoup(response.data, 'html.parser')
    adventures = soup.find_all('div', class_='adventure')
    assert len(adventures) > 40

    next_page_link = soup.find('a', { 'aria-label': 'Next page' })
    assert next_page_link


