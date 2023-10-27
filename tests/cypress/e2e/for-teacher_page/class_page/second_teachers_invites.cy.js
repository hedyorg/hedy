import {loginForTeacher, logout} from "../../tools/login/login.js"
import { goToProfilePage } from "../../tools/navigation/nav";

const secondTeachers = ["teacher2", "teacher3"]
const invitesTable = body => body.find("#invites-block table")

describe("Second teachers: invitations", () => {
  it(`Invites ${secondTeachers.length} second teachers: by username`, () => {

    loginForTeacher();

    cy.wait(500);

    cy.get(".view_class").first().click();

    for (const teacher of secondTeachers) {
      cy.wait(500);
      
      cy.get("#add-second-teacher").click();
      
      // cy.get("#invite-student").click();
      // cy.wait(2000)
      cy.get("#modal-prompt-input").type(teacher);
      cy.get("#modal-ok-button").click();
      
      cy.wait(500);
      
      cy.get("body").then(invitesTable).then(table => {
        if (table.length) {
          table = cy.get("#invites-block table")
          cy.get("#invites-block .username_cell")
          .should('be.visible')
          .and("include.text", teacher)
        } else {
          cy.log("Second teacher not invited.")
        }
      })
    }
      //logout:
    // logout();
  })

  it(`Tries duplicating ${secondTeachers[0]}'s invitation`, () => {

    loginForTeacher()

    cy.get(".view_class").first().click();

    cy.wait(500);

    cy.get("#add-second-teacher").click();
    cy.get("#modal-prompt-input").type(secondTeachers[0]);
    cy.get("#modal-ok-button").click();
    cy.wait(500);

    cy.get("#modal_alert_container")
    .should('be.visible')
    .and("contain", "pending invitation")
  })

  it(`Accepts invitation sent to ${secondTeachers[0]}`, () => {
    loginForTeacher(secondTeachers[0])
    goToProfilePage()
    cy.get("#messages").should("exist")
    cy.get("#messages #join").click()
    logout();
  })

  it.only("Reads all second teachers", () => {
    loginForTeacher()
    cy.get(".view_class").first().click();
    cy.wait(500);
    cy.get("#second_teachers_container .username_cell").should("include.text", secondTeachers[0])
    logout()
  })

  it(`Deletes ${secondTeachers[1]}'s invitation`, () => {

    loginForTeacher();
    cy.wait(500);
    cy.get(".view_class").first().click();

    cy.get("body").then(invitesTable).then(table => {
      // if not, then no invitation.
      if (table.length) {
        table = cy.get("#invites-block table")
        console.log(table)
        table.should("exist")
        table.get(".remove_user_invitation").first().click()
        cy.wait(500);
        cy.get("#modal-yes-button").click();
      } else {
        cy.log("Second teacher not deleted.")
      }
    })
    
    cy.wait(500);
    cy.get('body').then(invitesTable).then(table => 
      table.length && cy.get("#invites-block table").should("not.contain", secondTeachers[0]))
    logout();
  })

})
