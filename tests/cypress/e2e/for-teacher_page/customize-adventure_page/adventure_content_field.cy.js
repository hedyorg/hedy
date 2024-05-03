import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Adventure content Field test', () => {
  const data = 'this is the content of this adventure \"!#@\'( )*$%\'123\"';
  for (const teacher of ["teacher1", "teacher4"]) { 
    it(`passes: ${teacher}`, () => {
      loginForTeacher(teacher);
      goToEditAdventure();

      cy.window().then(win => {
        const editor = win.ckEditor;

        cy.get('.ck-editor__editable')
          .should('be.visible')
          .should('not.be.disabled')

        editor.setData(data);
        cy.get('.ck-editor__editable')
          .invoke('text')
          .should('eq', data);

      })
    })
  }
})
