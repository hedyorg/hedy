import { modal } from './modal';
import { join_class } from './teachers';
import {saveitP, showAchievements} from './app';

export interface Profile {
  session_expires_at: number;
}

interface Dict<T> {
    [key: string]: T;
}

interface User {
  username?: string;
  email?: string;
  mail_repeat?: string;
  password?: string;
  password_repeat?: string;
  birth_year?: number;
  language?: string,
  keyword_language?: string,
  country?: string;
  gender?: string;
  subscribe?: string;
  agree_terms?: string;
  agree_third_party?: string;
  prog_experience?: 'yes' | 'no';
  experience_languages?: string[];
  is_teacher?: string;
}

interface UserForm {
  username?: string;
  email?: string;
  token?: string;
  password?: string;
  birth_year?: string;
  language?: string,
  keyword_language?: string,
  country?: string;
  gender?: string;
  subscribe?: string;
  agree_terms?: string;
  mail_repeat?: string;
  password_repeat?: string;
  old_password?: string;
}

export const auth = {
  profile: undefined as (Profile | undefined),
  reset: undefined as (Record<string, string> | undefined),
  entityify: function (string: string) {
      return string.replace (/&/g, '&amp;').replace (/</g, '&lt;').replace (/>/g, '&gt;').replace (/"/g, '&quot;').replace (/'/g, '&#39;').replace (/`/g, '&#96;');
   },
  redirect: function (where: string) {
    where = '/' + where;
    window.location.pathname = where;
  },
  logout: function () {
    $.ajax ({type: 'POST', url: '/auth/logout'}).done (function () {
      auth.redirect ('login');
    });
  },
  destroy: function (confirmation: string) {
    modal.confirm (confirmation, function () {
      $.ajax ({type: 'POST', url: '/auth/destroy'}).done (function () {
        auth.redirect ('');
      });
    });
  },
  destroy_public: function (confirmation: string) {
    modal.confirm (confirmation, function () {
      $.ajax ({type: 'POST', url: '/auth/destroy_public'}).done (function () {
        auth.redirect ('my-profile');
      });
    });
  },
  submit: function (op: string) {
    const values: UserForm = {};
    $ ('form.js-validated-form *').map (function (_k, el) {
      if (el.id) values[el.id as keyof UserForm] = (el as HTMLInputElement).value;
    });

    if (op === 'signup') {
      const payload: User = {
        username: values.username,
        email: values.email,
        mail_repeat: values.mail_repeat,
        password: values.password,
        password_repeat: values.password_repeat,
        language: values.language,
        keyword_language: values.keyword_language,
        birth_year: values.birth_year ? parseInt(values.birth_year) : undefined,
        country: values.country ? values.country : undefined,
        gender: values.gender ? values.gender : undefined,
        is_teacher: $('#is_teacher').prop('checked'),
        subscribe: $('#subscribe').prop('checked'),
        agree_terms: $('#agree_terms').prop('checked'),
        agree_third_party: $('#agree_third_party').prop('checked'),
        prog_experience: $('input[name=has_experience]:checked').val() as 'yes'|'no',
        experience_languages: $('#languages').is(':visible')
          ? $('input[name=languages]').filter(':checked').map((_, box) => $(box).val() as string).get()
          : undefined,
      };

      $.ajax ({
        type: 'POST',
        url: '/auth/signup',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function () {
        // We set up a non-falsy profile to let `saveit` know that we're logged in. We put session_expires_at since we need it.
        afterLogin({"first_time": true});
      }).fail (function (response) {
        modal.alert(response.responseText, 3000, true);
      });
    }

    if (op === 'login') {
      $.ajax ({
        type: 'POST',
        url: '/auth/login',
        data: JSON.stringify ({username: values.username, password: values.password}),
        contentType: 'application/json; charset=utf-8'
      }).done (function (response) {
        // We set up a non-falsy profile to let `saveit` know that we're logged in. We put session_expires_at since we need it.
        // This happens when a student account (without an mail address logs in for the first time
        if (response['first_time']) {
          return afterLogin({"first_time": true});
        }
        return afterLogin({"admin": response['admin'] || false, "teacher": response['teacher']} || false);
      }).fail (function (response) {
        modal.alert(response.responseText, 3000, true);
      });
    }

    if (op === 'profile') {
      const payload: User = {
        email: values.email ? values.email : undefined,
        language: values.language,
        keyword_language: values.keyword_language,
        birth_year: values.birth_year ? parseInt(values.birth_year) : undefined,
        country: values.country ? values.country : undefined,
        gender: values.gender ? values.gender : undefined
      };

      $.ajax ({
        type: 'POST', url: '/profile',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function (response) {
        if (response.reload) {
          modal.alert(response.message, 2000, false);
          setTimeout (function () {location.reload ()}, 2000);
        } else {
          modal.alert(response.message, 3000, false);
        }
      }).fail (function (response) {
        modal.alert(response.responseText, 3000, true);
      });
    }

    if (op === 'change_password') {
      const payload = {
        old_password: values.old_password,
        password: values.password,
        password_repeat: values.password_repeat
      };

      $.ajax ({
        type: 'POST',
        url: '/auth/change_password',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function (response) {
        modal.alert(response.responseText, 3000, false);
        $ ('#old_password').val ('');
        $ ('#password').val ('');
        $ ('#password_repeat').val ('');
      }).fail (function (response) {
        modal.alert(response.responseText, 3000, true);
      });
    }

    if (op === 'recover') {
      const payload = {
        username: values.username
      };
      $.ajax ({
        type: 'POST', url: '/auth/recover',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function (response) {
        modal.alert(response.message, 3000, false);
        $('#username').val('');
      }).fail (function (response) {
        modal.alert(response.responseText, 3000, true);
      });
    }

    if (op === 'reset') {
      const payload = {
        username: values.username,
        token: values.token,
        password: values.password,
        password_repeat: values.password_repeat
      };

      $.ajax ({
        type: 'POST', url: '/auth/reset',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function (response) {
        modal.alert(response.message, 2000, false);
        $('#password').val('');
        $('#password_repeat').val('');
        setTimeout(function (){
          auth.redirect ('login');
        }, 2000);
      }).fail (function (response) {
        modal.alert(response.responseText, 3000, true);
      });
    }

    if (op === 'public_profile') {
      const data = {
        image: $('#profile_picture').val() ? $('#profile_picture').val():  undefined,
        personal_text: $('#personal_text').val() ? $('#personal_text').val():  undefined,
        favourite_program: $('#favourite_program').val() ? $('#favourite_program').val():  undefined
      }
      $.ajax ({
        type: 'POST',
        url: '/auth/public_profile',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8'
      }).done (function (response) {
        modal.alert(response.message, 3000, false);
        if (response.achievement) {
          showAchievements(response.achievement, false, "");
        }
        $('#public_profile_redirect').show();
      }).fail (function (response) {
        return modal.alert(response.responseText, 3000, true);
      });
    }
  },
  markAsTeacher: function (checkbox: any, username: string, is_teacher: boolean) {
    $(checkbox).prop('checked', false);
    let text = "Are you sure you want to remove " + username + " as a teacher?";
    if (is_teacher) {
      text = "Are you sure you want to make " + username + " a teacher?";
    }
    modal.confirm (text, function () {
      $.ajax({
        type: 'POST',
        url: '/admin/markAsTeacher',
        data: JSON.stringify({username: username, is_teacher: is_teacher}),
        contentType: 'application/json; charset=utf-8'
      }).done(function () {
        $(checkbox).prop('checked', true);
        modal.alert(['User', username, 'successfully', is_teacher ? 'marked' : 'unmarked', 'as teacher'].join(' '), 2000, false);
      }).fail(function () {
        modal.alert(['Error when', is_teacher ? 'marking' : 'unmarking', 'user', username, 'as teacher'].join(' '), 2000, false);
      });
    });
  },
  changeUserEmail: function (username: string, email: string) {
    modal.prompt ('Please enter the corrected email', email, function (correctedEmail) {
      if (correctedEmail === email) return;
      $.ajax ({
        type: 'POST',
        url: '/admin/changeUserEmail',
        data: JSON.stringify ({username: username, email: correctedEmail}),
        contentType: 'application/json; charset=utf-8'
      }).done (function () {
        location.reload ();
      }).fail (function () {
        // Todo TB -> Remove hard-coded string
        modal.alert (['Error when changing the email for user', username].join (' '), 2000, true);
      });
    });
  },
}

// *** LOADERS ***

$("#language").change(function () {
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

$ ('#email, #mail_repeat').on ('cut copy paste', function (e) {
   e.preventDefault ();
   return false;
});

/**
 * After login:
 *
 * - Check if there's a saved program in localstorage. If so, save it.
 * - Check if we were supposed to be joining a class. If so, join it.
 * - Otherwise redirect to "my programs".
 */
async function afterLogin(loginData: Dict<boolean>) {
  const savedProgramString = localStorage.getItem('hedy-first-save');
  const savedProgram = savedProgramString ? JSON.parse(savedProgramString) : undefined;

  if (savedProgram) {
    await saveitP(savedProgram[0], savedProgram[1], savedProgram[2], savedProgram[3], savedProgram[4]);
    localStorage.removeItem('hedy-first-save');
    return auth.redirect('programs');
  }

  const joinClassString = localStorage.getItem('hedy-join');
  const joinClass = joinClassString ? JSON.parse(joinClassString) : undefined;
  if (joinClass) {
    localStorage.removeItem('hedy-join');
    return join_class(joinClass.id, joinClass.name);
  }

  const redirect = getSavedRedirectPath();
  if (redirect) {
    return auth.redirect(redirect);
  }

  // If the user logs in for the first time -> redirect to the landing-page after signup
  if (loginData['first_time']) {
    return auth.redirect('landing-page/1');
  }
  // If the user is an admin -> re-direct to admin page after login
  if (loginData['admin']) {
    return auth.redirect('admin');
  }

  // If the user is a teacher -> re-direct to for-teachers page after login
  if (loginData['teacher']) {
    return auth.redirect('for-teachers');
  }
  // Otherwise, redirect to the programs page
  auth.redirect('landing-page');
}

function getSavedRedirectPath() {
  const redirect = localStorage.getItem('hedy-save-redirect');
  if (redirect) {
    localStorage.removeItem('hedy-save-redirect');
  }
  return redirect;
}
