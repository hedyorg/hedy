(function() {
  // A bunch of code expects a global "State" object. Set it here if not 
  // set yet.
  if (!window.State) {
    window.State = {};
  }

  // If there's no #editor div, we're requiring this code in a non-code page.
  // Therefore, we don't need to initialize anything.
  const $editor = $('#editor');
  if (!$editor.length) return;

  // *** EDITOR SETUP ***
  // We expose the editor globally so it's available to other functions for resizing
  var editor = window.editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");

  // Editor could have been initialized as readonly
  if ($editor.data('readonly')) {
    editor.setReadOnly(true);
  }

  // a variable which turns on(1) highlighter or turns it off(0)
  var highlighter = 0;

  if (highlighter == 1){
        if (window.State.level == 1){
          window.editor.session.setMode("ace/mode/level1");
        }
        if (window.State.level == 2){
          window.editor.session.setMode("ace/mode/level2");
        }
        if (window.State.level == 3){
          window.editor.session.setMode("ace/mode/level3");
        }
        if (window.State.level == 4){
          window.editor.session.setMode("ace/mode/level4");
        }
        if (window.State.level == 5){
          window.editor.session.setMode("ace/mode/level5");
        }
        if (window.State.level == 6){
          window.editor.session.setMode("ace/mode/level6");
        }
        if (window.State.level == 7){
          window.editor.session.setMode("ace/mode/level7");
        }
        if (window.State.level == 8 || window.State.level == 9){
          window.editor.session.setMode("ace/mode/level8and9");
        }
        if (window.State.level == 10){
          window.editor.session.setMode("ace/mode/level10");
        }
        if (window.State.level == 11){
          window.editor.session.setMode("ace/mode/level11");
        }
        if (window.State.level == 12){
          window.editor.session.setMode("ace/mode/level12");
        }
        if (window.State.level == 13){
          window.editor.session.setMode("ace/mode/level13");
        }
        if (window.State.level == 14){
          window.editor.session.setMode("ace/mode/level14");
        }
        if (window.State.level == 15){
          window.editor.session.setMode("ace/mode/level15");
        }
        if (window.State.level == 16){
          window.editor.session.setMode("ace/mode/level16");
        }
        if (window.State.level == 17 || window.State.level == 18){
          window.editor.session.setMode("ace/mode/level17and18");
        }
        if (window.State.level == 19){
          window.editor.session.setMode("ace/mode/level19");
        }
        if (window.State.level == 20){
          window.editor.session.setMode("ace/mode/level20");
        }
        if (window.State.level == 21 || window.State.level == 22){
          window.editor.session.setMode("ace/mode/level21and22");
        }
  }


  // Load existing code from session, if it exists
  const storage = window.sessionStorage;
  if (storage) {
    const levelKey = $editor.data('lskey');
    const loadedProgram = $editor.data('loaded-program');

    // On page load, if we have a saved program and we are not loading a program by id, we load the saved program
    if (loadedProgram !== 'True' && storage.getItem(levelKey)) {
      editor.setValue(storage.getItem(levelKey), 1);
    }

    // When the user exits the editor, save what we have.
    editor.on('blur', function(e) {
      storage.setItem(levelKey, editor.getValue());
    });

    // If prompt is shown and user enters text in the editor, hide the prompt.
    editor.on('change', function () {
      if ($('#inline-modal').is (':visible')) $('#inline-modal').hide();
      window.State.disable_run = false;
      $ ('#runit').css('background-color', '');
      window.State.unsaved_changes = true;
    });
  }

  // *** PROMPT TO SAVE CHANGES ***

  window.onbeforeunload = function () {
     // The browser doesn't show this message, rather it shows a default message.
     // We still have an internationalized message in case we want to implement this as a modal in the future.
     if (window.State.unsaved_changes) return window.auth.texts.unsaved_changes;
  };

  // *** KEYBOARD SHORTCUTS ***

  let altPressed;

  // alt is 18, enter is 13
  window.addEventListener ('keydown', function (ev) {
    const keyCode = (ev || document.event).keyCode;
    if (keyCode === 18) return altPressed = true;
    if (keyCode === 13 && altPressed) {
      runit (window.State.level, window.State.lang, function () {
        $ ('#output').focus ();
      });
    }
    // We don't use jquery because it doesn't return true for this equality check.
    if (keyCode === 37 && document.activeElement === document.getElementById ('output')) {
      editor.focus ();
      editor.navigateFileEnd ();
    }
  });
  window.addEventListener ('keyup', function (ev) {
    const keyCode = (ev || document.event).keyCode;
    if (keyCode === 18) return altPressed = false;
  });

})();

