import {loginForTeacher} from '../../tools/login/login.js'

it('Is able to see copy link to add student to class', () => {
    loginForTeacher();
    cy.wait(500);
    
    openClassView();
    cy.getDataCy('view_class_link').first().click();
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())
    cy.getDataCy('add_student').click();
    cy.getDataCy('copy_join_link').should('be.visible').should('be.enabled').click();
})
