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
    return goToPage('/');
}

export function goToRegisterStudent()
{
    return goToPage(Cypress.env('register_student_page'));
}

export function goToRegisterTeacher()
{
    return goToPage(Cypress.env('register_teacher_page'));
}

export function goToLogin()
{
    return goToPage(Cypress.env('login_page'));
}

export function goToRecover()
{
    return goToPage(Cypress.env('recover_page'));
}

export function goToTeachersPage()
{
    return goToPage(Cypress.env('teachers_page'));
}

export function goToHedyPage()
{
    return goToPage(Cypress.env('hedy_page'));
}

export default {goToPage}
