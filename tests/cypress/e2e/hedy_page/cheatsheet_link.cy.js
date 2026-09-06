import { goToHedyLevel } from "../tools/navigation/nav";

describe('Cheatsheet link in level dropdown', () => {
  it('shows a cheatsheet link for every level', () => {
    goToHedyLevel(1);

    cy.get('[id^="level_"][id$="_adventures"]').each(($el) => {
      const match = $el.attr('id').match(/^level_(\d+)_adventures$/);
      if (match) {
        const level = parseInt(match[1]);
        cy.wrap($el).find(`li[onclick*="/cheatsheet/${level}"]`).should('exist');
      }
    });
  });
});
