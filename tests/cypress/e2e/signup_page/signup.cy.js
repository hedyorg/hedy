import { goToSignup, goToProfilePage } from '../tools/navigation/nav.js'

beforeEach(() => {
  goToSignup();
})

describe('Test signing up', () => {
  it('Is able to sign up as a student', () => {
    cy.getDataCy('signup_student').click()

    // basic info
    cy.getDataCy('username').type('student123')
    cy.getDataCy('email').type('somerandomstudentemail@gmail.com')
    const some_password = 'some_password\"!#@\'( )*$%\'123\"'
    cy.getDataCy('password').type(some_password)
    cy.getDataCy('password_repeat').type(some_password)
    cy.getDataCy('language').select('English')
    cy.getDataCy('birth_year').type('2000')
    cy.getDataCy('gender').select('Female')
    cy.getDataCy('country').select('Australia')

    // teacher fields should not exist
    cy.getDataCy('from_another_teacher').should('not.exist')
    cy.getDataCy('social_media').should('not.exist')
    cy.getDataCy('from_video').should('not.exist')
    cy.getDataCy('from_magazine_website').should('not.exist')
    cy.getDataCy('other_source').should('not.exist')
    cy.getDataCy('subscribe').should('not.exist')
    cy.getDataCy('pair_with_teacher').should('not.exist')
    cy.getDataCy('connect_guest_teacher').should('not.exist')
  
    // experience
    cy.getDataCy('prog_experience_yes').check()
    cy.getDataCy('scratch').check()
    cy.getDataCy('other_block').check()
    cy.getDataCy('python').check()
    cy.getDataCy('other_text').check()
  
    cy.getDataCy('agree_terms').check()
    cy.getDataCy('submit_button').click()
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.env('landing_page'));
    
    // delete profile
    goToProfilePage();
    cy.getDataCy('personal_settings').click()
    cy.getDataCy('delete_profile_button').click()
    cy.getDataCy('modal_yes_button').click()
  })

  it('Is able to sign up as a teacher', () => {
    cy.getDataCy('signup_teacher').click()

    // basic info
    cy.getDataCy('username').type('teacher123')
    cy.getDataCy('email').type('somerandomteacheremail@gmail.com')
    const some_password = 'some_password\"!#@\'( )*$%\'123\"'
    cy.getDataCy('password').type(some_password)
    cy.getDataCy('password_repeat').type(some_password)
    cy.getDataCy('language').select('English')
    cy.getDataCy('birth_year').type('2000')
    cy.getDataCy('gender').select('Female')
    cy.getDataCy('country').select('Australia')

    // heard about
    cy.getDataCy('from_another_teacher').check()
    cy.getDataCy('social_media').check()
    cy.getDataCy('from_video').check()
    cy.getDataCy('from_magazine_website').check()
    cy.getDataCy('other_source').check()

    // experience
    cy.getDataCy('prog_experience_yes').check()
    cy.getDataCy('scratch').check()
    cy.getDataCy('other_block').check()
    cy.getDataCy('python').check()
    cy.getDataCy('other_text').check()

    // teacher connect
    cy.getDataCy('subscribe').check()
    cy.getDataCy('pair_with_teacher').check()
    cy.getDataCy('connect_guest_teacher').check()
    // phone will open when connect_guest_teacher is checked
    cy.getDataCy('phone').type('0612345678')
  
    cy.getDataCy('agree_terms').check()
    cy.getDataCy('submit_button').click()
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.env('landing_page'));
    
    //delete profile
    goToProfilePage();
    cy.getDataCy('personal_settings').click()
    cy.getDataCy('delete_profile_button').click()
    cy.getDataCy('modal_yes_button').click()
  })
})
