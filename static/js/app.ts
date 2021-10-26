// It's important that this file gets loaded first
import './syntaxModesRules';

import { modal, error } from './modal';
import { auth } from './auth';

export let theGlobalEditor: AceAjax.Editor;

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
    // And add an overlay button to the editor, if the no-copy-button attribute isn't there
    if (! $(preview).hasClass('no-copy-button')) {
      const buttonContainer = $('<div>').css({ position: 'absolute', top: 5, right: 5, width: 'auto' }).appendTo(preview);
      $('<button>').attr('title', UiMessages['try_button']).css({ fontFamily: 'sans-serif' }).addClass('green-btn').text('⇥').appendTo(buttonContainer).click(function() {
        theGlobalEditor?.setValue(exampleEditor.getValue() + '\n');
      });
    }
  }

  /**
   * Initialize the main editor and attach all the required event handlers
   */
  function initializeMainEditor($editor: JQuery) {
    if (!$editor.length) return;

    // We expose the editor globally so it's available to other functions for resizing
    var editor = turnIntoAceEditor($editor.get(0)!, $editor.data('readonly'));
    theGlobalEditor = editor;
    error.setEditor(editor);

    window.Range = ace.require('ace/range').Range // get reference to ace/range

    // Load existing code from session, if it exists
    const storage = window.sessionStorage;
    if (storage) {
      const levelKey = $editor.data('lskey');
      const loadedProgram = $editor.data('loaded-program');

      // On page load, if we have a saved program and we are not loading a program by id, we load the saved program
      const programFromStorage = storage.getItem(levelKey);
      if (loadedProgram !== 'True' && programFromStorage) {
        editor.setValue(programFromStorage, 1);
      }

      // When the user exits the editor, save what we have.
      editor.on('blur', function(_e: Event) {
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

    window.onbeforeunload = () => {
      // The browser doesn't show this message, rather it shows a default message.
      if (window.State.unsaved_changes && !window.State.no_unload_prompt) {
        return auth.texts['unsaved_changes'];
      } else {
        return undefined;
      }
    };

    // *** KEYBOARD SHORTCUTS ***

    let altPressed: boolean | undefined;

    // alt is 18, enter is 13
    window.addEventListener ('keydown', function (ev) {
      const keyCode = ev.keyCode;
      if (keyCode === 18) {
        altPressed = true;
        return;
      }
      if (keyCode === 13 && altPressed) {
        if (!window.State.level || !window.State.lang) {
          throw new Error('Oh no');
        }
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
      const keyCode = ev.keyCode;
      if (keyCode === 18) {
        altPressed = false;
        return;
      }
    });
    return editor;
  }

  /**
   * Turn an HTML element into an Ace editor
   */
  function turnIntoAceEditor(element: HTMLElement, isReadOnly: boolean): AceAjax.Editor {
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
      // this table. Yes the numbers are strings. That's just JavaScript for you.
      const modeExceptions: Record<string, string> = {
        '9': 'ace/mode/level9and10',
        '10': 'ace/mode/level9and10',
        '18': 'ace/mode/level18and19',
        '19': 'ace/mode/level18and19',
      };

      if (window.State.level) {
        const mode = modeExceptions[window.State.level] || `ace/mode/level${window.State.level}`;
        editor.session.setMode(mode);
      }
    }

    return editor;
  }
})();

function reloadOnExpiredSession () {
   // If user is not logged in or session is not expired, return false.
   if (! auth.profile || auth.profile.session_expires_at > Date.now ()) return false;
   // Otherwise, reload the page to update the top bar.
   location.reload ();
   return true;
}

function clearErrors(editor: AceAjax.Editor) {
  editor.session.clearAnnotations();
  for (const marker in editor.session.getMarkers(false)) {
    editor.session.removeMarker(marker as any);
  }
}

export function runit(level: string, lang: string, cb: () => void) {
  if (window.State.disable_run) return modal.alert (auth.texts['answer_question']);

  if (reloadOnExpiredSession ()) return;

  error.hide();
  try {
    level = level.toString();
    var editor = theGlobalEditor;
    var code = get_trimmed_code();

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
        error.showWarning(ErrorMessages['Transpile_warning'], response.Warning);
      }
      if (response.Error) {
        error.show(ErrorMessages['Transpile_error'], response.Error);
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
            new ace.Range(
                response.Location[0] - 1,
                response.Location[1] - 1,
                response.Location[0] - 1,
                response.Location[1],
            ),
            "editor-error", "fullLine", false
          );
        }
        return;
      }
      runPythonProgram(response.Code, response.has_turtle, cb).catch(function(err) {
        console.log(err)
        error.show(ErrorMessages['Execute_error'], err.message);
        reportClientError(level, code, err.message);
      });
    }).fail(function(xhr) {
      console.error(xhr);
      // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState
      if (xhr.readyState < 4) {
        error.show(ErrorMessages['Connection_error'], ErrorMessages['CheckInternet']);
      } else {
        error.show(ErrorMessages['Other_error'], ErrorMessages['ServerError']);
      }
    });

  } catch (e: any) {
    console.error(e);
    error.show(ErrorMessages['Other_error'], e.message);
  }
}

