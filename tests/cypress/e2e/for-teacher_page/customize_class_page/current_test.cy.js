import { loginForTeacher, loginForStudent } from '../../tools/login/login.js'
import { ensureClass } from "../../tools/classes/class.js";

describe('customize class page', () => {
    let className;
    beforeEach(async () => {
      loginForTeacher();
      className = await ensureClass();
      cy.getBySel('view_class_link').first().click(); // Press on view class button
      cy.getBySel('customize_class_button').click(); // Press customize class button
      // Remove any customizations that already exist to get the class into a predictable state
      // This always throws up a modal dialog      
      cy.getBySel('remove_customizations_button').click({ force: true });
      cy.getBySel('modal_yes_button').click();      
    });
    
    describe('an adventure that is hidden', () => {
      const hiddenAdventure = 'parrot';

      beforeEach(() => {
        selectLevel('1');
        cy.get(`*[data-cy="level-1"] div[data-cy='${hiddenAdventure}'] *[data-cy="hide"]`).click();
      });

      it('disappears from the tab list', () => {
        cy.get(`input[value="${hiddenAdventure}"]`).should('not.exist');
      });

      it('can be re-added from the right dropdown list', () => {
        cy.getBySel('available_adventures_current_level').children(`*[value='${hiddenAdventure}']`).should('exist');

        cy.getBySel('available_adventures_current_level').select(`${hiddenAdventure}`);

        cy.get(`div[data-cy="${hiddenAdventure}"]`).should('be.visible');
      });

      it('becomes invisible for the student', () => {
        // FIXME: This test is hard to write, as I'd like to invite `student1`
        // to the class, but inviting existing students takes a lot of steps...

        // loginForStudent();
      });
    });
});

function selectLevel(level) {
  cy.getBySel("adventures")
    .select(level, {force: true})
    .select(level, {force: true})
    .should('have.value', level);
}