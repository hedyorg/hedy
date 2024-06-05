import {loginForTeacher} from '../../../tools/login/login.js'
import { navigateToClass } from "../../../tools/classes/class.js";

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
    it(`Is able to see copy link to add student to class for ${teacher}`, () => {
        loginForTeacher();
        navigateToClass();
        cy.getDataCy('add_student').click();
        cy.getDataCy('copy_join_link').should('be.visible').should('be.enabled').click();
    })
})
