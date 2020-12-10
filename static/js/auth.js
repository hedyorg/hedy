var countries = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos (Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands (Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See (Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin (French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten (Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

window.auth = {
  logout: function () {
    $.ajax ({type: 'POST', url: '/auth/logout'}).done (function () {
      window.location.pathname = '/login';
    });
  },
  destroy: function () {
    $.ajax ({type: 'POST', url: '/auth/destroy'}).done (function () {
      if (! confirm ('Are you sure? You cannot revert this action.')) return;
      window.location.pathname = '/signup';
    });
  },
  submit: function (op) {
    var values = {};
    $ ('form.auth *').map (function (k, el) {
      if (el.id) values [el.id] = el.value;
    });

    if (op === 'signup') {
      if (! values.username) return alert ('Please enter an username.');
      values.username = values.username.trim ();
      if (values.username.length < 3) return alert ('Username must contain at least three characters.');
      if (values.username.match (/:|@/)) return alert ('Username cannot contain `:` or `@`.');
      if (! values.password) return alert ('Please enter a password.');
      if (values.password.length < 6) return alert ('Password must contain at least six characters.');
      if (values.password !== values.password_repeat) return alert ('The repeated password does not match.');
      if (! values.email.match (/^(([a-zA-Z0-9_\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$/)) return alert ('Please enter a valid email.');
      if (values.birth_year) {
        values.birth_year = parseInt (values.birth_year);
        if (! values.birth_year || values.birth_year < 1900 || values.birth_year > new Date ().getFullYear ()) return alert ('Please enter a year between 1900 and ' + new Date ().getFullYear ());
      }

      var payload = {};
      ['username', 'email', 'password', 'birth_year', 'country', 'gender'].map (function (k) {
        if (! values [k]) return;
        if (k === 'birth_year') payload [k] = parseInt (values [k]);
        payload [k] = values [k];
      });

      $.ajax ({type: 'POST', url: '/auth/signup', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function () {
        alert ('Success! Please login :).');
        window.location.pathname = '/login';
      }).fail (function (response) {
        alert ('There was an error, please try again.');
      });
    }

    if (op === 'login') {
      if (! values.username) return alert ('Please enter an username or email.');
      if (! values.password) return alert ('Please enter a password.');
      $.ajax ({type: 'POST', url: '/auth/login', data: JSON.stringify ({username: values.username, password: values.password}), contentType: 'application/json; charset=utf-8'}).done (function () {
        window.location.pathname = '/my-profile';
      }).fail (function (response) {
        alert ('There was an error, please try again.');
      });
    }
  }
}

// *** LOADERS ***

if ($ ('#country') && $ ('#country').html () && $ ('#country').html ().trim () === '') {
  var html = '<option value="">Select</option>';
  Object.keys (countries).map (function (code) {
    html += '<option value="' + code + '">' + countries [code] + '</option>';
  });
  $ ('#country').html (html);
}

// We use GET /profile to see if we're logged in since we use HTTP only cookies and cannot check from javascript.
$.ajax ({type: 'GET', url: '/profile'}).done (function (response) {
  if (window.location.pathname.indexOf (['/signup', '/login']) !== -1) window.location.pathname = '/my-profile';
  window.auth.profile = response;
  if ($ ('#profile').html ()) $ ('#profile').html (JSON.stringify (window.auth.profile, null, '  '));
}).fail (function (response) {
  if (window.location.pathname.indexOf (['/my-profile']) !== -1) window.location.pathname = '/login';
});
