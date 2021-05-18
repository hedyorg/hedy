var feedback_level;
var prev_feedback_level;
var similar_code;
var prev_similar_code;
var general_answer = null;
var last_question;
var level_answers = [null, null, null, null];
var feedback_viewed = [null, null, null, null];

(function() {

  // If there's no #editor div, we're requiring this code in a non-code page.
  // Therefore, we don't need to initialize anything.
  if (! $ ('#editor').length) return;

  // *** EDITOR SETUP ***
  // We expose the editor globally so it's available to other functions for resizing
  var editor = window.editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");

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
  }


  // Load existing code from session, if it exists
  const storage = window.sessionStorage;
  if (storage) {
    const levelKey = $('#editor').data('lskey');
    const loadedProgram = $('#editor').data('loaded-program');

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
        code: code,
        lang: lang,
        adventure_name: window.State.adventure_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      feedback_level = response.feedback_level;
      prev_feedback_level = response.prev_feedback_level;
      feedback_viewed[feedback_level-2] = false; // Not viewed until we have viewed it
      prev_similar_code = response.prev_similar_code;

      if (response.Duplicate) {
        $ ('#feedbackbox .expand-dialog').text("▲ " + GradualErrorMessages.Click_expand + " ▲")
        error.showFeedback(ErrorMessages.Feedback_duplicate, response.Feedback);
      }
      else {
        if (response.Feedback) {
          $ ('#feedbackbox .expand-dialog').text("▲ " + GradualErrorMessages.Click_expand + " ▲")
          if (response.feedback_level === 3) {
            error.showFeedback(ErrorMessages.Feedback_similar_code, response.Feedback);
          } else if (response.feedback_level == 4) {
            error.showFeedback(ErrorMessages.Feedback_new, response.Feedback);
          } else if (response.feedback_level == 5) {
            error.showFeedback(ErrorMessages.Feedback_suggestion, response.Feedback);
          }  else {
            error.showFeedback(ErrorMessages.Feedback_error, response.Feedback);
          }
        }
      }
      if (response.Warning) {
        error.showWarning(ErrorMessages.Transpile_warning, response.Warning);
      }
      if (response.Error && response.feedback_level) { // Only enforce error reading when using the GFM model
        error.show(ErrorMessages.Transpile_error, response.Error);
        window.State.disable_run = true;
        var btn = $('#runit');
        btn.prop('disabled', true);
        btn.css("background", "gray");
        btn.css("border-bottom", "4px solid black");
        setTimeout(function () {
          btn.prop('disabled', false);
          btn.css('background-color', ''); //reset to original color
          btn.css("border-bottom", '');
          window.State.disable_run = false;
        }, 2500);
        return;
      }
      runPythonProgram(response.Code, cb).catch(function(err) {
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
 * Called when the user clicks the "Try" button in one of the palette buttons
 */
function tryPaletteCode(exampleCode) {
  var editor = ace.edit("editor");

  var MOVE_CURSOR_TO_END = 1;
  editor.setValue(exampleCode, MOVE_CURSOR_TO_END);
  window.State.unsaved_changes = false;
}


window.saveit = function saveit(level, lang, name, code, cb) {
  error.hide();

  if (reloadOnExpiredSession ()) return;

  try {
    // If there's no session but we want to save the program, we store the program data in localStorage and redirect to /login.
    if (! window.auth.profile) {
       if (! confirm (window.auth.texts.save_prompt)) return;
       // If there's an adventure_name, we store it together with the level, because it won't be available otherwise after signup/login.
       if (window.State.adventure_name) level = [level, window.State.adventure_name];
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
      if (cb) return response.Error ? cb (response) : cb ();
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
          adventure.loaded_program_name = name;
          adventure.loaded_program      = code;
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

function get_level_question(level) {
  if (level == 2) {
    last_question = 2;
    return GradualErrorMessages.Feedback_question2;
  } else if (level == 3) {
    last_question = 3;
    return GradualErrorMessages.Feedback_question3;
  } else if (level == 4) {
    last_question = 4;
    return GradualErrorMessages.Feedback_question4;
  } else {
    last_question = 5;
    return GradualErrorMessages.Feedback_question5;
  }
}

function feedback(answer) {
  if (answer == null) { // The user didn't look at any part of the model
    $.ajax({
      type: 'POST',
      url: '/feedback',
      data: JSON.stringify({
        general_answer: null,
        level_answers: [null, null, null, null],
        collapse: feedback_viewed,
        similar_code: "-",
      }),
      contentType: 'application/json',
      dataType: 'json'
    });
    $('#feedback-popup').hide();
    $('#opaque').hide();
    feedback_viewed = [null, null, null, null];
    general_answer = null;
  } else if (general_answer == null) {
    last_question = 0;
    general_answer = answer;
    $('#feedback-popup .caption').text(get_level_question(feedback_viewed.indexOf(true)+2))
  } else {
    level_answers[last_question - 2] = answer;
    if (feedback_viewed.indexOf((true), last_question - 1) != -1) { // So there is some question left
      $('#feedback-popup .caption').text(get_level_question((feedback_viewed.indexOf((true), last_question - 1) + 2)));
    } else {
      if (prev_feedback_level >= 3) { // So similar code has been shown to the end-user, how do we retrieve it?
        similar_code = prev_similar_code
      } else {
        similar_code = "-" // No similar code has been given to the user
      }
      $.ajax({
        type: 'POST',
        url: '/feedback',
        data: JSON.stringify({
          general_answer: general_answer,
          level_answers: level_answers,
          collapse: feedback_viewed,
          similar_code: similar_code,
          feedback_level: prev_feedback_level
        }),
        contentType: 'application/json',
        dataType: 'json'
      });
      $('#feedback-popup').hide();
      $('#opaque').hide();
      feedback_viewed = [null, null, null, null]; // Set back to false to ensure that it won't pop-up in next error streak without looking
      general_answer = null; // Set back to false to ensure that both questions are asked again in next mistake session
    }
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

// Notes from Timon
// In the function below the actual output of the program is ran
// If there is a feedback level higher then 1: pop-up a window with feedback question
// Then, post this question through app.py and log the yes / no answer and the collapse boolean
function runPythonProgram(code, cb) {
  if (prev_feedback_level > 1) {
    if (feedback_viewed.indexOf(true) != -1) { // So there is a true value somewhere -> the user look at the feedback
      var count = 0;
      $('#feedback-popup .caption').text(GradualErrorMessages.Feedback_question_general)
      $('#feedback-popup .yes').text(GradualErrorMessages.Feedback_answerY)
      $('#feedback-popup .no').text(GradualErrorMessages.Feedback_answerN)
      $('#feedback-popup').show();
      $('#opaque').show();
    }
    else {
      feedback(null);
    }
  }

  $('#runit').css('background-color', ''); //reset to original color
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

$('#feedbackbox .expand-dialog').click(function(){
   feedback_viewed[feedback_level-2] = true;
   $ ('#feedbackbox .details').toggle();
   var text = $ ('#feedbackbox .expand-dialog').text();
   if (text === "▼ " + GradualErrorMessages.Click_shrink + " ▼"){
      $ ('#feedbackbox .expand-dialog').text("▲ " + GradualErrorMessages.Click_expand + " ▲")
   }
   else {
     $ ('#feedbackbox .expand-dialog').text("▼ " + GradualErrorMessages.Click_shrink + " ▼")
   }
});

var error = {
  hide() {
    $('#errorbox').hide();
    $('#warningbox').hide();
    $('#feedbackbox').hide();
    if ($ ('#editor').length) editor.resize ();
  },

  showWarning(caption, message) {
    $('#warningbox .caption').text(caption);
    $('#warningbox .details').text(message);
    $('#warningbox').show();
    if ($ ('#editor').length) editor.resize ();
  },

  showFeedback(caption, message) {
    $('#feedbackbox .caption').text(caption);
    var obj = $("#feedbackbox .details").text(message);
    obj.html(obj.html().replace(/\n/g,'<br/>'));
    $('#feedbackbox').show();
    $("#feedbackbox .details").hide();
    editor.resize ();
  },

  show(caption, message) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').text(message);
    $('#errorbox').show();
    if ($ ('#editor').length) editor.resize ();
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
