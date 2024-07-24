import { loginForAdmin } from "../login/login";
import { openAdventureView } from '../../tools/adventures/adventure.js';

export function goToPage(page)
{
    if (typeof page === 'string' || page instanceof String)
    {
        if(page != "")
        {
            cy.visit(page);
        }

    }
}

export function goToHome()
{
    goToPage('/');
}

export function goToSignup()
{
    goToPage(Cypress.env('signup_page'));
}

export function goToLogin()
{
    goToPage(Cypress.env('login_page'));
}

export function goToRecover()
{
    goToPage(Cypress.env('recover_page'));
}

export function goToTeachersPage()
{
    goToPage(Cypress.env('teachers_page'));
}

export function goToHedyPage()
{
    goToPage(Cypress.env('hedy_page'));
}

export function goToHedyPageWithEnKeywords()
{
    goToPage(Cypress.env('hedy_english_keywords'));
}

export function goToAdventurePage()
{
    goToPage(Cypress.env('adventure_page'));
}

export function goToProfilePage()
{
    goToPage(Cypress.env('profile_page'));
}

export function goToHedyLevel2Page()
{
    goToPage(Cypress.env('hedy_level2_page'));
}

export function goToHedyLevel5Page()
{
    goToPage(Cypress.env('hedy_level5_page'));
}

export function goToAdminUsersPage()
{
    loginForAdmin();
    cy.get('#users_button').click();
}

export function goToAdminAdventuresPage()
{
   goToPage(Cypress.env('admin_adventures_page'));
}

export function goToAdminAchievementsPage()
{
   goToPage(Cypress.env('admin_achievements_page'));
}

export function goToAdminClassesPage()
{
   goToPage(Cypress.env('admin_classes_page'));
}

// Must be logged in and able to edit an adventure
export function goToEditAdventure()
{
    goToTeachersPage();

    // takes the first adventures and goes to its edit page
    // It does not matter which adventure we take (we choose the first one)
    openAdventureView();
    cy.getDataCy("edit_link_adventure").first().click();
}

export function goToExploreProgramsPage()
{
   goToPage(Cypress.env('explore_programs_page'));
}

export function goToProgramsPage()
{
   goToPage(Cypress.env('programs_page'));
}

export function navigateHomeButton(button, path)
{
    goToHome();
    cy.getDataCy(button).click();
    cy.location().should((loc) => {
      expect(loc.pathname).equal(path);
    })
}

export function goToSubscribePage()
{
   goToPage(Cypress.env('subscribe_page'));
}

export function goToHedyPageAdventure(adventure)
{
    goToHedyPage();
    cy.getDataCy('dropdown_adventure_button').click();
    cy.wait(1000);
    cy.getDataCy('adventure_dropdown').should('be.visible');
    cy.getDataCy(`adventure_button_${adventure}`).scrollIntoView();
    cy.wait(1000);
    cy.getDataCy(`adventure_button_${adventure}`).should('be.visible');
    cy.getDataCy(`adventure_button_${adventure}`).click();
}

export default {goToPage}