function reloadOnExpiredSession () {
   // If user is not logged in or session is not expired, return false.
   if (! window.auth.profile || window.auth.profile.session_expires_at > Date.now ()) return false;
   // Otherwise, reload the page to update the top bar.
   location.reload ();
   return true;
}

function runit(level, lang, cb) {
  if (window.State.disable_run) return alert (window.auth.texts.answer_question);

  if (reloadOnExpiredSession ()) return;

  error.hide();
  try {
    level = level.toString();
    var editor = ace.edit("editor");
    var code = editor.getValue();

    console.log('Original program:\n', code);
    $.ajax({
      type: 'POST',
      url: '/parse',
      data: JSON.stringify({
        level: level,
        sublevel: window.State.sublevel ? window.State.sublevel : undefined,
        code: code,
        lang: lang,
        adventure_name: window.State.adventure_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      console.log('Response', response);
      if (response.Warning) {
        error.showWarning(ErrorMessages.Transpile_warning, response.Warning);
      }
      if (response.Error) {
        error.show(ErrorMessages.Transpile_error, response.Error);
        return;
      }
      runPythonProgram(response.Code, cb).catch(function(err) {
        console.log(err)
        error.show(ErrorMessages.Execute_error, err.message);
        reportClientError(level, code, err.message);
      });
    }).fail(function(xhr) {
      console.error(xhr);
      // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState
      if (xhr.readyState < 4) {
        error.show(ErrorMessages.Connection_error, ErrorMessages.CheckInternet);
      } else {
        error.show(ErrorMessages.Other_error, ErrorMessages.ServerError);
      }
    });

  } catch (e) {
    console.error(e);
    error.show(ErrorMessages.Other_error, e.message);
  }
}

/**
 * Called when the user clicks the "Try" button in one of the palette buttons
 */
function tryPaletteCode(exampleCode) {
  var editor = ace.edit("editor");

  var MOVE_CURSOR_TO_END = 1;
  editor.setValue(exampleCode + '\n', MOVE_CURSOR_TO_END);
  window.State.unsaved_changes = false;
}


window.saveit = function saveit(level, lang, name, code, cb) {
  if (window.State.sublevel) return alert ('Sorry, you cannot save programs when in a sublevel.');
  error.hide();

  if (reloadOnExpiredSession ()) return;

  try {
    // If there's no session but we want to save the program, we store the program data in localStorage and redirect to /login.
    if (! window.auth.profile) {
       if (! confirm (window.auth.texts.save_prompt)) return;
       // If there's an adventure_name, we store it together with the level, because it won't be available otherwise after signup/login.
       if (window.State && window.State.adventure_name) level = [level, window.State.adventure_name];
       localStorage.setItem ('hedy-first-save', JSON.stringify ([level, lang, name, code]));
       window.location.pathname = '/login';
       return;
    }

    window.State.unsaved_changes = false;

    var adventure_name = window.State.adventure_name;
    // If saving a program for an adventure after a signup/login, level is an array of the form [level, adventure_name]. In that case, we unpack it.
    if (level instanceof Array) {
       adventure_name = level [1];
       level = level [0];
    }

    $.ajax({
      type: 'POST',
      url: '/programs',
      data: JSON.stringify({
        level: level,
        lang:  lang,
        name:  name,
        code:  code,
        adventure_name: adventure_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      // The auth functions use this callback function.
      if (cb) return response.Error ? cb (response) : cb (null, response);
      if (response.Warning) {
        error.showWarning(ErrorMessages.Transpile_warning, response.Warning);
      }
      if (response.Error) {
        error.show(ErrorMessages.Transpile_error, response.Error);
        return;
      }
      $ ('#okbox').show ();
      $ ('#okbox .caption').html (window.auth.texts.save_success);
      $ ('#okbox .details').html (window.auth.texts.save_success_detail);
      setTimeout (function () {
         $ ('#okbox').hide ();
      }, 2000);
      // If we succeed, we need to update the default program name & program for the currently selected tab.
      // To avoid this, we'd have to perform a page refresh to retrieve the info from the server again, which would be more cumbersome.
      // The name of the program might have been changed by the server, so we use the name stated by the server.
      $ ('#program_name').val (response.name);
      window.State.adventures.map (function (adventure) {
        if (adventure.short_name === (adventure_name || 'level')) {
          adventure.loaded_program = {name: response.name, code: code};
        }
      });
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
      if (err.status === 403) {
         localStorage.setItem ('hedy-first-save', JSON.stringify ([adventure_name ? [level, adventure_name] : level, lang, name, code]));
         localStorage.setItem ('hedy-save-redirect', 'hedy');
         window.location.pathname = '/login';
      }
    });
  } catch (e) {
    console.error(e);
    error.show(ErrorMessages.Other_error, e.message);
  }
}

function viewProgramLink(programId) {
  return window.location.origin + '/hedy/' + programId + '/view';
}

window.share_program = function share_program (level, lang, id, Public, reload) {
  if (! window.auth.profile) return alert (window.auth.texts.must_be_logged);

  var share = function (id) {
    $.ajax({
      type: 'POST',
      url: '/programs/share',
      data: JSON.stringify({
        id: id,
        public: Public
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      if ($ ('#okbox') && $ ('#okbox').length) {
        $ ('#okbox').show ();
        $ ('#okbox .caption').html (window.auth.texts.save_success);
        $ ('#okbox .details').html (Public ? window.auth.texts.share_success_detail : window.auth.texts.unshare_success_detail);
        // If we're sharing the program, copy the link to the clipboard.
        if (Public) window.copy_to_clipboard (viewProgramLink(id), true);
      }
      else {
        // If we're sharing the program, copy the link to the clipboard.
        if (Public) window.copy_to_clipboard (viewProgramLink(id), true);
        alert (Public ? window.auth.texts.share_success_detail : window.auth.texts.unshare_success_detail);
      }
      if (reload) setTimeout (function () {location.reload ()}, 1000);
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
    });
  }

  // If id is not true, the request comes from the programs page. In that case, we merely call the share function.
  if (id !== true) return share (id);

  // Otherwise, we save the program and then share it.
  // Saving the program makes things way simpler for many reasons: it covers the cases where:
  // 1) there's no saved program; 2) there's no saved program for that user; 3) the program has unsaved changes.
  var name = $ ('#program_name').val ();
  var code = ace.edit('editor').getValue();
  return saveit(level, lang, name, code, function (err, resp) {
    if (err && err.Warning) return error.showWarning(ErrorMessages.Transpile_warning, err.Warning);
    if (err && err.Error) return error.show(ErrorMessages.Transpile_error, err.Error);
    share (resp.id);
  });

}

window.copy_to_clipboard = function copy_to_clipboard (string, noAlert) {
  // https://hackernoon.com/copying-text-to-clipboard-with-javascript-df4d4988697f
  var el = document.createElement ('textarea');
  el.value = string;
  el.setAttribute ('readonly', '');
  el.style.position = 'absolute';
  el.style.left = '-9999px';
  document.body.appendChild (el);
  var selected = document.getSelection ().rangeCount > 0 ? document.getSelection ().getRangeAt (0) : false;
  el.select ();
  document.execCommand ('copy');
  document.body.removeChild (el);
  if (selected) {
     document.getSelection ().removeAllRanges ();
     document.getSelection ().addRange (selected);
  }
  if (! noAlert) alert (window.auth.texts.copy_clipboard);
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

window.onerror = function reportClientException(message, source, line_number, column_number, error) {

  $.ajax({
    type: 'POST',
    url: '/client_exception',
    data: JSON.stringify({
      message: message,
      source: source,
      line_number: line_number,
      column_number: column_number,
      error: error
    }),
    contentType: 'application/json',
    dataType: 'json'
  });
}

function runPythonProgram(code, cb) {
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
    if (cb) cb ();
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
   // Note: this method is currently not being used.
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

  // This method draws the prompt for asking for user input.
  function inputFromInlineModal(prompt) {
    return new Promise(function(ok) {

      window.State.disable_run = true;
      $ ('#runit').css('background-color', 'gray');

      const input = $('#inline-modal input[type="text"]');
      $('#inline-modal .caption').text(prompt);
      input.val('');
      input [0].placeholder = prompt;
      setTimeout(function() {
        input.focus();
      }, 0);
      $('#inline-modal form').one('submit', function(event) {

        window.State.disable_run = false;
        $ ('#runit').css('background-color', '');

        event.preventDefault();
        $('#inline-modal').hide();
        ok(input.val());
        $ ('#output').focus ();

        return false;
      });
      $('#inline-modal').show();
    });
  }
}

var error = {
  hide() {
    $('#errorbox').hide();
    $('#warningbox').hide();
    if ($('#editor').length) editor.resize ();
  },

  showWarning(caption, message) {
    $('#warningbox .caption').text(caption);
    $('#warningbox .details').text(message);
    $('#warningbox').show();
    if ($('#editor').length) editor.resize ();
  },

  show(caption, message) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').text(message);
    $('#errorbox').show();
    if ($('#editor').length) editor.resize ();
  }
}

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