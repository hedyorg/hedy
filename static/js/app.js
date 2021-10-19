(function() {
  // A bunch of code expects a global "State" object. Set it here if not
  // set yet.
  if (!window.State) {
    window.State = {};
  }

  // *** EDITOR SETUP ***
  initializeMainEditor($('#editor'));

  // Any code blocks we find inside 'turn-pre-into-ace' get turned into
  // read-only editors (for syntax highlighting)
  for (const preview of $('.turn-pre-into-ace pre').get()) {
    $(preview).addClass('text-lg rounded');
    const exampleEditor = turnIntoAceEditor(preview, true)
    // Fits to content size
    exampleEditor.setOptions({ maxLines: Infinity });
    exampleEditor.setOptions({ minLines: 2 });
    // Strip trailing newline, it renders better
    exampleEditor.setValue(exampleEditor.getValue().replace(/\n+$/, ''), -1);
    // And add an overlay button to the editor
    const buttonContainer = $('<div>').css({ position: 'absolute', top: 5, right: 5, width: 'auto'}).appendTo(preview);
    $('<button>').attr('title', UiMessages.try_button).css({ fontFamily: 'sans-serif'}).addClass('green-btn').text('⇥').appendTo(buttonContainer).click(function() {
      window.editor.setValue(exampleEditor.getValue() + '\n');
    });
  }

  /**
   * Initialize the main editor and attach all the required event handlers
   */
  function initializeMainEditor($editor) {
    if (!$editor.length) return;

    // We expose the editor globally so it's available to other functions for resizing
    var editor = window.editor = turnIntoAceEditor($editor.get(0), $editor.data('readonly'));

    window.Range = ace.require('ace/range').Range // get reference to ace/range

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

        clearErrors(editor);
      });
    }

    // *** PROMPT TO SAVE CHANGES ***

    window.onbeforeunload = function () {
       // The browser doesn't show this message, rather it shows a default message.
       if (window.State.unsaved_changes) {
          // This allows us to avoid showing the programmatic modal from `prompt_unsaved` and then the native one
          if (! window.State.no_unload_prompt) return window.auth.texts.unsaved_changes;
       }
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
  }

  /**
   * Turn an HTML element into an Ace editor
   */
  function turnIntoAceEditor(element, isReadOnly) {
    const editor = ace.edit(element);
    editor.setTheme("ace/theme/monokai");
    if (isReadOnly) {
      editor.setOptions({
        readOnly: true,
        showGutter: false,
        showPrintMargin: false,
        highlightActiveLine: false
      });
    }

    // a variable which turns on(1) highlighter or turns it off(0)
    var highlighter = 1;

    if (highlighter == 1) {
      // Everything turns into 'ace/mode/levelX', except what's in
      // this table.
      const modeExceptions = {
        9: 'ace/mode/level9and10',
        10: 'ace/mode/level9and10',
        18: 'ace/mode/level18and19',
        19: 'ace/mode/level18and19',
      };

      const mode = modeExceptions[window.State.level] || `ace/mode/level${window.State.level}`;
      editor.session.setMode(mode);
    }

    return editor;
  }
})();

function reloadOnExpiredSession () {
   // If user is not logged in or session is not expired, return false.
   if (! window.auth.profile || window.auth.profile.session_expires_at > Date.now ()) return false;
   // Otherwise, reload the page to update the top bar.
   location.reload ();
   return true;
}

function clearErrors(editor) {
  editor.session.clearAnnotations();
  for (var marker in editor.session.getMarkers()) {
    editor.session.removeMarker(marker);
  }
}

