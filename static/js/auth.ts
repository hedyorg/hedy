import { modal } from './modal';
import { join_class } from './teachers';
import { showAchievements } from './app';
import { localLoadOnce, localSave } from './local';

const REDIRECT_AFTER_LOGIN_KEY = 'login-redirect';

// *** Utility functions ***

interface Dict<T> {
  [key: string]: T;
}

/**
 * Links to the login page redirect back to the page you come from,
 * by storing the origin address in localstorage (because our login
 * form works via JavaScript/AJAX).
 */
export function initializeLoginLinks() {
  $('a[href="/login"]').on('click', () => {
    comeBackHereAfterLogin();
    // Allow the default navigation operation
  });
}

export function comeBackHereAfterLogin() {
  localSave(REDIRECT_AFTER_LOGIN_KEY, {
    url: window.location.toString(),
  });
}

function convertFormJSON(form: JQuery<HTMLElement>) {
  let result : Dict<any> = {};
  $.each($(form).serializeArray(), function() {
    if (result[this.name]) {
      // If this value already exists it's most likely a check button: store all selected ones in an Array
      if ($.isArray(result[<string>this.name])) {
        result[this.name] = $.merge(result[this.name], Array(this.value));
      } else {
        result[this.name] = $.merge(Array(result[this.name]), Array(this.value));
      }
    } else {
      // Only add the current field to the JSON object if it actually contains a value
      if ((this.value)) {
        result[this.name] = this.value;
      }
    }
  });
  return JSON.stringify(result);
}

function redirect(where: string) {
  where = '/' + where;
  window.location.pathname = where;
}

// *** User POST without data ***

export async function logout() {
  $.ajax ({
    type: 'POST',
    url: '/auth/logout'
  }).done (function () {
    window.location.reload();
  });
}

// Todo TB: It might be nice to get a confirmation pop-up from the server instead with some secret key
// As with the current flow one can destroy an account by "accidentally" making an empty POST to /auth/destroy
export function destroy(confirmation: string) {
  modal.confirm (confirmation, function () {
    $.ajax ({
      type: 'POST',
      url: '/auth/destroy'
    }).done (function () {
      redirect('');
    });
  });
}

export function destroy_public(confirmation: string) {
  modal.confirm (confirmation, function () {
    $.ajax ({
      type: 'POST',
      url: '/auth/destroy_public'
    }).done (function () {
      redirect ('my-profile');
    });
  });
}

export function request_teacher_account() {
  $.ajax ({
      type: 'GET',
      url: '/auth/request_teacher'
    }).done (function (response) {
      modal.notifySuccess(response.message);
      setTimeout (function () {location.reload ()}, 2000);
    }).fail (function (response) {
      modal.notifyError(response.responseText);
  });
}

// *** User forms ***

export function initializeFormSubmits() {
  $('form#signup').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
          type: 'POST',
          url: '/auth/signup',
          // This should do the magic to convert to a correct JSON object
          data: convertFormJSON($(this)),
          contentType: 'application/json; charset=utf-8'
        }).done (function () {
          afterLogin({"first_time": true});
        }).fail (function (response) {
          modal.notifyError(response.responseText);
        });
  });

  $('form#login').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
      type: 'POST',
      url: '/auth/login',
      data: convertFormJSON($(this)),
      contentType: 'application/json; charset=utf-8'
    }).done (function (response) {
      if (response['first_time']) {
        return afterLogin({"first_time": true});
      }
      return afterLogin({"admin": response['admin'] || false, "teacher": response['teacher']} || false);
    }).fail (function (response) {
      modal.notifyError(response.responseText);
    });
  });

  $('form#profile').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
      type: 'POST', url: '/profile',
      data: convertFormJSON($(this)),
      contentType: 'application/json; charset=utf-8'
    }).done (function (response) {
      if (response.reload) {
        modal.notifySuccess(response.message, 2000);
        setTimeout (function () {location.reload ()}, 2000);
      } else {
        modal.notifySuccess(response.message);
      }
    }).fail (function (response) {
      modal.notifyError(response.responseText);
    });
  });

  $('form#change_password').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
      type: 'POST',
      url: '/auth/change_password',
      data: convertFormJSON($(this)),
      contentType: 'application/json; charset=utf-8'
    }).done (function (response) {
      modal.notifySuccess(response.message);
      $('form#change_password').trigger('reset');
    }).fail (function (response) {
      modal.notifyError(response.responseText);
    });
  });

  $('form#recover').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
      type: 'POST', url: '/auth/recover',
      data: convertFormJSON($(this)),
      contentType: 'application/json; charset=utf-8'
    }).done (function (response) {
      modal.notifySuccess(response.message);
      $('form#recover').trigger('reset');
    }).fail (function (response) {
      modal.notifyError(response.responseText);
    });
  });

  $('form#reset').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
      type: 'POST', url: '/auth/reset',
      data: convertFormJSON($(this)),
      contentType: 'application/json; charset=utf-8'
    }).done (function (response) {
      modal.notifySuccess(response.message, 2000);
      $('form#reset').trigger('reset');
      setTimeout(function (){
        redirect ('login');
      }, 2000);
    }).fail (function (response) {
      modal.notifyError(response.responseText);
    });
  });

  $('form#public_profile').on('submit', function(e) {
    e.preventDefault();
    $.ajax ({
      type: 'POST',
      url: '/auth/public_profile',
      data: convertFormJSON($(this)),
      contentType: 'application/json; charset=utf-8'
    }).done (function (response) {
      modal.notifySuccess(response.message, 2000);
      if (response.achievement) {
        showAchievements(response.achievement, true, "");
      } else {
        setTimeout(function () {
          location.reload()
        }, 2000);
      }

    }).fail (function (response) {
      return modal.notifyError(response.responseText);
    });
  });

  // *** LOADERS ***

  $("#language").on('change', function () {
      const lang = $(this).val();
      $('#keyword_language').val("en");
      if (lang == "en" || !($('#' + lang + '_option').length)) {
        $('#keyword_lang_container').hide();
      } else {
        $('.keyword_lang_option').hide();
        $('#en_option').show();
        $('#' + lang + '_option').show();
        $('#keyword_lang_container').show();
      }
  });

}

