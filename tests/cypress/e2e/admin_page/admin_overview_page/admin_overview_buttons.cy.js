import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminPage } from '../../tools/navigation/nav.js'


// This dict contains all id's of the buttons to be tested and their expected urls
const buttons_dict = {
'#users_button': 'admin_users_page',
'#classes_button': 'admin_classes_page',
'#adventures_button': 'admin_adventures_page',
'#achievements_button': 'admin_achievements_page',
'#statistics_button': 'admin_stats_page',
'#logs_button': 'admin_logs_page'}


describe('Admin overview buttons', () => {
  it('passes', () => {
    loginForAdmin();

    for (let button in buttons_dict){
       cy.get(button)
      .should('be.visible')
      .should('be.not.disabled')
      .click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env(buttons_dict[button]));
    goToAdminPage();
    }

  })
})