function runit(level, lang, cb) {
  if (window.State.disable_run) return window.modal.alert (window.auth.texts.answer_question);

  if (reloadOnExpiredSession ()) return;

  error.hide();
  try {
    level = level.toString();
    var editor = ace.edit("editor");
    var code = editor.getValue();

    clearErrors(editor);

    console.log('Original program:\n', code);
    $.ajax({
      type: 'POST',
      url: '/parse',
      data: JSON.stringify({
        level: level,
        code: code,
        lang: lang,
        read_aloud : !!$('#speak_dropdown').val(),
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
        if (response.Location && response.Location[0] != "?") {
          editor.session.setAnnotations([
            {
              row: response.Location[0] - 1,
              column: response.Location[1] - 1,
              text: "",
              type: "error",
            }
          ]);
          // FIXME change this to apply only to the error span once errors have an end location.
          editor.session.addMarker(
            new Range(
                response.Location[0] - 1,
                response.Location[1] - 1,
                response.Location[0] - 1,
                response.Location[1],
            ),
            "editor-error", "fullLine"
          );
        }
        return;
      }
      runPythonProgram(response.Code, response.has_turtle, cb).catch(function(err) {
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
  error.hide();

  if (reloadOnExpiredSession ()) return;

  try {
    // If there's no session but we want to save the program, we store the program data in localStorage and redirect to /login.
    if (! window.auth.profile) {
       return window.modal.confirm (window.auth.texts.save_prompt, function () {
         // If there's an adventure_name, we store it together with the level, because it won't be available otherwise after signup/login.
         if (window.State && window.State.adventure_name) level = [level, window.State.adventure_name];
         localStorage.setItem ('hedy-first-save', JSON.stringify ([level, lang, name, code]));
         window.location.pathname = '/login';
       });
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
      window.modal.alert (window.auth.texts.save_success_detail, 4000);
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
  if (! window.auth.profile) return window.modal.alert (window.auth.texts.must_be_logged);

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
      // If we're sharing the program, copy the link to the clipboard.
      if (Public) window.copy_to_clipboard (viewProgramLink(id), true);
      window.modal.alert (Public ? window.auth.texts.share_success_detail : window.auth.texts.unshare_success_detail, 4000);
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
  if (! noAlert) window.modal.alert (window.auth.texts.copy_clipboard, 4000);
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
      page: window.location.href,
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
      error: error,
      url: window.location.href,
      user_agent: navigator.userAgent,
    }),
    contentType: 'application/json',
    dataType: 'json'
  });
}

function runPythonProgram(code, hasTurtle, cb) {
  const outputDiv = $('#output');
  outputDiv.empty();

  Sk.pre = "output";
  const turtleConfig = (Sk.TurtleGraphics || (Sk.TurtleGraphics = {}));
  turtleConfig.target = 'turtlecanvas';
  turtleConfig.width = 400;
  turtleConfig.height = 300;
  turtleConfig.worldWidth = 400;
  turtleConfig.worldHeight = 300;

  if (!hasTurtle) {
    // There might still be a visible turtle panel. If the new program does not use the Turtle,
    // remove it (by clearing the '#turtlecanvas' div)
    $('#turtlecanvas').empty();
  }

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
    // Check if the program was correct but the output window is empty: Return a warning
    if ($('#output').is(':empty') && $('#turtlecanvas').is(':empty')) {
      error.showWarning(ErrorMessages.Transpile_warning, ErrorMessages.Empty_output);
    }
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
    speak(text)
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
    $('#turtlecanvas').empty();
    return new Promise(function(ok) {

      window.State.disable_run = true;
      $ ('#runit').css('background-color', 'gray');

      const input = $('#inline-modal input[type="text"]');
      $('#inline-modal .caption').text(prompt);
      input.val('');
      input [0].placeholder = prompt;
      speak(prompt)

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

(function () {
  window.speak = function speak(text) {
    var selectedURI = $('#speak_dropdown').val();
    if (!selectedURI) { return; }
    var voice = window.speechSynthesis.getVoices().filter(v => v.voiceURI === selectedURI)[0];

    if (voice) {
      let utterance = new SpeechSynthesisUtterance(text);
      utterance.voice = voice;
      utterance.rate = 0.9;
      speechSynthesis.speak(utterance);
    }
  }

  if (!window.speechSynthesis) { return; /* No point in even trying */ }
  if (!window.State.lang) { return; /* Not on a code page */ }

  /**
   * Show the "speak" checkbox if we find that we have speech support for the
   * current language (showing an initially hidden element is a better experience
   * than hiding an initially shown element... arguably... ?)
   *
   * Also, for funzies: the speechSynthesis.getVoices() array is asynchronously
   * populated *some time* after the page loads... and we won't know when. Keep
   * on testing periodically until we got it or it's taken too long to finish.
   */
  let attempts = 0;
  const timer = setInterval(function() {
    attempts += 1;

    const voices = findVoices(window.State.lang);

    if (voices.length > 0) {
      for (const voice of voices) {
        $('#speak_dropdown').append($('<option>').attr('value', voice.voiceURI).text('📣 ' + voice.name));
      }

      $('#speak_container').show();

      clearInterval(timer);
    }
    if (attempts >= 20) {  // ~2 seconds
      // Give up
      clearInterval(timer);
    }
  }, 100);

  function findVoices(lang) {
    // Our own "lang" is *typically* just the language code, but we also have "pt_BR".
    const simpleLang = lang.match(/^([a-z]+)/i)[1];

    // If the feature doesn't exist in the browser, return null
    if (!window.speechSynthesis) { return []; }
    return window.speechSynthesis.getVoices().filter(voice => voice.lang.startsWith(simpleLang));
  }
})();

window.create_class = function create_class() {
  window.modal.prompt (window.auth.texts.class_name_prompt, '', function (class_name) {

    $.ajax({
      type: 'POST',
      url: '/class',
      data: JSON.stringify({
        name: class_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      location.reload ();
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
    });
  });
}

window.rename_class = function rename_class(id) {
  window.modal.prompt (window.auth.texts.class_name_prompt, '', function (class_name) {

    $.ajax({
      type: 'PUT',
      url: '/class/' + id,
      data: JSON.stringify({
        name: class_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      location.reload ();
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
    });
  });
}

window.delete_class = function delete_class(id) {
  window.modal.confirm (window.auth.texts.delete_class_prompt, function () {

    $.ajax({
      type: 'DELETE',
      url: '/class/' + id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      window.location.pathname = '/for-teachers';
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
    });
  });
}

window.join_class = function join_class(link, name, noRedirect) {
  // If there's no session but we want to join the class, we store the program data in localStorage and redirect to /login.
  if (! window.auth.profile) {
    return window.modal.confirm (window.auth.texts.join_prompt, function () {
      localStorage.setItem ('hedy-join', JSON.stringify ({link: link, name: name}));
      window.location.pathname = '/login';
      return;
    });
  }

  $.ajax({
    type: 'GET',
    url: link,
  }).done(function(response) {
    window.modal.alert (window.auth.texts.class_join_confirmation + ' ' + name);
    if (! noRedirect) window.location.pathname = '/programs';
  }).fail(function(err) {
    console.error(err);
    error.show(ErrorMessages.Connection_error, JSON.stringify(err));
  });
}

window.remove_student = function delete_class(class_id, student_id) {
  window.modal.confirm (window.auth.texts.remove_student_prompt, function () {

    $.ajax({
      type: 'DELETE',
      url: '/class/' + class_id + '/student/' + student_id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      location.reload ();
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
    });
  });
}

window.prompt_unsaved = function prompt_unsaved(cb) {
  if (! window.State.unsaved_changes) return cb ();
  // This variable avoids showing the generic native `onbeforeunload` prompt
  window.State.no_unload_prompt = true;
  window.modal.confirm (window.auth.texts.unsaved_changes, cb);
}
