import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

const teachers = ["teacher1", "teacher4"];
const data = 'this is the editor of this adventure \"!#@\'( )*$%\'123\"';
const data_warning = "<code>to</code>";

teachers.forEach((teacher) => {
  describe("Test customize adventure editor", () => {
    beforeEach(() => {
      loginForTeacher(teacher);
      goToEditAdventure();
    });

    it(`Is able to write code inside the editor for ${teacher}`, () => {
      cy.getDataCy('adventure').click();

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

    it('Is able to write a word with several possible keywords and close warning message', () => {
      cy.getDataCy('adventure').click();

      cy.window().then(win => {
          const editor = win.ckEditor;

          cy.get('.ck-editor__editable')
            .should('be.visible')
            .should('not.be.disabled');

          editor.setData(data_warning);
          cy.getDataCy('test_warning_message').should('be.visible').and('contain.text', 'to, to_list')
          cy.getDataCy('close_warning').click()
          cy.getDataCy('test_warning_message').should('not.exist')
        })
    })
  })
})
