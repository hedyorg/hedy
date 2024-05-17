import {loginForTeacher, logout, login} from '../../tools/login/login.js'

it('Is able to add student by name', () => {
    loginForTeacher();
    let student = 'student5'

    cy.get('[data-cy="view_class_link"]').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get('[data-cy="view_classes"]').click();
      }
    });
    cy.get('[data-cy="view_class_link"]').first().click();
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())

    // delete student if in class
    cy.get('[data-cy="class_user_table"]').then(($div) => {
        if ($div.text().includes(student)){
          cy.get('[data-cy="remove_student"]').first().click();
          cy.get('[data-cy="modal_yes_button"]').click();
        }
    })

    cy.wait(500);

    cy.get('[data-cy="add_student"]').click();

    cy.get('[data-cy="invite_student"]').click();
    cy.get('[data-cy="modal_prompt_input"]').type(student);
    cy.get('[data-cy="modal_ok_button"]').click();

    login(student, "123456");

    cy.get('[data-cy="user_dropdown"]').click();
    cy.get('[data-cy="my_account_button"]').click();
    cy.get('[data-cy="join_link"]').click();

    logout();
    loginForTeacher();

    cy.get('[data-cy="view_class_link"]').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get('[data-cy="view_classes"]').click();
      }
    });
    cy.get('[data-cy="view_class_link"]').first().click();

    cy.get('[data-cy="student_username_cell"]').should(($div) => {
      const text = $div.text()
      expect(text).include('student5');
    })
})
