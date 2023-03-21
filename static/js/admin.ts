export interface InitializeAdminUsersPageOptions {
  readonly page: 'admin-users';
}

export function initializeAdminUserPage(_options: InitializeAdminUsersPageOptions) {
  $('.attribute').change(function() {
      const attribute = $(this).attr('id');
      if(!(this as HTMLInputElement).checked) {
          $('#' + attribute + '_header').hide();
          $('.' + attribute + '_cell').hide();
      } else {
          $('#' + attribute + '_header').show();
          $('.' + attribute + '_cell').show();
      }
  });
  // Todo TB: Not sure why I wrote this code here instead of in a .ts file -> re-structure this someday (08-22)
  $('#admin_filter_category').change(function() {
      $('.filter_input').hide();
      if ($('#admin_filter_category').val() == "email" || $('#admin_filter_category').val() == "username") {
          $('#email_filter_input').show();
      } else if ($('#admin_filter_category').val() == "language") {
          $('#language_filter_input').show();
      } else if ($('#admin_filter_category').val() == "keyword_language") {
          $('#keyword_language_filter_input').show();
      } else {
          $('#date_filter_input').show();
      }
  });

  $('#next_page_btn').click(function() {
      // Copy the token into the hidden input field, then submit the form
      var token = $('#next_page_btn').data('page_token');
      console.log(token);
      $('#hidden-page-input').attr('value', token);
      $('#filterform').submit();
  });
}