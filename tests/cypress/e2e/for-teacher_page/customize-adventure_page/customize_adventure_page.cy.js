import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'
import "cypress-real-events"

it('Test for the Customize Adventure Page: writing a word with several possible keywords should show an alert message, that can be closed', () => {
  loginForTeacher();
  goToEditAdventure();

  cy.window().then(win => {
      const editor = win.ckEditor;
      cy.get('.ck-editor__editable')
        .should('be.visible')
        .should('not.be.disabled');
      const data = "<code>to</code>";
      editor.setData(data);
      cy.getDataCy('test_warning_message').should('be.visible').and('contain.text', 'to, to_list')
      // Once we click the close button
      cy.get('div[data-cy="test_warning_message"] > p[class="close-dialog"]').click()
      // The alert should not exist anymore
      cy.getDataCy('test_warning_message').should('not.exist')
    })
})
