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

export function goToHedyLevel(level) {
    goToPage(`${Cypress.env('hedy_page')}/${level}#default`);
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
    cy.get('body').then(($body) => {
        if ($body.find('[data-cy^="edit_link_"]').length > 0) {
            cy.get('[data-cy^="edit_link_"]').first().invoke('attr', 'href').then((href) => {
                const adventureId = href.split('/').pop();
                cy.visit(`/for-teachers/legacy/customize-adventure/${adventureId}`);
            });
            return;
        }

        if ($body.find('#my-adventures-table a[href*="/for-teachers/customize-adventure/"]').length > 0) {
            cy.get('#my-adventures-table a[href*="/for-teachers/customize-adventure/"]').first().invoke('attr', 'href').then((href) => {
                const adventureId = href.split('/').pop();
                cy.visit(`/for-teachers/legacy/customize-adventure/${adventureId}`);
            });
            return;
        }

        cy.visit('/for-teachers/customize-adventure?name=autosave-temp&level=1');
        cy.location('pathname').then((pathname) => {
            const match = pathname.match(/customize-adventure\/([^/]+)/);
            if (match && match[1]) {
                cy.visit(`/for-teachers/legacy/customize-adventure/${match[1]}`);
            }
        });
    });
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

export function clickAdventureIndexButton()
{
    cy.getDataCy('dropdown_open_button').click();
}

export default {goToPage}

