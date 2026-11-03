import { goToProfilePage } from '../navigation/nav.js'

export function makeProfilePublic() {
    goToProfilePage();
    cy.getDataCy('profile_button').click();
    cy.getDataCy('personal_text').type('updating profile to be public');
    cy.getDataCy('agree_terms').check();  // May start out checked, in which case 'click()' would undo the check!
    cy.getDataCy('submit_public_profile').click();
}