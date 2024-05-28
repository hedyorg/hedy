import { loginForAdmin } from "../login/login";

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

export function goToRegisterStudent()
{
    goToPage(Cypress.env('register_student_page'));
}

export function goToRegisterTeacher()
{
    goToPage(Cypress.env('register_teacher_page'));
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
    cy.get("#adventures_table").then($viewAdventure => {
        if (!$viewAdventure.is(':visible')) {
            cy.get("#view_adventures").click();
        }
    });
    cy.get('#adventures_table tbody > :nth-child(1) [data-cy="edit-link"]')
      .click();
}

export function goToExploreProgramsPage()
{
   goToPage(Cypress.env('explore_programs_page'));
}

export default {goToPage}
