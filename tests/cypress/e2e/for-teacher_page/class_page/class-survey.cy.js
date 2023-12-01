import {loginForTeacher} from '../../tools/login/login.js'
import {createClassAndAddStudents} from '../../tools/classes/class.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

let classname;

beforeEach(() => {
    loginForTeacher("teacher4");
    ({classname} = createClassAndAddStudents());
    goToTeachersPage();
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
})

describe('Class Survey View', () => {
  it('Can first respond to 1 question, then to last 3 questions', () => {
    cy.get("#input").type("test");
    cy.get("#submit").click();
    goToTeachersPage();
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    var surveyInputs = Array.from({length:3},(v, k)=>k+1)
    cy.wrap(surveyInputs).each((index) => {
        cy.getBySel("input_" + index)
            .type("test")
            .invoke('val').then((text) => {
            expect('test').to.equal(text);
            });
        });
    cy.get("#submit").click();
    goToTeachersPage();
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.get("#survey").should('not.exist');
  })


  it('Can be skipped and survey is not shown after', () => {
    cy.get("#skip").click();
    goToTeachersPage();
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.get("#survey").should('not.exist');
  })

  it('Can be skipped and survey is not shown after', () => {
    cy.get("#remind_later").click();
    goToTeachersPage();
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.get("#survey").should('not.exist');
  })
})
