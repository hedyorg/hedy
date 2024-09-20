import { goToSignup, goToProfilePage } from '../tools/navigation/nav.js'

beforeEach(() => {
  goToSignup();
})

describe('Test signing up', () => {
it('Is able to sign up as a student', () => {
    cy.getDataCy('signup_student').click()

    // basic info
    let student = `student_${Math.random()}`
    cy.getDataCy('username').type(student)
    cy.getDataCy('email').type(student + '@test.biz')
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
    cy.intercept('/auth/signup').as('sign_up');
    cy.getDataCy('submit_button').click()
    cy.wait('@sign_up').should('have.nested.property', 'response.statusCode', 200)
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.env('hedy_page'));
    
    // delete profile
    goToProfilePage();
    cy.getDataCy('personal_settings').click()
    cy.getDataCy('delete_profile_button').click()
    cy.intercept('/auth/destroy').as('delete_user')
    cy.getDataCy('modal_yes_button').click()
    cy.wait('@delete_user').should('have.nested.property', 'response.statusCode', 204)
    cy.url().should('contain', Cypress.config('baseUrl'));
  })

it('Is able to sign up as a teacher', () => {
    cy.clearCookies();
    cy.clearAllLocalStorage()
    cy.clearAllSessionStorage();  
    cy.getDataCy('signup_teacher').click()
    // basic info
    let username = `teacher_${Math.random()}`
    cy.getDataCy('username').type(username)
    cy.getDataCy('email').type(username + '@test.biz')
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
    cy.getDataCy('pair_with_teacher').check()
    cy.getDataCy('connect_guest_teacher').check()
    // phone will open when connect_guest_teacher is checked
    cy.getDataCy('phone').type('0612345678')
  
    cy.getDataCy('agree_terms').check()
    cy.intercept('/auth/signup').as('sign_up');
    cy.getDataCy('submit_button').click()
    cy.wait('@sign_up').should('have.nested.property', 'response.statusCode', 200)
    cy.url().should('contain', Cypress.env('teachers_page'));
    
    //delete profile
    goToProfilePage();
    cy.getDataCy('personal_settings').click()
    cy.getDataCy('delete_profile_button').click()
    cy.intercept('/auth/destroy').as('delete_user')
    cy.getDataCy('modal_yes_button').click()
    cy.wait('@delete_user').should('have.nested.property', 'response.statusCode', 204)
    cy.url().should('contain', Cypress.config('baseUrl'));
  })
})
