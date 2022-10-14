export function goToPage(page)
{
    if (typeof page === 'string' || page instanceof String)
    {
        let url = Cypress.env('base_url');
        if(url != "")
        {
            cy.visit(url + page);
        }
        else
        {
            cy.visit('http://localhost:8080' + page);
        }
        
    }
}

export function goToHome()
{
    return goToPage('/#');
}

export function goToRegister()
{
    return goToPage('/signup');
}

export default {goToPage, goToRegister}