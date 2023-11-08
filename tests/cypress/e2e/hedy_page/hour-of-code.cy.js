
import {goToPage} from "../tools/navigation/nav";

// The rest of the tests of the hedy_page applies on the hour-of-code, the subset is an additional feature.
const subsetsPerLevel = {1: ["print_command", "parrot"], 6: ["is_command", "maths", "dice", "dishes" ]}
describe("Testing subset passed through the URL", () => {
    for (const level of Object.keys(subsetsPerLevel)) {
        const subset = subsetsPerLevel[level]
        it(`Level ${level} should have ${subset.length} adventures + quiz`, () => {
            goToPage(`/hour-of-code/${level}?subset=${subset.join(",")}`)
            cy.get(".tab").should("have.length", subset.length + 1)
        })
    }
})