/**
 * Called when the user clicks the "Try" button in one of the palette buttons
 */
export function tryPaletteCode(exampleCode: string) {
  var editor = ace.edit("editor");

  var MOVE_CURSOR_TO_END = 1;
  editor.setValue(exampleCode + '\n', MOVE_CURSOR_TO_END);
  window.State.unsaved_changes = false;
}

export function saveit(level: number | [number, string], lang: string, name: string, code: string, cb?: (err: any, resp?: any) => void) {
  error.hide();

  if (reloadOnExpiredSession ()) return;

  try {
    // If there's no session but we want to save the program, we store the program data in localStorage and redirect to /login.
    if (! auth.profile) {
       return modal.confirm (auth.texts['save_prompt'], function () {
         // If there's an adventure_name, we store it together with the level, because it won't be available otherwise after signup/login.
         if (window.State && window.State.adventure_name && !Array.isArray(level)) level = [level, window.State.adventure_name];
         localStorage.setItem ('hedy-first-save', JSON.stringify ([level, lang, name, code]));
         window.location.pathname = '/login';
       });
    }

    window.State.unsaved_changes = false;

    var adventure_name = window.State.adventure_name;
    // If saving a program for an adventure after a signup/login, level is an array of the form [level, adventure_name]. In that case, we unpack it.
    if (Array.isArray(level)) {
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
        error.showWarning(ErrorMessages['Transpile_warning'], response.Warning);
      }
      if (response.Error) {
        error.show(ErrorMessages['Transpile_error'], response.Error);
        return;
      }
      modal.alert (auth.texts['save_success_detail'], 4000);
      // If we succeed, we need to update the default program name & program for the currently selected tab.
      // To avoid this, we'd have to perform a page refresh to retrieve the info from the server again, which would be more cumbersome.
      // The name of the program might have been changed by the server, so we use the name stated by the server.
      $ ('#program_name').val (response.name);
      window.State.adventures?.map (function (adventure) {
        if (adventure.short_name === (adventure_name || 'level')) {
          adventure.loaded_program = {name: response.name, code: code};
        }
      });
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
      if (err.status === 403) {
         localStorage.setItem ('hedy-first-save', JSON.stringify ([adventure_name ? [level, adventure_name] : level, lang, name, code]));
         localStorage.setItem ('hedy-save-redirect', 'hedy');
         window.location.pathname = '/login';
      }
    });
  } catch (e: any) {
    console.error(e);
    error.show(ErrorMessages['Other_error'], e.message);
  }
}

/**
 * The 'saveit' function, as an async function
 */
export function saveitP(level: number | [number, string], lang: string, name: string, code: string) {
  return new Promise<any>((ok, ko) => {
    saveit(level, lang, name, code, (err, response) => {
      if (err) {
        ko(err);
      } else {
        ok(response);
      }
    });
  });
}

export function viewProgramLink(programId: string) {
  return window.location.origin + '/hedy/' + programId + '/view';
}

