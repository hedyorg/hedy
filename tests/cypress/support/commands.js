// ***********************************************
// This example keywords.js shows you how to
// create various custom keywords and overwrite
// existing keywords.
//
// For more comprehensive examples of custom
// keywords please read more here:
// https://on.cypress.io/custom-keywords
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.keywords.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.keywords.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.keywords.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.keywords.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.keywords.add('getDataCy', (selector, ...args) => {
  let dataSelector = "";
  const selectors = selector.split(" ");
  for (let s of selectors) {
    if (s.startsWith("*")) {
      s = s.slice(1);
      dataSelector += `*[data-cy="${s}"] `
    } else {
      dataSelector += `[data-cy="${s}"] `
    }
  }

  return cy.get(dataSelector, ...args)
})

Cypress.keywords.add('getDataCyLike', (selector, ...args) => {
  return cy.get(`*[data-cy="${selector}"]`, ...args)
})
