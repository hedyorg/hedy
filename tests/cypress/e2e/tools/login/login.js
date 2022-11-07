import { goToHome, goToLogin } from "../navigation/nav";

// Setups the database with 3 registered accounts
// [account type]: [username] [password]
// - Admin account: admin_user useruser
// - Teacher account: teacher_user useruser
// - Student account: student_user useruser
export function setupDatabase() {
    cy.writeFile("../dev_database.json", "{  \"program-stats\": [    {      \"id#level\": \"@all-anonymous#1\",      \"week\": \"2022-38\",      \"id\": \"@all-anonymous\",      \"level\": 1,      \"MissingCommandException\": 1,      \"IncompleteCommandException\": 2,      \"successful_runs\": 4    }  ],  \"users\": [    {      \"username\": \"teacher_user\",      \"password\": \"$2b$09$vkF36em4O5M8MHooarkzL.FRZeFyk39owlmR9UQSbYL5MofschUei\",      \"email\": \"teacher_user@user.com\",      \"language\": \"en\",      \"keyword_language\": \"en\",      \"created\": 1666010820398,      \"third_party\": null,      \"verification_pending\": \"$2b$09$eYSVtBhb/Ig6k4oFQvb3qeOZwhezaDme3z46SqyidVUCwKpj3DubC\",      \"last_login\": 1666012349019,      \"country\": \"NL\",      \"birth_year\": 2001,      \"gender\": \"m\",      \"epoch\": 1,      \"is_teacher\": 1    },    {      \"username\": \"admin_user\",      \"password\": \"$2b$09$Gj4Lz5mvboIo84Cdxe8WT.sDDD6lDyfHjc9/.Mz8YUW8w/dh3bKZ.\",      \"email\": \"admin_user@user.com\",      \"language\": \"en\",      \"keyword_language\": \"en\",      \"created\": 1666010862655,      \"third_party\": null,      \"verification_pending\": \"$2b$09$qKGKB0SurPy/Y.Ax17zhy.J4pUkcnWF11w1ZJ6ryz5l2WUvDe8tw2\",      \"last_login\": 1667741037667,      \"country\": \"NL\",      \"birth_year\": 2001,      \"gender\": \"m\",      \"epoch\": 1    },    {      \"username\": \"student_user\",      \"password\": \"$2b$09$bx8wJanXvmy7Hm.bfHlQNeassxsCE9pQdyFRkEDYBDvpH5iau/VFK\",      \"email\": \"student_user@user.com\",      \"language\": \"en\",      \"keyword_language\": \"en\",      \"created\": 1667741153672,      \"teacher_request\": null,      \"third_party\": null,      \"verification_pending\": \"$2b$09$5aJCMoRi2PJiyOf6MthY8OQgKu2trUeUL7MjuqGQuaQaiDHpCCAYO\",      \"last_login\": 1667741153672,      \"country\": \"NL\",      \"birth_year\": 2000,      \"gender\": \"o\",      \"prog_experience\": \"no\",      \"epoch\": 1    }  ],  \"tokens\": []}")
}

export function loginForAdmin() {
    login("admin_user", "useruser");
}

export function loginForTeacher() {
    login("teacher_user", "useruser");
}

export function loginForStudent() {
    login("student_user", "useruser");
}

export function login(username, password) {
    goToLogin();
    cy.get('#username').type(username);
    cy.get("#password").type(password);
    cy.get('#login > .green-btn').click();
}

export function logout()
{
    goToHome();            
    cy.get("body").then($body => {
        if ($body.find(".menubar-text:contains('Log in')").length == 0) {   
            
            cy.get('.dropdown > .menubar-text').click();
            cy.get(':nth-child(4) > .dropdown-item').click();
            cy.wait(500);
            
        } 
    });
}

export default {loginForAdmin, loginForTeacher};
