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
    return goToPage('/#');
}

export function goToRegister()
{
    return goToPage('/signup?teacher=false');
}

export function goToLogin()
{
    return goToPage("/login");
}

export default {goToPage, goToRegister}