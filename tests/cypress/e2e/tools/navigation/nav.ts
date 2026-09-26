import { loginForAdmin } from "../login/login";
import { openAdventureView } from '../adventures/adventure.js';

export function goToPage(page: string, options = {}) {
    if (page != "") {
        cy.visit(page, options);
    }
}

export function goToHome() {
    goToPage('/');
}

export function goToSignup() {
    cy.env(['signup_page']).then(({signup_page}) => { goToPage(signup_page) });
}

export function goToLogin() {
    cy.env(['login_page']).then(({login_page}) => { goToPage(login_page) });
}

export function goToRecover() {
    cy.env(['recover_page']).then(({recover_page}) => { goToPage(recover_page) });
}

export function goToTeachersPage() {
    cy.env(['teachers_page']).then(({teachers_page}) => { goToPage(teachers_page) });
}

export function goToHedyPage(options = {}) {
    cy.env(['hedy_page']).then(({hedy_page}) => { goToPage(hedy_page, options); });
}

export function goToHedyPageWithEnKeywords() {
    cy.env(['hedy_english_keywords']).then(({hedy_english_keywords}) => { goToPage(hedy_english_keywords) });
}

export function goToAdventurePage() {
    cy.env(['adventure_page']).then(({adventure_page}) => { goToPage(adventure_page) });
}

export function goToProfilePage() {
    cy.env(['profile_page']).then(({profile_page}) => { goToPage(profile_page) });
}

export function goToHedyLevel(level: string | number) {
    cy.env(['hedy_page']).then(({ hedy_page }) => { goToPage(`${hedy_page}/${level}#default`); });
}

export function goToAdminUsersPage() {
    loginForAdmin();
    cy.env(['admin_users_page']).then(({admin_users_page}) => { goToPage(admin_users_page) });
}

export function goToAdminAdventuresPage() {
    cy.env(['admin_adventures_page']).then(({admin_adventures_page}) => { goToPage(admin_adventures_page) });
}

export function goToAdminAchievementsPage() {
    cy.env(['admin_achievements_page']).then(({admin_achievements_page}) => { goToPage(admin_achievements_page) });
}

export function goToAdminClassesPage() {
    cy.env(['admin_classes_page']).then(({admin_classes_page}) => { goToPage(admin_classes_page) });
}

// Must be logged in and able to edit an adventure
export function goToEditAdventure() {
    goToTeachersPage();

    // takes the first adventures and goes to its edit page
    // It does not matter which adventure we take (we choose the first one)
    openAdventureView();
    cy.get('body').then(($body) => {
        if ($body.find('[data-cy^="edit_link_"]').length > 0) {
            cy.get('[data-cy^="edit_link_"]').first().invoke('attr', 'href').then((href) => {
                const adventureId = href?.split('/').pop();
                cy.visit(`/for-teachers/legacy/customize-adventure/${adventureId}`);
            });
            return;
        }

        if ($body.find('#my-adventures-table a[href*="/for-teachers/customize-adventure/"]').length > 0) {
            cy.get('#my-adventures-table a[href*="/for-teachers/customize-adventure/"]').first().invoke('attr', 'href').then((href) => {
                const adventureId = href?.split('/').pop();
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

export function navigateHomeButton(button: string, path: string) {
    goToHome();
    cy.getDataCy(button).click();
    cy.location().should((loc) => {
        expect(loc.pathname).equal(path);
    })
}

export function goToSubscribePage() {
    cy.env(['subscribe_page']).then(({subscribe_page}) => { goToPage(subscribe_page) });
}

export function clickAdventureIndexButton() {
    cy.getDataCy('dropdown_open_button').click();
}

export default { goToPage }

