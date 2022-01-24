import { modal } from './modal';
import { join_class } from './teachers';
import { saveitP } from './app';

const countries: Record<string, string> = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos (Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands (Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See (Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin (French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten (Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

export interface Profile {
  session_expires_at: number;
}

interface User {
  username?: string;
  email?: string;
  mail_repeat?: string;
  password?: string;
  password_repeat?: string;
  birth_year?: number;
  language?: string,
  country?: string;
  gender?: string;
  subscribe?: string;
  prog_experience?: 'yes' | 'no';
  experience_languages?: string[];
  is_teacher?: string;
}

interface UserForm {
  username?: string;
  email?: string;
  password?: string;
  birth_year?: string;
  language?: string,
  country?: string;
  gender?: string;
  subscribe?: string;
  mail_repeat?: string;
  password_repeat?: string;
  old_password?: string;
}

if (!(window as any).AuthMessages) {
  throw new Error('On a page where you load this JavaScript, you must also load the "client_messages.js" script');
}

export const auth = {
  texts: AuthMessages,
  profile: undefined as (Profile | undefined),
  reset: undefined as (Record<string, string> | undefined),
  entityify: function (string: string) {
      return string.replace (/&/g, '&amp;').replace (/</g, '&lt;').replace (/>/g, '&gt;').replace (/"/g, '&quot;').replace (/'/g, '&#39;').replace (/`/g, '&#96;');
   },
  emailRegex: /^(([a-zA-Z0-9_+\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$/,
  redirect: function (where: string) {
    where = '/' + where;
    window.location.pathname = where;
  },
  logout: function () {
    $.ajax ({type: 'POST', url: '/auth/logout'}).done (function () {
      auth.redirect ('login');
    });
  },
  destroy: function () {
    modal.confirm (auth.texts['are_you_sure'], function () {
      $.ajax ({type: 'POST', url: '/auth/destroy'}).done (function () {
        auth.redirect ('');
      });
    });
  },
  destroy_public: function () {
    modal.confirm (auth.texts['are_you_sure'], function () {
      $.ajax ({type: 'POST', url: '/auth/destroy_public'}).done (function () {
        auth.redirect ('programs');
      });
    });
  },
  error: function (message: string, element?: string | null, id?: string) {
    $ (id || '#error').html (message);
    $ (id || '#error').css ('display', 'block');
    if (element) $ ('#' + element).css ('border', 'solid 1px red');
  },
  clear_error: function (id?: string) {
    $ (id || '#error').html ('');
    $ (id || '#error').css ('display', 'none');
    $ ('form *').css ('border', '');
  },
  success: function (message: string, id?: string) {
    $ ('#error').css ('display', 'none');
    $ (id || '#success').html (message);
    $ (id || '#success').css ('display', 'block');
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
        birth_year: values.birth_year ? parseInt(values.birth_year) : undefined,
        country: values.country ? values.country : undefined,
        gender: values.gender ? values.gender : undefined,
        subscribe: $('#subscribe').prop('checked'),
        is_teacher: $('#is_teacher').prop('checked'),
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
        auth.profile = {session_expires_at: Date.now () + 1000 * 60 * 60 * 24};
        afterLogin();
      }).fail (function (response) {
        auth.clear_error();
        if (response.responseText) {
          auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
      });
    }

    if (op === 'login') {
      $.ajax ({
        type: 'POST',
        url: '/auth/login',
        data: JSON.stringify ({username: values.username, password: values.password}),
        contentType: 'application/json; charset=utf-8'
      }).done (function () {
        // We set up a non-falsy profile to let `saveit` know that we're logged in. We put session_expires_at since we need it.
        auth.profile = {session_expires_at: Date.now () + 1000 * 60 * 60 * 24};
        afterLogin();
      }).fail (function (response) {
        auth.clear_error();
        if (response.responseText) {
           auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
      });
    }

    if (op === 'profile') {
      const payload: User = {
        email: values.email,
        language: values.language,
        birth_year: values.birth_year ? parseInt(values.birth_year) : undefined,
        country: values.country ? values.country : undefined,
        gender: values.gender ? values.gender : undefined,
        prog_experience: $('input[name=has_experience]:checked').val() as 'yes'|'no',
        experience_languages: $('#languages').is(':visible')
          ? $('input[name=languages]').filter(':checked').map((_, box) => $(box).val() as string).get()
          : undefined,
      };

      $.ajax ({
        type: 'POST', url: '/profile',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function () {
        auth.success (auth.texts['profile_updated']);
        setTimeout (function () {location.reload ()}, 1500);
      }).fail (function (response) {
        if (response.responseText) {
           auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
      });
    }

    if (op === 'change_password') {
      const payload = {old_password: values.old_password, password: values.password, password_repeat: values.password_repeat};

      auth.clear_error ('#error-password');
      $.ajax ({
        type: 'POST',
        url: '/auth/change_password',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function () {
        auth.success (auth.texts['password_updated'], '#success_password');
        $ ('#old_password').val ('');
        $ ('#password').val ('');
        $ ('#password_repeat').val ('');
      }).fail (function (response) {
        if (response.responseText) {
           auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
      });
    }

    if (op === 'recover') {
      const payload = {username: values.username};

      auth.clear_error ();
      $.ajax ({
        type: 'POST', url: '/auth/recover',
        data: JSON.stringify (payload),
        contentType: 'application/json; charset=utf-8'
      }).done (function () {
        auth.success (auth.texts['sent_password_recovery']);
        $ ('#username').val ('');
      }).fail (function (response) {
        if (response.responseText) {
          return auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
      });
    }

    if (op === 'reset') {
      const payload = {username: auth.reset?.['username'], token: auth.reset?.['token'], password: values.password};

      auth.clear_error ();
      $.ajax ({type: 'POST', url: '/auth/reset', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        auth.success (auth.texts['password_resetted']);
        $ ('#password').val ('');
        $ ('#password_repeat').val ('');
        delete auth.reset;
        auth.redirect ('login');
      }).fail (function (response) {
        if (response.responseText) {
          return auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
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
      }).done (function () {
        auth.success (auth.texts['public_profile_updated']);
        $('#public_profile_redirect').show();
      }).fail (function (response) {
        if (response.responseText) {
          return auth.error(response.responseText);
        } else {
          auth.error(auth.texts['ajax_error']);
        }
      });
    }
  },
  markAsTeacher: function (username: string, is_teacher: boolean) {
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
        modal.alert(['User', username, 'successfully', is_teacher ? 'marked' : 'unmarked', 'as teacher'].join(' '), 2000);
      }).fail(function (error) {
        console.log(error);
        modal.alert(['Error when', is_teacher ? 'marking' : 'unmarking', 'user', username, 'as teacher'].join(' '));
      });
    });
  },

  changeUserEmail: function (username: string, email: string) {
    modal.prompt ('Please enter the corrected email', email, function (correctedEmail) {
      if (correctedEmail === email) return;
      if (! correctedEmail.match (auth.emailRegex)) return modal.alert ('Please enter a valid email.');
      $.ajax ({type: 'POST', url: '/admin/changeUserEmail', data: JSON.stringify ({username: username, email: correctedEmail}), contentType: 'application/json; charset=utf-8'}).done (function () {
        modal.alert (['Successfully changed the email for User', username, 'to', correctedEmail].join (' '));
        location.reload ();
      }).fail (function (error) {
        console.log (error);
        modal.alert (['Error when changing the email for User', username].join (' '));
      });
    });
  },
}

// *** LOADERS ***

if ($ ('#country')) {
  let html = $('#country').html();
  Object.keys (countries).map (function (code) {
    html += '<option value="' + code + '">' + countries [code] + '</option>';
  });
  $ ('#country').html (html);
}

$ ('.auth input').get ().map (function (el) {
  // Clear red borders if input was marked from a previous error.
  el.addEventListener ('input', () => auth.clear_error());
});

// We use GET /profile to see if we're logged in since we use HTTP only cookies and cannot check from javascript.
$.ajax ({type: 'GET', url: '/profile'}).done (function (response) {
   if (['/signup', '/login'].indexOf (window.location.pathname) !== -1) auth.redirect ('my-profile');
   auth.profile = response;
});

if (window.location.pathname === '/reset') {
  const query = window.location.search.slice (1).split ('&');
  const params: Record<string, string> = {};
  query.map (function (item) {
    const split = item.split ('=');
    params [split [0]] = decodeURIComponent (split [1]);
  });
  // If we don't receive username and token, the redirect link is invalid. We redirect the user to /recover.
  if (! params['username'] || ! params['token']) auth.redirect ('recover')
  else auth.reset = params;
}

if (window.location.pathname === '/signup') {
  const login_username = localStorage.getItem ('hedy-login-username');
  if (login_username) {
    localStorage.removeItem ('hedy-login-username');
    if (login_username.match ('@')) $ ('#email').val (login_username);
    else                            $ ('#username').val (login_username);
  }
  const redirect = localStorage.getItem('hedy-save-redirect');
  if (redirect && redirect.includes('invite')) {
    $ ('#is_teacher_div').hide();
  }
}

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
async function afterLogin() {
  const savedProgramString = localStorage.getItem('hedy-first-save');
  const savedProgram = savedProgramString ? JSON.parse(savedProgramString) : undefined;

  if (savedProgram) {
    await saveitP(savedProgram[0], savedProgram[1], savedProgram[2], savedProgram[3]);
    localStorage.removeItem('hedy-first-save');

    const redirect = getSavedRedirectPath();
    if (redirect) {
      return auth.redirect(redirect);
    }
  }

  const joinClassString = localStorage.getItem('hedy-join');
  const joinClass = joinClassString ? JSON.parse(joinClassString) : undefined;
  if (joinClass) {
    localStorage.removeItem('hedy-join');
    return join_class(joinClass.link, joinClass.name);
  }

  const redirect = getSavedRedirectPath();
  if (redirect) {
    return auth.redirect(redirect);
  }

  auth.redirect('programs');
}

function getSavedRedirectPath() {
  const redirect = localStorage.getItem('hedy-save-redirect');
  if (redirect) {
    localStorage.removeItem('hedy-save-redirect');
  }
  return redirect;
}
