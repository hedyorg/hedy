import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure, goToTeachersPage} from '../../tools/navigation/nav.js'
import { createAdventure } from '../../tools/adventures/adventure.js'

describe('Tests for customize adventure page', () => {
  
  beforeEach(() => {
    loginForTeacher();
    goToEditAdventure();    
  })

  it('Can type into the customize adventure text area', () => {
    cy.getBySel('custom_adventure_content')
      .should('be.visible')
      .should('not.be.disabled')
      .clear()
      .should('have.value', '')
      .type('this is the content of this adventure \"!#@\'( )*$%\'123\"')
      .should('have.value', 'this is the content of this adventure \"!#@\'( )*$%\'123\"');
  })

  it('passes', () => {
    // Tests the first class out of all the classes we can add to
    // It does not matter which one we take (we choose the first one)
    // Disabling this test as we enable this functionality again
    //   cy.get(':nth-child(1) > .customize_adventure_class_checkbox')
    //     .should('be.visible')
    //     .should('not.be.disabled')
    //     .check()
    //     .should('be.checked')
    //     .uncheck()
    //     .should('not.be.checked');
  })
  
  it('A teacher can check and unchek to make their adventure public or not', () => {
    cy.get('#agree_public')
      .should('be.visible')
      .should('not.be.disabled')
      .check()
      .should('be.checked')
      .uncheck()
      .should('not.be.checked');
  })

  it('Clicking the go back to teachers page leads to the teachers page', () => {
    cy.getBySel('go_back_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
  })

  it('Can select a level in the dropdown menu', () => {
    // Tests level field interaction
    cy.get('#custom_adventure_level')
      .should('be.visible')
      .should('not.be.disabled')
      .select('1')
      .should('have.value', '1');
  })

  it('Can write values in the adventure name field', () => {
    // Tests name field interaction
    cy.get('#custom_adventure_name')
      .should('be.visible')
      .should('not.be.disabled')
      .clear()
      .should('be.empty')
      .type('some_name\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_name\"!#@\'( )*$%\'123\"');
  })

  it('Clicking the preview button shows a modal with the adventure preview', () => {
    cy.getBySel('modal-content')
      .should('not.be.visible');

    // opening preview
    cy.getBySel('preview_adventure_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();
    cy.getBySel('modal-content')
      .should('be.visible');

    
    // closing preview
    cy.get('#modal-preview-button')
      .should('not.be.disabled')
      .click();
    cy.getBySel('modal-content')
      .should('not.be.visible');
    cy.get('#modal-preview-button')
      .should('not.be.visible')
  })

  it('removes an adventure', ()=>{
    // Creating a new adventure to remove
    goToTeachersPage();
    cy.getBySel('create_adventure_button').click();
    let adventure = `test adventure ${Math.random()}`;
    cy.getBySel('modal-prompt-input').type(adventure);    
    cy.get('#modal-ok-button').click();

    // Testing removing adventure (clicking on remove and then on 'yes')
    cy.getBySel('remove_adventure_button')
      .click();

    cy.getBySel('modal-yes-button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    // back to for-teacher page
    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
    
    cy.getBySel('teacher_adventures')
      .should('not.contain', adventure);
  })


  describe('Tests involving the confirmation modal', () => {
    // The modal should only be visible for a short period
  
    beforeEach(() => {
      cy.get('#modal-confirm')
      .should('not.be.visible');
      cy.get('#modal_alert_container')
        .should('not.be.visible');
      cy.getBySel('modal_alert_text')
        .should('not.be.visible');
      cy.getBySel('modal-yes-button')
        .should('not.be.visible')
    })

    afterEach(() => {
      cy.wait(1000);
      cy.get('#modal-confirm')
      .should('not.be.visible');
      cy.get('#modal_alert_container')
        .should('not.be.visible');
      cy.getBySel('modal_alert_text')
        .should('not.be.visible');
      cy.getBySel('modal-yes-button')
        .should('not.be.visible')
    })
    
    it('clicks on the remove adventure button and then doesnt remove the adventure', () => {
      // Testing not removing adventure (clicking on remove and then on 'no')
      cy.getBySel('remove_adventure_button')
        .should('be.visible')
        .should('not.be.disabled')
        .should('have.attr', 'type', 'reset')
        .click();
  
      cy.get('#modal-confirm')
        .should('be.visible');
  
      cy.getBySel('modal-no-button')
        .should('be.visible')
        .should('not.be.disabled')
        .click();
    })

    it('the modal should disapear after clicking no on save adventure modal', () => {
      cy.getBySel('save_adventure_button')
        .click();
  
      cy.getBySel('modal-no-button')
        .should('be.visible')
        .should('not.be.disabled')
        .click();
    })

    it('Saves an adventure', () => {  
      cy.getBySel('save_adventure_button')
        .should('be.visible')
        .should('not.be.disabled')
        .should('have.attr', 'type', 'submit')
        .click();
  
      cy.get('#modal-confirm')
        .should('be.visible');
  
      cy.getBySel('modal-yes-button')
        .should('be.visible')
        .should('not.be.disabled')
        .click();
  
      cy.get('#modal_alert_container')
        .should('be.visible');
      cy.getBySel('modal_alert_text')
        .should('be.visible');    
    })
  })
})