// *** Admin functionality ***

export function markAsTeacher(checkbox: any, username: string, is_teacher: boolean, pending_request: boolean) {
  $(checkbox).prop('checked', false);
  let text = "Are you sure you want to remove " + username + " as a teacher?";
  if (is_teacher) {
    text = "Are you sure you want to make " + username + " a teacher?";
  }
  modal.confirm (text, function () {
    $.ajax({
      type: 'POST',
      url: '/admin/markAsTeacher',
      data: JSON.stringify({
        username: username,
        is_teacher: is_teacher
      }),
      contentType: 'application/json; charset=utf-8'
    }).done(function () {
      location.reload();
    }).fail(function () {
      modal.notifyError(['Error when', is_teacher ? 'marking' : 'unmarking', 'user', username, 'as teacher'].join(' '));
    });
  }, function () {
    // If there is a pending request, we decline the modal -> remove the teacher request
    if (pending_request) {
      $.ajax({
        type: 'POST',
        url: '/admin/markAsTeacher',
        data: JSON.stringify({
          username: username,
          is_teacher: false
        }),
        contentType: 'application/json; charset=utf-8'
      }).done(function () {
        location.reload();
      });
    }
  });
}

export function changeUserEmail(username: string, email: string) {
  modal.prompt ('Please enter the corrected email', email, function (correctedEmail) {
    if (correctedEmail === email) return;
    $.ajax ({
      type: 'POST',
      url: '/admin/changeUserEmail',
      data: JSON.stringify ({
        username: username,
        email: correctedEmail
      }),
      contentType: 'application/json; charset=utf-8'
    }).done (function () {
      location.reload ();
    }).fail (function () {
      modal.notifyError(['Error when changing the email for user', username].join (' '));
    });
  });
}

export function edit_user_tags(username: string) {
  $.ajax({
    type: 'POST',
    url: '/admin/getUserTags',
    data: JSON.stringify({
      username: username
    }),
    contentType: 'application/json; charset=utf-8'
  }).done(function (response) {
    console.log(response);
    $('#modal-mask').show();
    $('#tags_username').text(username);
    $('.tags-input').prop('checked', false);
    if (response.tags) {
      console.log(response.tags);
      if (jQuery.inArray("certified_teacher", response.tags) !== -1) {
        $('#certified-tag-input').prop('checked', true);
      }
      if (jQuery.inArray("distinguished_user", response.tags) !== -1) {
        $('#distinguished-tag-input').prop('checked', true);
      }
      if (jQuery.inArray("contributor", response.tags) !== -1) {
        $('#contributor-tag-input').prop('checked', true);
      }
    }
    $('#modal-tags').show();
  }).fail(function (response) {
    modal.notifyError(response.responseText);
  });
}

export function update_user_tags() {
  const username = $('#tags_username').text();
  const certified = $('#certified-tag-input').prop('checked');
  const distinguished = $('#distinguished-tag-input').prop('checked');
  const contributor = $('#contributor-tag-input').prop('checked');

  $.ajax({
    type: 'POST',
    url: '/admin/updateUserTags',
    data: JSON.stringify({
      username: username,
      certified: certified,
      distinguished: distinguished,
      contributor: contributor
    }),
    contentType: 'application/json; charset=utf-8'
  }).done(function () {
    $('#modal-mask').hide();
    $('#modal-tags').hide();
    modal.notifySuccess("Tags successfully updated");
  });
}

/**
 * After login:
 *
 * - Redirect to a stored URL if present in Local Storage.
 * - Check if we were supposed to be joining a class. If so, join it.
 * - Otherwise redirect to "my programs".
 */
async function afterLogin(loginData: Dict<boolean>) {
  const { url } = localLoadOnce(REDIRECT_AFTER_LOGIN_KEY) ?? {};
  if (url) {
    window.location = url;
    return;
  }

  const joinClassString = localStorage.getItem('hedy-join');
  const joinClass = joinClassString ? JSON.parse(joinClassString) : undefined;
  if (joinClass) {
    localStorage.removeItem('hedy-join');
    return join_class(joinClass.id, joinClass.name);
  }

  // If the user logs in for the first time -> redirect to the landing-page after signup
  if (loginData['first_time']) {
    return redirect('landing-page/1');
  }
  // If the user is an admin -> re-direct to admin page after login
  if (loginData['admin']) {
    return redirect('admin');
  }

  // If the user is a teacher -> re-direct to for-teachers page after login
  if (loginData['teacher']) {
    return redirect('for-teachers');
  }
  // Otherwise, redirect to the programs page
  redirect('landing-page');
}