import {loginForTeacher, logout, login} from '../../tools/login/login.js'

it('Is able to add student by name', () => {
    loginForTeacher();
    let student = 'student5'

    cy.getDataCy('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getDataCy('view_classes').click();
      }
    });
    cy.getDataCy('view_class_link').first().click();
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())

    // delete student if in class
    cy.getDataCy('class_user_table').then(($div) => {
        if ($div.text().includes(student)){
          cy.getDataCy('remove_student').first().click();
          cy.getDataCy('modal_yes_button').click();
        }
    })

    cy.wait(500);

    cy.getDataCy('add_student').click();

    cy.getDataCy('invite_student').click();
    cy.getDataCy('modal_prompt_input').type(student);
    cy.getDataCy('modal_ok_button').click();

    cy.wait(500);
    login(student, "123456");

    cy.getDataCy('user_dropdown').click();
    cy.getDataCy('my_account_button').click();
    cy.getDataCy('join_link').click();

    logout();
    loginForTeacher();

    cy.getDataCy('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getDataCy('view_classes').click();
      }
    });
    cy.getDataCy('view_class_link').first().click();

    cy.getDataCy('student_username_cell').should(($div) => {
      const text = $div.text()
      expect(text).include('student5');
    })
})
