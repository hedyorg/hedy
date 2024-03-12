// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('getBySel', (selector, ...args) => {
  return cy.get(`[data-cy=${selector}]`, ...args)
})

Cypress.Commands.add('getBySelLike', (selector, ...args) => {
  return cy.get(`[data-cy*=${selector}]`, ...args)
})

Cypress.Commands.add("checkForPlaceholders", () => {
  // Check elements that could include placeholders.
  cy.get("h1, h2, h3, p, label, input, button, option").each(($el) => {
    const text = $el.text().trim();
    const longText = text.split(" ").length > 3;
    // const hasSpaces = text.split(" ").length > 1;
    // if (!hasSpaces && text.includes("_")) {
      if (!longText && text.includes("_")) {
        expect(text).not.to.include("_"); // Fail if placeholder found
    }
  });

  const KEYS = ["value", "alt", "title"];
  // Optionally, check data attributes for placeholders
  cy.get("*").each(($el) => {
    const dataAttrs = $el.data();
    for (const key in KEYS) {
      if (dataAttrs.hasOwnProperty(key) && typeof dataAttrs[key] === "string") {
        const hasSpaces = dataAttrs[key].split(" ").length > 1;
        if (!hasSpaces && dataAttrs[key].includes("_")) {
          expect(dataAttrs[key]).not.to.include("_"); // Fail if placeholder found in data attribute
        }
      }
    }
  });
});
