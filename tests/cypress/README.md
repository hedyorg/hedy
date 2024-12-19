# Cypress tests

This directory contains tests that run in the browser using Cypress. They are
written in JavaScript, and interact with the Hedy website like a real user would.

Compared to the Python/HTML tests.

- ✅ Simulates a real user: Cypress tests can only click on a button if that
  button is actually visible, just like a user would.
- ✅ Test browser interaction: Cypress tests run in the browser so they test the
  entire stack, including the JavaScript in running on the client side.
- ❌ Slower: because they puppeteer an actual browser instance, these tests are slower
  to run.
- ❌ More awkward setup: because they have no special access to the server, these
  tests need to go through normal user dialog screens to set up the database in a
  particular state before a specific test can be run.
- ❌ Waiting: user interactions and page loads take time, and your tests need to
  account for this. This is often a frustrating source of flaky tests.


## Resources

Some resources about writing tests here:

- <https://docs.cypress.io/api/table-of-contents>
- <https://docs.cypress.io/app/core-concepts/best-practices>