import { modal, tryCatchPopup } from './modal';
import { join_class } from './teachers';
import { localLoadOnce, localSave } from './local';
import { postNoResponse, postJson } from './comm';

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
  return result;
}

function redirect(where: string) {
  where = '/' + where;
  window.location.pathname = where;
}

// *** User POST without data ***

export async function logout() {
  await postNoResponse('/auth/logout');
  window.location.reload();
}

// Todo TB: It might be nice to get a confirmation pop-up from the server instead with some secret key
// As with the current flow one can destroy an account by "accidentally" making an empty POST to /auth/destroy
export function destroy(confirmation: string) {
  modal.confirm (confirmation, async () => {
    await postNoResponse('/auth/destroy');
    redirect('');
  });
}

export function destroy_public(confirmation: string) {
  modal.confirm (confirmation, async () => {
    await postNoResponse('/auth/destroy_public');
    location.reload();
  });
}

export async function turn_into_teacher_account() {
  tryCatchPopup(async () => {
    const response = await postJson('/auth/turn-into-teacher');
    modal.notifySuccess(response.message);
    setTimeout (function () { redirect('for-teachers') }, 2000);
  });
}

export async function subscribe_to_newsletter() {
  tryCatchPopup(async () => {
    const response = await postJson('/auth/subscribe-to-newsletter');
    modal.notifySuccess(response.message);
    $('#subscribe_panel').hide();
    $('#subscribed_panel').show();
  });
}

// *** User forms ***

export function initializeFormSubmits() {
  $('form#signup').on('submit', async function (e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const body = convertFormJSON($(this))
      await postNoResponse('/auth/signup', body);      
      afterLogin({"first_time": true, "is_teacher": "is_teacher" in body});
    });
  });

  $('form#login').on('submit', function(e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const response = await postJson('/auth/login', convertFormJSON($(this)));
      if (response['first_time']) {
        return afterLogin({"first_time": true});
      }
      return afterLogin({"admin": response['admin'] || false, "teacher": response['teacher']} || false);
    });
  });

  $('form#profile').on('submit', function(e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const response = await postJson('/profile', convertFormJSON($(this)));
      if (response.reload) {
        modal.notifySuccess(response.message, 2000);
        setTimeout (function () {location.reload ()}, 2000);
      } else {
        modal.notifySuccess(response.message);
      }
  });
  });

  $('form#change_password').on('submit', function(e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const response = await postJson('/auth/change_password', convertFormJSON($(this)));
      modal.notifySuccess(response.message);
    });
  });

  $('form#recover').on('submit', function(e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const response = await postJson('/auth/recover', convertFormJSON($(this)));
      modal.notifySuccess(response.message);
      $('form#recover').trigger('reset');
    });
  });

  $('form#reset').on('submit', function(e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const response = await postJson('/auth/reset', convertFormJSON($(this)));
      modal.notifySuccess(response.message, 2000);
      $('form#reset').trigger('reset');
      setTimeout(function (){
        redirect ('login');
      }, 2000);
    });
  });

  $('form#public_profile').on('submit', function(e) {
    e.preventDefault();
    tryCatchPopup(async () => {
      const response = await postJson('/auth/public_profile', convertFormJSON($(this)));
      modal.notifySuccess(response.message, 2000);
      setTimeout(function () {
        location.reload()
      }, 2000);      
    });
  });

  // *** LOADERS ***

  $('#language').on('change', function () {
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

export function changeUserEmail(username: string, email: string) {
  modal.prompt ('Please enter the corrected email', email, async function (correctedEmail) {
    if (correctedEmail === email) return;
    try {
      await postJson('/admin/changeUserEmail', {
        username: username,
        email: correctedEmail
      });
      location.reload ();
    } catch {
      modal.notifyError(['Error when changing the email for user', username].join (' '));
    }
  });
}

export function edit_user_tags(username: string) {
  tryCatchPopup(async () => {
    const response = await postJson('/admin/getUserTags', {
      username: username
    });
    console.log(response);
    $('#modal_mask').show();
    $('#tags_username').text(username);
    $('.tags_input').prop('checked', false);
    if (response.tags) {
      console.log(response.tags);
      if (jQuery.inArray("certified_teacher", response.tags) !== -1) {
        $('#certified_tag_input').prop('checked', true);
      }
      if (jQuery.inArray("distinguished_user", response.tags) !== -1) {
        $('#distinguished_tag_input').prop('checked', true);
      }
      if (jQuery.inArray("contributor", response.tags) !== -1) {
        $('#contributor_tag_input').prop('checked', true);
      }
    }
    $('#modal_tags').show();
  });
}

export function update_user_tags() {
  tryCatchPopup(async () => {
    const username = $('#tags_username').text();
    const certified = $('#certified_tag_input').prop('checked');
    const distinguished = $('#distinguished_tag_input').prop('checked');
    const contributor = $('#contributor_tag_input').prop('checked');

    await postJson('/admin/updateUserTags', {
      username: username,
      certified: certified,
      distinguished: distinguished,
      contributor: contributor
    });

    $('#modal_mask').hide();
    $('#modal_tags').hide();
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
  if (url && !loginData['first_time']) {
    window.location = url;
    return;
  }

  const joinClassString = localStorage.getItem('hedy-join');
  const joinClass = joinClassString ? JSON.parse(joinClassString) : undefined;
  if (joinClass) {
    localStorage.removeItem('hedy-join');
    return join_class(joinClass.id, joinClass.name);
  }

  // If the user logs in for the first time and is a teacher -> redirect to the for teacher page
  if (loginData['first_time'] && loginData['is_teacher']) {
    return redirect('for-teachers');
  // If it's a student, send him to the first level
  } else if(loginData['first_time'] && !loginData['is_teacher']) {
    return redirect('hedy/1')
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
  redirect('');
}
