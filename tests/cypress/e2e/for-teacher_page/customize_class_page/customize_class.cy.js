import { loginForTeacher, loginForStudent } from '../../tools/login/login.js'
import { navigateToClass, removeCustomizations, selectLevel } from "../../tools/classes/class";
import { goToHedyPage, clickAdventureIndexButton } from "../../tools/navigation/nav";

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
  describe(`customize class page for ${teacher}`, () => {
    beforeEach(() => {
      loginForTeacher(teacher);
      navigateToClass();
      removeCustomizations();
    });

    it('Is able to switch to level 2', () => {
      // We should be defaulted in level 1
      cy.getDataCy("level_1").should('be.visible');
      cy.getDataCy("level_2").should('not.exist');

      // Go to level 2 and check if we are now in level 2
      selectLevel('2');
      cy.getDataCy("level_2").should('be.visible');
      cy.getDataCy("level_1").should('not.exist');
    });

    it('Is able to open the opening date container, check the option checkboxes, fill in the dates and level disabled text should be visible', () => {
      cy.getDataCy('opening_date_container').should("not.be.visible")
      cy.getDataCy('opening_date_label').click();
      cy.getDataCy('opening_date_container').should("be.visible")

      // Level 1 should not have disabled message
      cy.getDataCy('level_1').should('be.visible');
      cy.getDataCy('state_disabled').should('not.be.visible');
      // The following line has a bug in cypress:
      // cy.getDataCy("opening_date_level_" + index).type("2023-01-01").should("have.value", "2023-01-01")
      // The following tests only checks if the field is not empty using a for loop:
      var levelarray = Array.from({length:4},(v, k)=>k+1) // is it necessary to run this for all 18 levels?
      cy.wrap(levelarray).each((index) => {
        cy.getDataCy("opening_date_level_" + index)
          .type("2023-01-01")
          .invoke('val').then((text) => {
            expect('2023-01-01').to.equal(text);
          });

          cy.getDataCy(`enable_level_${index}`).should('be.checked')
          cy.getDataCy(`enable_level_${index}`).parent('.switch').click();
          cy.getDataCy(`enable_level_${index}`).should('be.not.checked')
      });

      // Level 1 should have disabled message
      cy.getDataCy('state_disabled').should('be.visible');
    });

    it('Is able to remove adventure', () => {
      selectLevel('2');
      // Make sure that level 2 has been loaded
      cy.getDataCy('level_2');

      // The available adventures dropdown should only include the default option
      // but it may also have teacher-specific adventures
      cy.getDataCy("available_adventures_current_level")
        .children()
        .then($children => $children.length)
        .as('startLength')
        .then(startLength => {
          // store the name of the adventure we're going to delete
          cy.get('[data-cy="level_2"] div:first input')
            .invoke('attr', 'value')
            .as('adventure')
            .then(adventure => {
              // Get the first adventure, and click its remove button
              cy.getDataCy(`hide_adv_${adventure}`).click();

              // The available adventures dropdown should now include the new adventure
              cy.getDataCy("available_adventures_current_level")
                .children()
                .should('have.length', startLength + 1);

              // after selecting the adventure, it shouldn't be among the options
              cy.getDataCy('available_adventures_current_level').select(`${adventure}`)

              cy.getDataCy('available_adventures_current_level')
                .children()
                .should('have.length', startLength);

              // the adventure should now be last
              cy.getDataCy(`level_2 ${adventure}`).should("exist")
          });
      });
    });

    it('Is able to reset the adventures and create a new adventure', () => {
      // At first, the Parrot adventure should be in the level 1's adventures

      selectLevel('1');
      cy.getDataCy('htmx_modal').should('not.exist');
      cy.getDataCy(`hide_adv_parrot`).click();
      cy.getDataCy('parrot').should('not.exist');

      cy.getDataCy('reset_adventures').click();
      cy.getDataCy('confirm_modal').should('be.visible');
      cy.getDataCy('htmx_modal_yes_button').click();
      cy.getDataCy('parrot').should('be.visible');

      const new_adventure = "test_new_adventure"
      cy.getDataCy('edit_link').click();
      cy.getDataCy('custom_adventure_name')
      .clear()
      .type(new_adventure)
      // TODO check if adventure is added to class and level correctly
    });

    it('Is able to be re-added from the right dropdown list', () => {
      const hiddenAdventure = 'parrot';
      selectLevel('1');
      cy.getDataCy(`hide_adv_${hiddenAdventure}`).click();

      cy.getDataCy(`${hiddenAdventure}`).should('not.exist');

      cy.getDataCy('available_adventures_current_level').children(`*[value='${hiddenAdventure}']`).should('exist');
      cy.getDataCy('available_adventures_current_level').select(`${hiddenAdventure}`);
      cy.getDataCy(`${hiddenAdventure}`).should('exist');
      cy.wait(500);

      // should be visible for a student
      loginForStudent();
      goToHedyPage();
      clickAdventureIndexButton();
      cy.getDataCy('parrot').should('be.visible');
    });

    //commenting this out because the for each takes time.
    // it('FIXME: selects two adventures and swaps them using drag and drop', () => {
      /**
       * FIXME: Since We changed the library that handles the drag and drop,
       * this test is harder to make into work, since the Cypress documentation,
       * and the documentation of the library are no use.
       */

      /*
      // Click on level 1
      selectLevel('1');
      // Now it should be visible
      cy.getDataCy('level_1').should('be.visible');
      // Get the first and second adventure
      cy.getDataCy('level_1')
        .children()
        .eq(0)
        .invoke('attr', 'value')
        .as('first_adventure');
      cy.getDataCy('level_1')
        .children()
        .eq(1)
        .invoke('attr', 'value')
        .as('second_adventure');
      // Getting their values first, and then moving them around
      cy.get('@first_adventure').then(first_adventure => {
        cy.get('@second_adventure').then(second_adventure => {
          // Move the second adventure to the first place
          cy.getDataCy('level_1')
            .children()
            .eq(1)
            .trigger('dragstart')
          cy.getDataCy('level_1')
            .children()
            .eq(0)
            .trigger('drop')
            .trigger('dragend');
          // they should be inverted now
          cy.getDataCy('level_1')
            .children()
            .eq(0)
            .should('have.value', second_adventure);
          cy.getDataCy('level_1')
            .children()
            .eq(1)
            .should('have.value', first_adventure);
        })
      })
    */
    // });
  });
});


