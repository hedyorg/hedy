import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigate_home_button } from "../tools/navigation/nav";

describe('Navigation buttons', () => {
  it('When not logged in: Is able to click all menubar buttons', () => {
    navigate_home_button('hedy_button', '/hedy')
    navigate_home_button('explore_button', '/login')
  })

  it('As a teacher: Is able to click all menubar buttons', () => {
    loginForTeacher();
    navigate_home_button('hedy_button', '/hedy')
    navigate_home_button('explore_button', '/explore')
    navigate_home_button('for_teacher_button', '/for-teachers')
    navigate_home_button('manual_button', '/for-teachers/manual')
    navigate_home_button('programs_button', '/programs')
  })

  it('As a student: Is able to click all menubar buttons', () => {
    loginForStudent();
    navigate_home_button('hedy_button', '/hedy')
    navigate_home_button('explore_button', '/explore')
    not_navigate_home_button('for_teacher_button')
    not_navigate_home_button('manual_button')
    navigate_home_button('programs_button', '/programs')
  })

  it('As a user: Is able to click all menubar buttons', () => {
    loginForUser();
    navigate_home_button('hedy_button', '/hedy')
    navigate_home_button('explore_button', '/explore')
    not_navigate_home_button('for_teacher_button')
    not_navigate_home_button('manual_button')
    navigate_home_button('programs_button', '/programs')
  })
})

function not_navigate_home_button(button)
{
    goToHome();
    cy.getDataCy(button).should('not.exist');
}