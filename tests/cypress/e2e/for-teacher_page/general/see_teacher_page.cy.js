describe('teacher login redirect behavior', () => {
  const loginAsTeacher = () => {
    cy.intercept('POST', '/auth/login').as('loginUi')
    cy.getDataCy('username', { timeout: 15000 }).clear().type('teacher1')
    cy.getDataCy('password', { timeout: 15000 }).clear().type('123456', { parseSpecialCharSequences: false })
    cy.getDataCy('login_button').click()
    cy.wait('@loginUi').its('response.statusCode').should('eq', 200)
  }

  it('redirects a teacher to for-teachers when login starts from home', () => {
    cy.visit('/')
    cy.get('a[href="/login"]:visible').first().click()
    cy.location('pathname', { timeout: 15000 }).should('eq', '/login')

    loginAsTeacher()

    cy.location('pathname', { timeout: 15000 }).should('eq', '/for-teachers')
  })

  it('keeps a teacher on their original page when login starts away from home', () => {
    cy.visit('/')
    cy.window().then((win) => {
      win.localStorage.setItem('login-redirect', JSON.stringify({ url: `${Cypress.config('baseUrl')}/hedy/1` }))
    })
    cy.visit('/login')
    cy.location('pathname', { timeout: 15000 }).should('eq', '/login')

    loginAsTeacher()

    cy.location('pathname', { timeout: 15000 }).should('eq', '/hedy/1')
  })
})