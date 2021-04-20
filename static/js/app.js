var prev_feedback_level;
var prev_similar_code;
var similar_code;
var general_answer;
var feedback_viewed = false;
var general_answered = false;

(function() {

  // If there's no #editor div, we're requiring this code in a non-code page.
  // Therefore, we don't need to initialize anything.
  if (! $ ('#editor').length) return;

  // *** EDITOR SETUP ***
  // We expose the editor globally so it's available to other functions for resizing
  var editor = window.editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");

    if (window.State.level == 1){
      window.editor.session.setMode("ace/mode/level1");
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
        lang: lang
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      prev_feedback_level = response.prev_feedback_level;
      prev_similar_code = response.prev_similar_code;
      console.log('Response', response);
      if (response.Duplicate) {
        error.showFeedback(ErrorMessages.Feedback_duplicate, response.Feedback);
      }
      else {
        if (response.Feedback) {
          $ ('#feedbackbox .expand-dialog').text(GradualErrorMessages.Click_expand)
          if (response.feedback_level === 4) {
            error.showFeedback(ErrorMessages.Feedback_similar_code, response.Feedback);
          } else {
            error.showFeedback(ErrorMessages.Feedback_error, response.Feedback);
          }
        }
      }
      if (response.Warning) {
        error.showWarning(ErrorMessages.Transpile_warning, response.Warning);
      }
      if (response.Error) {
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
        // Todo: We have to make some implementation changes to give the user some additional feedback here as well
        // Current idea:
        /*
          Make an additional POST to app.py and catch the updates on the GFI model
          Implement the feedback similarly to how it is done above, this will result in (a lot) of duplicate code
          The next step is to re-write the feedback-call and the button_disable-call into a function
          Then these are call in the response in runit() as well as the response here
         */
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

window.saveit = function saveit(level, lang, name, code, cb) {
  error.hide();

  if (reloadOnExpiredSession ()) return;

  if (name === true) name = $ ('#program_name').val ();

  window.State.unsaved_changes = false;

  try {
    if (! window.auth.profile) {
       if (! confirm (window.auth.texts.save_prompt)) return;
       localStorage.setItem ('hedy-first-save', JSON.stringify ([level, lang, name, code]));
       window.location.pathname = '/login';
       return;
    }

    $.ajax({
      type: 'POST',
      url: '/programs',
      data: JSON.stringify({
        level: level,
        lang:  lang,
        name:  name,
        code:  code
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
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
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages.Connection_error, JSON.stringify(err));
      if (err.status === 403) {
         localStorage.setItem ('hedy-first-save', JSON.stringify ([level, lang, name, code]));
         localStorage.setItem ('hedy-save-redirect', 'hedy');
         window.location.pathname = '/login';
      }
    });
  } catch (e) {
    console.error(e);
    error.show(ErrorMessages.Other_error, e.message);
  }
}

function get_level_question() {
  if (prev_feedback_level == 2) {
    return GradualErrorMessages.Feedback_question2;
  } else if (prev_feedback_level == 3) {
    return GradualErrorMessages.Feedback_question3;
  } else if (prev_feedback_level == 4) {
    return GradualErrorMessages.Feedback_question4;
  } else {
    return GradualErrorMessages.Feedback_question5;
  }
}

function feedback(answer) {
  if (general_answered == false) {
    general_answer = answer;
    general_answered = true
    $('#feedback-popup .caption').text(get_level_question()) // Change to level-dependent text
  } else {
    if (prev_feedback_level >= 4) { // So similar code has been shown to the end-user, how do we retrieve it?
      similar_code = prev_similar_code
    } else {
      similar_code = "-" // No similar code has been given to the user
    }
    level_answer = answer;
    $.ajax({
      type: 'POST',
      url: '/feedback',
      data: JSON.stringify({
        general_answer: general_answer,
        level_answer: level_answer,
        collapse: feedback_viewed,
        similar_code: similar_code,
        feedback_level: prev_feedback_level
      }),
      contentType: 'application/json',
      dataType: 'json'
    });
    $('#feedback-popup').hide();
    $('#opaque').hide();
    feedback_viewed = false; // Set back to false to ensure that it won't pop-up in next error streak without looking
    general_answered = false; // Set back to false to ensure that both questions are asked again in next mistake session
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
    if (feedback_viewed == true) {
      $('#feedback-popup .caption').text(GradualErrorMessages.Feedback_question_general)
      $('#feedback-popup .yes').text(GradualErrorMessages.Feedback_answerY)
      $('#feedback-popup .no').text(GradualErrorMessages.Feedback_answerN)
      $('#feedback-popup').show();
      $('#opaque').show();
    } else {
      feedback(false);
      feedback(false);
      // We have to call feedback() twice due to the code structure: not ideal of course
      // However, this way we are able to log the users error-solving even when the ECEM is not read
    }
  }
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

$('#feedbackbox').click(function(){
   feedback_viewed = true;
   $ ('#feedbackbox .details').toggle();
   var text = $ ('#feedbackbox .expand-dialog').text();
   if (text === GradualErrorMessages.Click_shrink){
      $ ('#feedbackbox .expand-dialog').text(GradualErrorMessages.Click_expand)
   }
   else {
     $ ('#feedbackbox .expand-dialog').text(GradualErrorMessages.Click_shrink)
   }
});

var error = {
  hide() {
    $('#errorbox').hide();
    $('#warningbox').hide();
    $('#feedbackbox').hide();
    editor.resize ();
  },

  showWarning(caption, message) {
    $('#warningbox .caption').text(caption);
    $('#warningbox .details').text(message);
    $('#warningbox').show();
    editor.resize ();
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
    editor.resize ();
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
