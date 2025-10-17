# Python/HTML tests

This directory contains tests that use Python to test the HTML that the Flask
app returns.

Compared to the Cypress tests:

- ✅ Faster to run: there is no UI interaction and no waiting, so they will go faster.
- ✅ Easier setup: easy to get the database into a desired state.
- ✅ No race conditions: we test the returned HTML in one shot, and we're not waiting
  for anything.
- ❌ Only server part: these tests cannot test code running in the browser, so we still
  need Cypress tests to test anything involving JavaScript.
- ❌ No presentation: these tests can only test that buttons are in the HTML; they cannot
  test that those UI elements are actually visible to users.


## Resources

Some resources about writing tests here:

- <https://flask.palletsprojects.com/en/stable/testing/>
- <https://werkzeug.palletsprojects.com/en/stable/test/>
- <https://docs.pytest.org/en/6.2.x/fixture.html>
