import { goToTeachersPage } from "../navigation/nav";

// https://onlinewebtutorblog.com/how-to-generate-random-string-in-jquery-javascript/
function generateRandomString(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

export function createClass()
{
    const classname = `test class ${generateRandomString(10)}`;
    
    goToTeachersPage();
    cy.wait(500);

    cy.get('#create_class_button').click();
    cy.get('#modal-prompt-input').type(classname);
    cy.get('#modal-ok-button').click();

    goToTeachersPage();
    cy.wait(500);
    
    return classname;
}

export function addStudents(classname, count) {
    const students = Array.from({length:count}, (_, index) => `student_${index}_${Math.random()}`) 

    goToTeachersPage();
    cy.wait(500);

    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.wait(500);

    cy.get('#add-student').click();
    cy.get('#create-accounts').click();
    cy.wrap(students).each((student, index) => {
      cy.get(`:nth-child(${(index + 2)}) > #username`).type(student);
      cy.get(`:nth-child(${(index + 2)}) > #password`).type('123456');
    })
    cy.get('#create_accounts_button').click();
    cy.get('#modal-yes-button').click();

    return students;
}

export function createClassAndAddStudents(){
    const classname = createClass();
    const students = addStudents(classname, 4);
    return {classname, students};
}

export default {createClassAndAddStudents};