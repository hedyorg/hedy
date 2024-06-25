import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

const teachers = ["teacher1", "teacher4"];
const data = 'this is the content of this adventure \"!#@\'( )*$%\'123\"';

teachers.forEach((teacher) => {
  it(`Adventure content Field test for ${teacher}`, () => {
    loginForTeacher(teacher);
    goToEditAdventure();
    // navigate to the editor's view
    cy.getBySel("adventure").click();

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
})
