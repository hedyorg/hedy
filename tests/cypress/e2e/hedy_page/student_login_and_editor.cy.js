import { loginForStudent } from "../tools/login/login";
import { goToHedyLevel } from "../tools/navigation/nav";
import { codeEditorContent } from "../tools/programs/program";

describe('Student access to Hedy editor', () => {
  it('Make sure that the page is accessible for a student who is served old customizations', () => {
    loginForStudent('student1');

    goToHedyLevel(1);

    codeEditorContent().should('be.visible').and('not.be.disabled');

    codeEditorContent().click().type("print 'hello'{enter}");
  });
});
