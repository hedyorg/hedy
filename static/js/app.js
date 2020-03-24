(function() {
  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");
  // editor.session.setMode("ace/mode/javascript");

  // Load existing code from session, if it exists
  const storage = window.sessionStorage;
  if (storage) {
    const level = queryParam('level') || '1';
    const levelKey = 'level_' + level + '_code';

    // On page load, if we have a saved program, load it
    if (storage.getItem(levelKey)) {
      editor.setValue(storage.getItem(levelKey), 1);
    }

    // When the user exits the editor, save what we have.
    editor.on('blur', function(e) {
      storage.setItem(levelKey, editor.getValue());
    });
  }
})();

function goto(level, lang) {
    window.location.href = buildUrl('/', {
      level: level,
      lang: lang
    });
}

function runit(level, lang) {
  error.hide();
  try {
    level = level.toString();
    var editor = ace.edit("editor");
    var code = editor.getValue();

    console.log('Original program:\n', code);

    $.getJSON('/parse/', {
      level: level,
      code: code,
      lang: lang
    }).done(function(response) {
      console.log('Response', response);
      if (response.Error) {
        error.show(ErrorMessages.Transpile_error, response.Error);
        return;
      }

      runPythonProgram(response.Code).catch(function(err) {
        error.show(ErrorMessages.Execute_error, err.message);
        reportClientError(level, code, err.message);
      });
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
    });

  } catch (e) {
    console.error(e);
    error.show(ErrorMessages.Other_error, e.message);
  }
}

/**
 * Do a POST with the error to the server so we can log it
 */
function reportClientError(level, code, client_error) {
  $.ajax({
    type: 'POST',
    url: '/report_error',
    data: JSON.stringify({
      level: level,
      code: code,
      client_error: client_error,
    }),
    contentType: 'application/json',
    dataType: 'json'
  });
}

function runPythonProgram(code) {
  const outputDiv = $('#output');
  outputDiv.empty();

  Sk.pre = "output";
  Sk.configure({
    output: outf,
    read: builtinRead,
    inputfun: inputFromInlineModal,
    inputfunTakesPrompt: true,
    __future__: Sk.python3
  });

  return Sk.misceval.asyncToPromise(function () {
    return Sk.importMainWithBody("<stdin>", false, code, true);
  }).then(function(mod) {
    console.log('Program executed');
  }).catch(function(err) {
    // Extract error message from error
    console.log(err);
    const errorMessage = errorMessageFromSkulptError(err) || JSON.stringify(err);
    throw new Error(errorMessage);
  });

  /**
   * Get the error messages from a Skulpt error
   *
   * They look like this:
   *
   * {"args":{"v":[{"v":"name 'name' is not defined"}]},"traceback":[{"lineno":3,"colno":0,"filename":"<stdin>.py"}]}
   *
   * Don't know why, so let's be defensive about it.
   */
  function errorMessageFromSkulptError(err) {
    const message = err.args && err.args.v && err.args.v[0] && err.args.v[0].v;
    return message;
  }

  function addToOutput(text, color) {
    $('<span>').text(text).css({ color }).appendTo(outputDiv);
  }

  // output functions are configurable.  This one just appends some text
  // to a pre element.
  function outf(text) {
    addToOutput(text, 'white');
  }

  function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
  }

  /**
   * Get the input inline in the terminal
   *
   * Render the prompt to the terminal, add an inputbox where the user can
   * type, and replace the inputbox with static text after they hit enter.
   */
  function inputFromTerminal(prompt) {
    return new Promise(function(ok) {
      addToOutput(prompt + '\n', 'white');
      const input = $('<input>').attr('placeholder', 'Typ hier je antwoord').appendTo(outputDiv).focus();

      // When enter is pressed, turn the input box into a regular
      // span and resolve the promise
      input.on('keypress', function(e) {
        if (e.which == 13 /* ENTER */) {
          const text = input.val();

          input.remove();
          addToOutput(text + '\n', 'yellow');
          ok(text);
        }
      });
    });
  }

  function inputFromInlineModal(prompt) {
    return new Promise(function(ok) {
      const input = $('#inline-modal input[type="text"]');
      $('#inline-modal .caption').text(prompt);
      input.val('');
      setTimeout(function() {
        input.focus();
      }, 0);
      $('#inline-modal form').one('submit', function(event) {
        event.preventDefault();
        $('#inline-modal').hide();
        ok(input.val());
        return false;
      });
      $('#inline-modal').show();
    });
  }
}

var error = {
  hide() {
    $('#errorbox').hide();
  },

  show(caption, message) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').text(message);
    $('#errorbox').show();
  }
};

function queryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

function buildUrl(url, params) {
  const clauses = [];
  for (let key in params) {
    const value = params[key];
    if (value !== undefined && value !== '') {
      clauses.push(encodeURIComponent(key) + '=' + encodeURIComponent(value));
    }
  }
  return url + (clauses.length > 0 ? '?' + clauses.join('&') : '');
}
