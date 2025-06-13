
import {goToPage} from "../tools/navigation/nav";

// The rest of the tests of the hedy_page applies on the hour-of-code, the subset is an additional feature.
const subsetsPerLevel = {1: ["print_command", "parrot", "turtle", "debugging"], 6: ["songs", "dishes", "turtle", "debugging" ]}
describe("Testing subset passed through the URL", () => {
    for (const level of Object.keys(subsetsPerLevel)) {
        const subset = subsetsPerLevel[level]
        it(`Level ${level} should have ${subset.length} adventures`, () => {
            cy.visit(`/hour-of-code/${level}`);
            cy.get(`#level_${level}_adventures`).children().then(($children) => {
                const actual = [...$children].map(el => el.getAttribute('data-cy'));
                expect(actual).to.deep.equal(subset);
            })
        })

        it('has a tracking pixel', () => {
            goToPage(`/hour-of-code/${level}`)
            cy.get("#tracking_pixel").should("exist")
        })
    }
})