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

  $('.admin_pagination_btn').click(function(ev) {
      // Copy the token into the hidden input field, then submit the form
      var token = $(ev.target).data('page_token');
      console.log(token);
      $('#hidden_page_input').attr('value', token);
      $('#filterform').submit();
  });
}

export function filter_admin() {
    const params: Record<string, any> = {};
  
    const filter = $('#admin_filter_category').val();
    params['filter'] = filter;
  
    if ($('#hidden_page_input').val()) {
      params['page'] = $('#hidden_page_input').val();
    }
  
    switch (filter) {
      case 'email':
      case 'username':
        params['substring'] = $('#email_filter_input').val();
        break;
      case 'language':
        params['language'] = $('#language_filter_input').val();
        break;
      case 'keyword_language':
        params['keyword_language'] = $('#keyword_language_filter_input').val();
        break;
      default:
        params['start'] = $('#admin_start_date').val();
        params['end'] = $('#admin_end_date').val();
        break;
    }
  
    const queryString = Object.entries(params).map(([k, v]) => k + '=' + encodeURIComponent(v)).join('&');
    window.open('?' + queryString, '_self');
}