export function share_program (level: number, lang: string, id: string | true, Public: boolean, reload?: boolean) {
  if (! auth.profile) return modal.alert (auth.texts['must_be_logged']);

  var share = function (id: string) {
    $.ajax({
      type: 'POST',
      url: '/programs/share',
      data: JSON.stringify({
        id: id,
        public: Public
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(_response) {
      // If we're sharing the program, copy the link to the clipboard.
      if (Public) copy_to_clipboard (viewProgramLink(id), true);
      modal.alert (Public ? auth.texts['share_success_detail'] : auth.texts['unshare_success_detail'], 4000);
      if (reload) setTimeout (function () {location.reload ()}, 1000);
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
  }

  // If id is not true, the request comes from the programs page. In that case, we merely call the share function.
  if (id !== true) return share (id);

  // Otherwise, we save the program and then share it.
  // Saving the program makes things way simpler for many reasons: it covers the cases where:
  // 1) there's no saved program; 2) there's no saved program for that user; 3) the program has unsaved changes.
  const name = `${$('#program_name').val()}`;
  const code = get_trimmed_code();
  return saveit(level, lang, name, code, (err: any, resp: any) => {
      if (err && err.Warning)
        return error.showWarning(ErrorMessages['Transpile_warning'], err.Warning);
      if (err && err.Error)
        return error.show(ErrorMessages['Transpile_error'], err.Error);
      share(resp.id);
    });

}

export function copy_to_clipboard (string: string, noAlert: boolean) {
  // https://hackernoon.com/copying-text-to-clipboard-with-javascript-df4d4988697f
  var el = document.createElement ('textarea');
  el.value = string;
  el.setAttribute ('readonly', '');
  el.style.position = 'absolute';
  el.style.left = '-9999px';
  document.body.appendChild (el);

  const selection = document.getSelection();
  const originalSelection = selection && selection.rangeCount > 0 ? selection.getRangeAt(0) : undefined;

  el.select ();
  document.execCommand ('copy');
  document.body.removeChild (el);
  if (originalSelection) {
     document.getSelection()?.removeAllRanges ();
     document.getSelection()?.addRange (originalSelection);
  }
  if (! noAlert) modal.alert (auth.texts['copy_clipboard'], 4000);
}

/**
 * Do a POST with the error to the server so we can log it
 */
function reportClientError(level: string, code: string, client_error: string) {
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

function runPythonProgram(code: string, hasTurtle: boolean, cb: () => void) {
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
  }).then(function(_mod) {
    console.log('Program executed');
    // Check if the program was correct but the output window is empty: Return a warning
    if ($('#output').is(':empty') && $('#turtlecanvas').is(':empty')) {
      error.showWarning(ErrorMessages['Transpile_warning'], ErrorMessages['Empty_output']);
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
  function errorMessageFromSkulptError(err: any) {
    const message = err.args && err.args.v && err.args.v[0] && err.args.v[0].v;
    return message;
  }

  function addToOutput(text: string, color: string) {
    $('<span>').text(text).css({ color }).appendTo(outputDiv);
  }


  // output functions are configurable.  This one just appends some text
  // to a pre element.
  function outf(text: string) {
    addToOutput(text, 'white');
    speak(text)
  }

  function builtinRead(x: string) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
  }

  // This method draws the prompt for asking for user input.
  function inputFromInlineModal(prompt: string) {
    $('#turtlecanvas').empty();
    return new Promise(function(ok) {

      window.State.disable_run = true;
      $ ('#runit').css('background-color', 'gray');

      const input = $('#inline-modal input[type="text"]');
      $('#inline-modal .caption').text(prompt);
      input.val('');
      input.attr('placeholder', prompt);
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

function speak(text: string) {
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

(() => {
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

    const voices = findVoices(window.State.lang ?? '');

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

  function findVoices(lang: string) {
    // Our own "lang" is *typically* just the language code, but we also have "pt_BR".
    const m = lang.match(/^([a-z]+)/i);
    if (!m) { return []; }
    const simpleLang = m[1];

    // If the feature doesn't exist in the browser, return null
    if (!window.speechSynthesis) { return []; }
    return window.speechSynthesis.getVoices().filter(voice => voice.lang.startsWith(simpleLang));
  }
})();

export function prompt_unsaved(cb: () => void) {
  if (! window.State.unsaved_changes) return cb ();
  // This variable avoids showing the generic native `onbeforeunload` prompt
  window.State.no_unload_prompt = true;
  modal.confirm(auth.texts['unsaved_changes'], cb);
}

export function load_quiz(level: string) {
  $('*[data-tabtarget="end"]').html ('<iframe id="quiz-iframe" class="w-full" title="Quiz" src="/quiz/start/' + level + '"></iframe>');
}

export function get_trimmed_code() {
  try {
    // This module may or may not exist, so let's be extra careful here.
    const whitespace = ace.require("ace/ext/whitespace");
    whitespace.trimTrailingSpace(theGlobalEditor.session, true);
  } catch (e) {
    console.error(e);
  }
  return theGlobalEditor?.getValue();
}

