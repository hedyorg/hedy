var countries = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos (Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands (Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See (Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin (French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten (Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

window.auth = {
  texts: {},
  emailRegex: /^(([a-zA-Z0-9_+\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$/,
  redirect: function (where) {
    where = '/' + where;
    window.location.pathname = where;
  },
  logout: function () {
    $.ajax ({type: 'POST', url: '/auth/logout'}).done (function () {
      auth.redirect ('login');
    });
  },
  destroy: function () {
    if (! confirm (auth.texts.are_you_sure)) return;
    $.ajax ({type: 'POST', url: '/auth/destroy'}).done (function () {
      auth.redirect ('');
    });
  },
  error: function (message, element, id) {
    $ (id || '#error').html (message);
    $ (id || '#error').css ('display', 'block');
    if (element) $ ('#' + element).css ('border', 'solid 1px red');
  },
  clear_error: function (id) {
    $ (id || '#error').html ('');
    $ (id || '#error').css ('display', 'none');
    $ ('form *').css ('border', '');
  },
  success: function (message, id) {
    $ ('#error').css ('display', 'none');
    $ (id || '#success').html (message);
    $ (id || '#success').css ('display', 'block');
  },
  submit: function (op) {
    var values = {};
    $ ('form.auth *').map (function (k, el) {
      if (el.id) values [el.id] = el.value;
    });

    if (op === 'signup') {
      if (! values.username) return auth.error (auth.texts.please_username, 'username');
      values.username = values.username.trim ();
      if (values.username.length < 3) return auth.error (auth.texts.username_three, 'username');
      if (values.username.match (/:|@/)) return auth.error (auth.texts.username_special, 'username');
      if (! values.password) return auth.error (auth.texts.please_password, 'password');
      if (values.password.length < 6) return auth.error (auth.texts.password_six, 'password');
      if (! values.email.match (window.auth.emailRegex)) return auth.error (auth.texts.valid_email, 'email');
      if (values.email    !== values.email_repeat)    return auth.error (auth.texts.repeat_match_email,    'email_repeat');
      if (values.password !== values.password_repeat) return auth.error (auth.texts.repeat_match_password, 'password_repeat');
      if (values.birth_year) {
        values.birth_year = parseInt (values.birth_year);
        if (! values.birth_year || values.birth_year < 1900 || values.birth_year > new Date ().getFullYear ()) return auth.error (auth.texts.valid_year + new Date ().getFullYear (), 'birth_year');
      }

      var payload = {};
      ['username', 'email', 'password', 'birth_year', 'country', 'gender', 'subscribe'].map (function (k) {
        if (! values [k]) return;
        if (k === 'birth_year') payload [k] = parseInt (values [k]);
        else if (k === 'subscribe') payload [k] = $ ('#subscribe').prop ('checked');
        else payload [k] = values [k];
      });

      $.ajax ({type: 'POST', url: '/auth/signup', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        auth.success (auth.texts.signup_success);

        var savedProgram = localStorage.getItem ('hedy-first-save');
        if (! savedProgram) return auth.redirect ('programs');
        savedProgram = JSON.parse (savedProgram);
        // We set up a non-falsy profile to let `saveit` know that we're logged in.
        window.auth.profile = {};
        window.saveit (savedProgram [0], savedProgram [1], savedProgram [2], savedProgram [3], function () {
           localStorage.removeItem ('hedy-first-save');
           var redirect = localStorage.getItem ('hedy-save-redirect');
           if (redirect) localStorage.removeItem ('hedy-save-redirect');
           auth.redirect (redirect || 'programs');
        });

      }).fail (function (response) {
        var error = response.responseText || '';
        if (error.match ('email'))         auth.error (auth.texts.exists_email);
        else if (error.match ('username')) auth.error (auth.texts.exists_username);
        else                               auth.error (auth.texts.ajax_error);
      });
    }

    if (op === 'login') {
      if (! values.username) return auth.error (auth.texts.please_username_email, 'username');
      if (! values.password) return auth.error (auth.texts.please_password, 'password');

      auth.clear_error ();
      $.ajax ({type: 'POST', url: '/auth/login', data: JSON.stringify ({username: values.username, password: values.password}), contentType: 'application/json; charset=utf-8'}).done (function () {

        var savedProgram = localStorage.getItem ('hedy-first-save');
        if (! savedProgram) return auth.redirect ('programs');
        savedProgram = JSON.parse (savedProgram);
        // We set up a non-falsy profile to let `saveit` know that we're logged in. We put session_expires_at since we need it.
        window.auth.profile = {session_expires_at: Date.now () + 1000 * 60 * 60 * 24};
        window.saveit (savedProgram [0], savedProgram [1], savedProgram [2], savedProgram [3], function () {
           localStorage.removeItem ('hedy-first-save');
           var redirect = localStorage.getItem ('hedy-save-redirect');
           if (redirect) localStorage.removeItem ('hedy-save-redirect');
           auth.redirect (redirect || 'programs');
        });

      }).fail (function (response) {
        if (response.status === 403) {
           auth.error (auth.texts.invalid_username_password + ' ' + auth.texts.no_account + ' &nbsp;<button class="green-btn" onclick="auth.redirect (\'signup\')">' + auth.texts.create_account + '</button>');
           $ ('#create-account').hide ();
           localStorage.setItem ('hedy-login-username', values.username);
        }
        else                         auth.error (auth.texts.ajax_error);
      });
    }

    if (op === 'profile') {
      if (! values.email.match (window.auth.emailRegex)) return auth.error (auth.texts.valid_email, 'email');
      if (values.birth_year) {
        values.birth_year = parseInt (values.birth_year);
        if (! values.birth_year || values.birth_year < 1900 || values.birth_year > new Date ().getFullYear ()) return auth.error (auth.texts.valid_year + new Date ().getFullYear (), 'birth_year');
      }

      var payload = {};
      ['email', 'birth_year', 'country', 'gender'].map (function (k) {
        if (! values [k]) return;
        if (k === 'birth_year') payload [k] = parseInt (values [k]);
        payload [k] = values [k];
      });

      auth.clear_error ();
      $.ajax ({type: 'POST', url: '/profile', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        auth.success (auth.texts.profile_updated);
      }).fail (function (response) {
        auth.error (auth.texts.ajax_error);
      });
    }

    if (op === 'change_password') {
      if (! values.password) return auth.error (auth.texts.please_password, 'password', '#error-password');
      if (values.password.length < 6) return auth.error (auth.texts.password_six, 'password', '#error-password');
      if (values.password !== values.password_repeat) return auth.error (auth.texts.repeat_match, 'password_repeat', '#error-password');

      var payload = {old_password: values.old_password, new_password: values.password};

      auth.clear_error ('#error-password');
      $.ajax ({type: 'POST', url: '/auth/change_password', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        auth.success (auth.texts.password_updated, '#success-password');
        $ ('#old_password').val ('');
        $ ('#password').val ('');
        $ ('#password_repeat').val ('');
      }).fail (function (response) {
        if (response.status === 403) auth.error (auth.texts.invalid_password, null, '#error-password');
        else                         auth.error (auth.texts.ajax_error, null, '#error-password');
      });
    }

    if (op === 'recover') {
      if (! values.username) return auth.error (auth.texts.please_username, 'username');

      var payload = {username: values.username};

      auth.clear_error ();
      $.ajax ({type: 'POST', url: '/auth/recover', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        auth.success (auth.texts.sent_password_recovery);
        $ ('#username').val ('');
      }).fail (function (response) {
        if (response.status === 403) auth.error (auth.texts.invalid_username);
        else                         auth.error (auth.texts.ajax_error);
      });
    }

    if (op === 'reset') {
      if (! values.password) return auth.error (auth.texts.please_password, 'password');
      if (values.password.length < 6) return auth.eror (auth.texts.password_six, 'password');
      if (values.password !== values.password_repeat) return auth.error (auth.texts.repeat_match, 'password_repeat');

      var payload = {username: auth.reset.username, token: auth.reset.token, password: values.password};

      auth.clear_error ();
      $.ajax ({type: 'POST', url: '/auth/reset', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        auth.success (auth.texts.password_resetted);
        $ ('#password').val ('');
        $ ('#password_repeat').val ('');
        delete auth.reset;
        auth.redirect ('login');
      }).fail (function (response) {
        if (response.status === 403) auth.error (auth.texts.invalid_reset_link);
        else                         auth.error (auth.texts.ajax_error);
      });
    }
  },
  markAsTeacher: function (username, is_teacher) {
    $.ajax ({type: 'POST', url: '/admin/markAsTeacher', data: JSON.stringify ({username: username, is_teacher: is_teacher}), contentType: 'application/json; charset=utf-8'}).done (function () {
      alert (['User', username, 'successfully', is_teacher ? 'marked' : 'unmarked', 'as teacher'].join (' '));
    }).fail (function (error) {
      console.log (error);
      alert (['Error when', is_teacher ? 'marking' : 'unmarking', 'user', username, 'as teacher'].join (' '));
    });
  },

  changeUserEmail: function (username, email) {
    var correctedEmail = prompt ('Please enter the corrected email', email);
    if (correctedEmail === email) return;
    if (! correctedEmail.match (window.auth.emailRegex)) return alert ('Please enter a valid email.');
    $.ajax ({type: 'POST', url: '/admin/changeUserEmail', data: JSON.stringify ({username: username, email: correctedEmail}), contentType: 'application/json; charset=utf-8'}).done (function () {
      alert (['Successfully changed the email for User', username, 'to', correctedEmail].join (' '));
      location.reload ();
    }).fail (function (error) {
      console.log (error);
      alert (['Error when changing the email for User', username].join (' '));
    });
  },
}

// *** LOADERS ***

if ($ ('#country')) {
  var html = '<option value="">Select</option>';
  Object.keys (countries).map (function (code) {
    html += '<option value="' + code + '">' + countries [code] + '</option>';
  });
  $ ('#country').html (html);
}

$ ('.auth input').get ().map (function (el) {
  // Clear red borders if input was marked from a previous error.
  el.addEventListener ('input', auth.clear_error);
});

$.ajax ({type: 'GET', url: '/auth/texts' + window.location.search}).done (function (response) {
  auth.texts = response;
});

// We use GET /profile to see if we're logged in since we use HTTP only cookies and cannot check from javascript.
$.ajax ({type: 'GET', url: '/profile'}).done (function (response) {
  if (['/signup', '/login'].indexOf (window.location.pathname) !== -1) auth.redirect ('my-profile');

  auth.profile = response;
  if ($ ('#profile').html ()) {
    $ ('#username').html (response.username);
    $ ('#email').val (response.email);
    $ ('#birth_year').val (response.birth_year);
    $ ('#gender').val (response.gender);
    $ ('#country').val (response.country);
  }
}).fail (function (response) {
  if (window.location.pathname.indexOf (['/my-profile']) !== -1) auth.redirect ('login');
});

if (window.location.pathname === '/reset') {
  var query = window.location.search.slice (1).split ('&');
  var params = {};
  query.map (function (item) {
    item = item.split ('=');
    params [item [0]] = decodeURIComponent (item [1]);
  });
  // If we don't receive username and token, the redirect link is invalid. We redirect the user to /recover.
  if (! params.username || ! params.token) auth.redirect ('recover')
  else auth.reset = params;
}

if (window.location.pathname === '/signup') {
  var login_username = localStorage.getItem ('hedy-login-username');
  if (login_username) {
    localStorage.removeItem ('hedy-login-username');
    if (login_username.match ('@')) $ ('#email').val (login_username);
    else                            $ ('#username').val (login_username);
  }
}

$ ('#email, #email_repeat').on ('cut copy paste', function (e) {
   e.preventDefault ();
   return false;
});
