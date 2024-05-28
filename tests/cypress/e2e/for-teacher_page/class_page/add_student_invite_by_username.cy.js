import {loginForTeacher, logout, login} from '../../tools/login/login.js'

it('Is able to add student by name', () => {
    loginForTeacher();
    let student = 'student5'

    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.getBySel('view_class_link').first().click();
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())

    // delete student if in class
    cy.getBySel('class_user_table').then(($div) => {
        if ($div.text().includes(student)){
          cy.getBySel('remove_student').first().click();
          cy.getBySel('modal_yes_button').click();
        }
    })

    cy.wait(500);

    cy.getBySel('add_student').click();

    cy.getBySel('invite_student').click();
    cy.getBySel('modal_prompt_input').type(student);
    cy.getBySel('modal_ok_button').click();

    login(student, "123456");

    cy.getBySel('user_dropdown').click();
    cy.getBySel('my_account_button').click();
    cy.getBySel('join_link').click();

    logout();
    loginForTeacher();

    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.getBySel('view_class_link').first().click();

    cy.getBySel('student_username_cell').should(($div) => {
      const text = $div.text()
      expect(text).include('student5');
    })
})
