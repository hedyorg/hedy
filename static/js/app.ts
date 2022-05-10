// It's important that this file gets loaded first
import './syntaxModesRules';

import { modal, error, success } from './modal';
import { auth } from './auth';

export let theGlobalEditor: AceAjax.Editor;
export let theModalEditor: AceAjax.Editor;

(function() {
  // A bunch of code expects a global "State" object. Set it here if not
  // set yet.
  if (!window.State) {
    window.State = {};
  }

  // Set const value to determine the current page direction -> useful for ace editor settings
  const dir = $("#main_container").attr("dir");

  // *** EDITOR SETUP ***
  initializeMainEditor($('#editor'));

  // Any code blocks we find inside 'turn-pre-into-ace' get turned into
  // read-only editors (for syntax highlighting)
  let counter = 0
  for (const preview of $('.turn-pre-into-ace pre').get()) {
    counter += 1;
    $(preview).addClass('text-lg rounded');
    $(preview).attr('id', "code_block_" + counter);
    // We set the language of the editor to the current keyword_language -> needed when copying to main editor
    $(preview).attr('lang', <string>window.State.keyword_language);
    $(preview).addClass('overflow-x-hidden');
    const exampleEditor = turnIntoAceEditor(preview, true);

    // Fits to content size
    exampleEditor.setOptions({ maxLines: Infinity });
    if ($(preview).hasClass('common-mistakes')) {
      exampleEditor.setOptions({ minLines: 10 });
    } else if ($(preview).hasClass('cheatsheet')) {
      exampleEditor.setOptions({ minLines: 1 });
    } else {
      exampleEditor.setOptions({ minLines: 2 });
    }

    if (dir === "rtl") {
         exampleEditor.setOptions({ rtl: true });
    }
    // Strip trailing newline, it renders better
    exampleEditor.setValue(exampleEditor.getValue().replace(/\n+$/, ''), -1);
    // And add an overlay button to the editor, if the no-copy-button attribute isn't there
    if (! $(preview).hasClass('no-copy-button')) {
      const buttonContainer = $('<div>').addClass('absolute ltr:-right-1 rtl:left-2 w-16').css({top: 5}).appendTo(preview);
      let symbol = "⇥";
      if (dir === "rtl") {
        symbol = "⇤";
      }
      $('<button>').css({ fontFamily: 'sans-serif' }).addClass('green-btn').text(symbol).appendTo(buttonContainer).click(function() {
        theGlobalEditor?.setValue(exampleEditor.getValue() + '\n');
        update_view("main_editor_keyword_selector", <string>$(preview).attr('lang'));
      });
    }
    if($(preview).attr('level')){
      let level = String($(preview).attr('level'));
      exampleEditor.session.setMode(getHighlighter(level));
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

      if (dir === "rtl") {
         editor.setOptions({ rtl: true });
      }

      // If prompt is shown and user enters text in the editor, hide the prompt.
      editor.on('change', function () {
        if ($('#inline-modal').is (':visible')) $('#inline-modal').hide();
        window.State.disable_run = false;
        $ ('#runit').css('background-color', '');
        window.State.unsaved_changes = true;

        clearErrors(editor);
        //removing the debugging state when loading in the editor
      stopDebug();
      });
    }

    // *** PROMPT TO SAVE CHANGES ***

    window.onbeforeunload = () => {
      // The browser doesn't show this message, rather it shows a default message.
      if (window.State.unsaved_changes && !window.State.no_unload_prompt) {
        return ErrorMessages['Unsaved_Changes'];
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
        runit (window.State.level, window.State.lang, "", function () {
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
      // When it is the main editor -> we want to show line numbers!
      if (element.getAttribute('id') === "editor") {
        editor.setOptions({
          showGutter: true
        });
      }
      if ($(element).hasClass('common-mistakes')) {
        $(element).height("22rem");
        editor.setOptions({
          showGutter: true,
          showPrintMargin: true,
          highlightActiveLine: true
        });
      }
    }

    // a variable which turns on(1) highlighter or turns it off(0)
    var highlighter = 1;

    if (highlighter == 1) {
      // Everything turns into 'ace/mode/levelX', except what's in
      // this table. Yes the numbers are strings. That's just JavaScript for you.
      if (window.State.level) {
        const mode = getHighlighter(window.State.level);
        editor.session.setMode(mode);
      }
    }

    return editor;
  }
})();

export function getHighlighter(level: string) {
  return `ace/mode/level` + level;
}

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

export function stopit() {
  // We bucket-fix stop the current program by setting the run limit to 1ms
  Sk.execLimit = 1;
  $('#stopit').hide();
  $('#runit').show();

  // This gets a bit complex: if we do have some input modal waiting, fake submit it and hide it
  // This way the Promise is no longer "waiting" and can no longer mess with our next program
  if ($('#inline-modal').is(":visible")) {
    $('#inline-modal form').submit();
    $('#inline-modal').hide();
  }

  window.State.disable_run = false;
}

export function runit(level: string, lang: string, disabled_prompt: string, cb: () => void) {
  if (window.State.disable_run) {
    // If there is no message -> don't show a prompt
    if (disabled_prompt) {
      return modal.alert(disabled_prompt, 3000, true);
    } return;
  }
  if (reloadOnExpiredSession ()) return;

  // We set the run limit to 1ms -> make sure that the previous programs stops (if there is any)
  Sk.execLimit = 1;
  $('#runit').hide();
  $('#stopit').show();

  const outputDiv = $('#output');
  //Saving the variable button because sk will overwrite the output div
  const variableButton = $(outputDiv).find('#variable_button');
  const variables = $(outputDiv).find('#variables');
  outputDiv.empty();

  outputDiv.addClass("overflow-auto");
  outputDiv.append(variableButton);
  outputDiv.append(variables);
  error.hide();
  success.hide();

  try {
    level = level.toString();
    var editor = theGlobalEditor;
    var code = get_trimmed_code();

    clearErrors(editor);
    removeBulb();
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
    }).done(function(response: any) {
      console.log('Response', response);
      if (response.Warning) {
        storeFixedCode(response, level);
        error.showWarning(ErrorMessages['Transpile_warning'], response.Warning);
      }
      if (response.achievements) {
        showAchievements(response.achievements, false, "");
      }
      if (response.Error) {
        error.show(ErrorMessages['Transpile_error'], response.Error);
        if (response.Location && response.Location[0] != "?") {
          storeFixedCode(response, level);
          // Location can be either [row, col] or just [row].
          // @ts-ignore
          highlightAceError(editor, response.Location[0], response.Location[1]);
        }
        $('#stopit').hide();
        $('#runit').show();
        return;
      }
      runPythonProgram(response.Code, response.has_turtle, response.has_sleep, response.Warning, cb).catch(function(err) {
        // The err is null if we don't understand it -> don't show anything
        if (err != null) {
          error.show(ErrorMessages['Execute_error'], err.message);
          reportClientError(level, code, err.message);
        }
      });
    }).fail(function(xhr) {
      console.error(xhr);
       https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState
      if (xhr.readyState < 4) {
        error.show(ErrorMessages['Connection_error'], ErrorMessages['CheckInternet']);
      } else {
        error.show(ErrorMessages['Other_error'], ErrorMessages['ServerError']);
      }
    });

  } catch (e: any) {
    modal.alert(e.responseText, 3000, true);
  }
}

function storeFixedCode(response: any, level: string) {
  if (response.FixedCode) {
    sessionStorage.setItem ("fixed_level_{lvl}__code".replace("{lvl}", level), response.FixedCode);
    showBulb(level);
  }
}

function showBulb(level: string){
  const parsedlevel = parseInt(level)
  if(parsedlevel <= 2){
    const repair_button = $('#repair_button');
    repair_button.show();
    repair_button.attr('onclick', 'hedyApp.modalStepOne(' + parsedlevel + ');event.preventDefault();');
  }

}

export function pushAchievement(achievement: string) {
  $.ajax({
    type: 'POST',
    url: '/achievements',
    data: JSON.stringify({
      achievement: achievement
    }),
    contentType: 'application/json',
    dataType: 'json'
    }).done(function(response: any) {
      if (response.achievements) {
        showAchievements(response.achievements, false, "");
      }
  });
}

export function showAchievements(achievements: any[], reload: boolean, redirect: string) {
  fnAsync(achievements, 0);
  if (reload) {
    setTimeout(function(){
      location.reload();
     }, achievements.length * 6000);
  }
  if (redirect) {
    setTimeout(function(){
      window.location.pathname = redirect;
     }, achievements.length * 6000);
  }
}

async function fnAsync(achievements: any[], index: number) {
  await showAchievement(achievements[index]);
  if (index < achievements.length - 1) {
    await fnAsync(achievements, index + 1)
  }
}

function showAchievement(achievement: any[]){
  return new Promise<void>((resolve)=>{
        $('#achievement_reached_title').text('"' + achievement[0] + '"');
        $('#achievement_reached_text').text(achievement[1]);
        $('#achievement_pop-up').fadeIn(1000, function () {
          setTimeout(function(){
            $('#achievement_pop-up').fadeOut(1000);
           }, 4000);
        });
        setTimeout(()=>{
            resolve();
        ;} , 6000
        );
    });
}

function removeBulb(){
    const repair_button = $('#repair_button');
    repair_button.hide();
}

/**
 * Mark an error location in the ace editor
 *
 * The error occurs at the given row, and optionally has a column and
 * and a length.
 *
 * If 'col' is not given, the entire line will be highlighted red. Otherwise
 * the character at 'col' will be highlighted, optionally extending for
 * 'length' characters.
 *
 * 'row' and 'col' are 1-based.
 */
function highlightAceError(editor: AceAjax.Editor, row: number, col?: number, length=1) {
  // This adds a red cross in the left margin.
  // Not sure what the "column" argument does here -- it doesn't seem
  // to make a difference.
  editor.session.setAnnotations([
    {
      row: row - 1,
      column: (col ?? 1) - 1,
      text: '',
      type: 'error',
    }
  ]);

  if (col === undefined) {
    // Higlight entire row
    editor.session.addMarker(
      new ace.Range(row - 1, 1, row - 1, 2),
      "editor-error", "fullLine", false
    );
    return;
  }

  // Highlight span
  editor.session.addMarker(
    new ace.Range(
      row - 1, col - 1,
      row - 1, col - 1 + length,
    ),
    "editor-error", "text", false
  );
}

/**
 * Called when the user clicks the "Try" button in one of the palette buttons
 */
export function tryPaletteCode(exampleCode: string) {
  var editor = ace.edit("editor");

  var MOVE_CURSOR_TO_END = 1;
  editor.setValue(exampleCode + '\n', MOVE_CURSOR_TO_END);
  //As the commands try-it buttons only contain english code -> make sure the selected language is english
  if (!($('#editor').attr('lang') == 'en')) {
      $('#editor').attr('lang', 'en');
      update_view("main_editor_keyword_selector", "en");
  }
  window.State.unsaved_changes = false;
}

function storeProgram(level: number | [number, string], lang: string, name: string, code: string, shared: boolean, force_save: boolean, cb?: (err: any, resp?: any) => void) {
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
      shared: shared,
      force_save: force_save,
      adventure_name: adventure_name
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function(response) {
    // If the program contains an error -> verify that the user really wants to save it and POST again
    // If we already answered this question with yes the "force_save" is true, so we skip this part
    if (response.parse_error && !force_save) {
      modal.confirm(response.message, function() {
        return storeProgram(level, lang, name, code, shared, true, cb);
      });
      return;
    }
    // The auth functions use this callback function.
    if (cb) return response.Error ? cb (response) : cb (null, response);
    if (shared) {
      $('#modal-copy-button').attr('onclick', "hedyApp.copy_to_clipboard('" + viewProgramLink(response.id) + "')");
      modal.copy_alert (response.message, 5000);
    } else {
      modal.alert(response.message, 3000, false);
    }
    if (response.achievements) {
      showAchievements(response.achievements, false, "");
    }
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
}

export function saveit(level: number | [number, string], lang: string, name: string, code: string, shared: boolean, cb?: (err: any, resp?: any) => void) {
  if (reloadOnExpiredSession ()) return;
  try {
    $.ajax({
      type: 'POST',
      url: '/programs/duplicate-check',
      data: JSON.stringify({
        name:  name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      if (response['duplicate']) {
        modal.confirm (response.message, function () {
          storeProgram(level, lang, name, code, shared, false, cb);
          pushAchievement("double_check");
        });
      } else {
         storeProgram(level, lang, name, code, shared, false, cb);
      }
    }).fail(function(err) {
      if (err.status == 403) { // The user is not allowed -> so not logged in
        return modal.confirm (err.responseText, function () {
           // If there's an adventure_name, we store it together with the level, because it won't be available otherwise after signup/login.
           if (window.State && window.State.adventure_name && !Array.isArray(level)) {
             level = [level, window.State.adventure_name];
           }
           localStorage.setItem ('hedy-first-save', JSON.stringify ([level, lang, name, code, shared]));
           window.location.pathname = '/login';
         });
      }
    });
  } catch (e: any) {
    console.error(e);
    modal.alert(e.message, 3000, true);
  }
}

/**
 * The 'saveit' function, as an async function
 */
export function saveitP(level: number | [number, string], lang: string, name: string, code: string, shared: boolean) {
  return new Promise<any>((ok, ko) => {
    saveit(level, lang, name, code, shared,(err, response) => {
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

function change_shared (shared: boolean, index: number) {
  // Index is a front-end unique given to each program container and children
  // This value enables us to remove, hide or show specific element without connecting to the server (again)
  // When index is -1 we share the program from code page (there is no program container) -> no visual change needed
  if (index == -1) {
    return;
  }
  if (shared) {
    $('#non_public_button_container_' + index).hide();
    $('#public_button_container_' + index).show();
    $('#favourite_program_container_' + index).show();
  } else {
    $('#modal-copy-button').hide();
    $('#public_button_container_' + index).hide();
    $('#non_public_button_container_' + index).show();
    $('#favourite_program_container_' + index).hide();

    // In the theoretical situation that a user unshares their favourite program -> Change UI
    $('#favourite_program_container_' + index).removeClass('text-yellow-400');
    $('#favourite_program_container_' + index).addClass('text-white');
  }
}

export function share_program(id: string, index: number, Public: boolean) {
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
      if (response.achievement) {
        showAchievements(response.achievement, false, "");
      }
      if (Public) {
        $('#modal-copy-button').attr('onclick', "hedyApp.copy_to_clipboard('" + viewProgramLink(id) + "')");
        modal.copy_alert (response.message, 5000);
        change_shared(true, index);
      } else {
        modal.alert (response.message, 3000, false);
        change_shared(false, index);
      }
    }).fail(function(err) {
      modal.alert(err.responseText, 3000, true);
    });
}

export function delete_program(id: string, index: number, prompt: string) {
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'POST',
      url: '/programs/delete',
      data: JSON.stringify({
        id: id
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      if (response.achievement) {
          showAchievements(response.achievement, true, "");
      } else {
          $('#program_' + index).remove();
      }
      modal.alert(response.message, 3000, false);
    }).fail(function(err) {
      modal.alert(err.responseText, 3000, true);
    });
  });
}

function set_favourite(index: number) {
    $('.favourite_program_container').removeClass('text-yellow-400');
    $('.favourite_program_container').addClass('text-white');

    $('#favourite_program_container_' + index).removeClass('text-white');
    $('#favourite_program_container_' + index).addClass('text-yellow-400');
}

export function set_favourite_program(id: string, index: number, prompt: string) {
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'POST',
      url: '/programs/set_favourite',
      data: JSON.stringify({
        id: id
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      set_favourite(index)
      modal.alert (response.message, 3000, false);
    }).fail(function(err) {
      modal.alert(err.responseText, 3000, true);
    });
  });
}

function change_to_submitted (index: number) {
    // Index is a front-end unique given to each program container and children
    // This value enables us to remove, hide or show specific element without connecting to the server (again)
    $('#non_submitted_button_container_' + index).remove();
    $('#submitted_button_container_' + index).show();
    $('#submitted_header_' + index).show();
    $('#program_' + index).removeClass("border-orange-400");
    $('#program_' + index).addClass("border-gray-400 bg-gray-400");
}

export function submit_program (id: string, index: number) {
  $.ajax({
    type: 'POST',
    url: '/programs/submit',
    data: JSON.stringify({
      id: id
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function(response) {
    if (response.achievements) {
      showAchievements(response.achievements, false, "");
    }
    change_to_submitted(index);
  }).fail(function(err) {
      return modal.alert(err.responseText, 3000, true);
  });
}

export function set_explore_favourite(id: string, favourite: boolean) {
  let prompt = "Are you sure you want to remove this program as explore favourite?";
  if (favourite) {
    prompt = "Are you sure you want to set this program as explore favourite?";
  }
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'POST',
      url: '/programs/submit',
      data: JSON.stringify({
        id: id
    }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
        modal.alert(response.success, 3000, false);
        if (favourite) {
          $('#' + id).removeClass('text-white');
          $('#' + id).addClass('text-yellow-500');
        } else {
          $('#' + id).removeClass('text-yellow-500');
          $('#' + id).addClass('text-white');
        }
    }).fail(function(err) {
        return modal.alert(err.responseText, 3000, true);
    });
  });
}

export function copy_to_clipboard (string: string, prompt: string) {
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
  modal.hide_alert();
  modal.alert (prompt, 3000, false);
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

function runPythonProgram(this: any, code: string, hasTurtle: boolean, hasSleep: boolean, hasWarnings: boolean, cb: () => void) {
  const outputDiv = $('#output');
  //Saving the variable button because sk will overwrite the output div
  const variableButton = $(outputDiv).find('#variable_button');
  const variables = $(outputDiv).find('#variables');
  outputDiv.empty();
  outputDiv.append(variableButton);
  outputDiv.append(variables);

  var storage = window.localStorage;
  var debug = storage.getItem("debugLine")

  Sk.pre = "output";
  const turtleConfig = (Sk.TurtleGraphics || (Sk.TurtleGraphics = {}));
  turtleConfig.target = 'turtlecanvas';
  // If the adventures are not shown -> increase height of turtleConfig
  if ($('#adventures-tab').is(":hidden")) {
      turtleConfig.height = 600;
      turtleConfig.worldHeight = 600;
  } else {
      turtleConfig.height = 300;
      turtleConfig.worldHeight = 300;
  }
  // Always set the width to output panel width -> match the UI
  turtleConfig.width = $( '#output' ).width();
  turtleConfig.worldWidth = $( '#output' ).width();

  if (!hasTurtle) {
    // There might still be a visible turtle panel. If the new program does not use the Turtle,
    // remove it (by clearing the '#turtlecanvas' div)
    $('#turtlecanvas').empty();
  } else {
    // Otherwise make sure that it is shown as it might be hidden from a previous code execution.
    $('#turtlecanvas').show();
  }

  Sk.configure({
    output: outf,
    read: builtinRead,
    inputfun: inputFromInlineModal,
    inputfunTakesPrompt: true,
    __future__: Sk.python3,
    timeoutMsg: function () {
      // If the timeout is 1 this is due to us stopping the program: don't show "too long" warning
      $('#stopit').hide();
      $('#runit').show();
      if (Sk.execLimit != 1) {
        pushAchievement("hedy_hacking");
        return ErrorMessages ['Program_too_long'];
      } else {
        return null;
      }
    },
    // We want to make the timeout function a bit more sophisticated that simply setting a value
    // In levels 1-6 users are unable to create loops and programs with a lot of lines are caught server-sided
    // So: a very large limit in these levels, keep the limit on other onces.
    execLimit: (function () {
      const level = Number(window.State.level) || 0;
      if (level < 7) {
        // Set a non-realistic time-out of 5 minutes
        return (3000000);
      }
      // Set a time-out of either 20 seconds (when turtle / sleep) or 5 seconds when not
      return ((hasTurtle || hasSleep) ? 20000 : 5000);
    }) ()
  });

  return Sk.misceval.asyncToPromise( () =>
    Sk.importMainWithBody("<stdin>", false, code, true), {
      "*": () => {
        // We don't do anything here...
      }
    }
   ).then(function(_mod) {
    console.log('Program executed');
    //@ts-ignore
    const pythonVariables = Sk.globals;
    load_variables(pythonVariables);
    $('#stopit').hide();
    $('#runit').show();

    // Check if the program was correct but the output window is empty: Return a warning
    if (window.State.programsInExecution === 1 && $('#output').is(':empty') && $('#turtlecanvas').is(':empty')) {
      if(debug == null){
        pushAchievement("error_or_empty");
        error.showWarning(ErrorMessages['Transpile_warning'], ErrorMessages['Empty_output']);
      }
      return;
    }
    window.State.programsInExecution--;
    if (!hasWarnings) {
      if (debug == null) {
        showSuccesMessage();
      }
    }
    if (cb) cb ();
  }).catch(function(err) {
    const errorMessage = errorMessageFromSkulptError(err) || null;
    if (!errorMessage) {
      throw null;
    }
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
    // If there's more than one program being executed at a time, we ignore it.
    // This happens when a program requiring user input is suspended when the user changes the code.
    if (window.State.programsInExecution > 1) return;
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
    // We give the user time to give input.
    var storage = window.localStorage;
    var debug = storage.getItem("debugLine")
    if (storage.getItem("prompt-" + prompt) == null) {
    Sk.execStart = new Date(new Date().getTime() + 1000 * 60 * 60 * 24 * 365);
    $('#turtlecanvas').hide();
    return new Promise(function(ok) {
      window.State.disable_run = true;

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
        event.preventDefault();
        $('#inline-modal').hide();
        if (hasTurtle) {
          $('#turtlecanvas').show();
        }
        // We reset the timer to the present moment.
        Sk.execStart = new Date ();
        // We set a timeout for sending back the input, so that the input box is hidden before processing the program.
        // Since processing the program might take some time, this timeout increases the responsiveness of the UI after
        // replying to a query.
        setTimeout (function () {
           ok(input.val());
           if (debug != null) {
              storage.setItem("prompt-" + prompt, input.val()!.toString());
           }
           $ ('#output').focus ();
        }, 0);

          return false;
        });
        $('#inline-modal').show();
      });
    } else {
      return new Promise(function (ok) {
        ok(storage.getItem("prompt-" + prompt));

      });
    }
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
  pushAchievement("make_some_noise");
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
  // This variable avoids showing the generic native `onbeforeunload` prompt
  window.State.no_unload_prompt = true;
  if (! window.State.unsaved_changes) return cb ();
  modal.confirm(ErrorMessages['Unsaved_Changes'], cb);
}

export function load_quiz(level: string) {
  $('*[data-tabtarget="quiz"]').html ('<iframe id="quiz-iframe" class="w-full" title="Quiz" src="/quiz/start/' + level + '"></iframe>');
}

export function showVariableView() {
// When blue label button is clicked, the view will appear or hide
  const variables = $('#variables');
  if (variables.is(":hidden")) {
    variables.show();
    $("#variables").trigger("click")
  }
  else {
    variables.hide();
  }
}

//Feature flag for step by step debugger. Becomes true automatically for level 7 and below.
var step_debugger = false;
if(window.State.level != null){
  let level = Number(window.State.level);
  step_debugger = level <= 7;
}

//Hides the debug button if feature flag is false
if (!step_debugger) {
  $('#debug_button').hide();
}

export function show_variables() {
  const variableList = $('#variable-list');
  if (variableList.hasClass('hidden')) {
    variableList.removeClass('hidden');
  }
}

export function load_variables(variables: any){
    //@ts-ignore
    variables = clean_variables(variables);
    const variableList = $('#variable-list');
    variableList.empty();
    for (const i in variables) {
      variableList.append(`<li style=color:${variables[i][2]}>${variables[i][0]}: ${variables[i][1]}</li>`);
    }
}

// Color-coding string, numbers, booleans and lists
// This will be cool to use in the future!
// Just change the colors to use it
function special_style_for_variable(variable: any){
  let result = '';
  let parsedVariable = parseInt(variable.v);
  if (typeof parsedVariable == 'number' && !isNaN(parsedVariable)){
     result =  "#ffffff";
   }
   if(typeof variable.v == 'string' && isNaN(parsedVariable)){
     result = "#ffffff";
   }
   if(typeof variable.v == 'boolean'){
     result = "#ffffff";
   }
   if (variable.tp$name == 'list'){
    result =  "#ffffff";
   }
   return result;
}

//hiding certain variables from the list unwanted for users
// @ts-ignore
function clean_variables(variables: any) {
  const new_variables = [];
  const unwanted_variables = ["random", "time", "int_saver","int_$rw$", "turtle", "t"];
  for (const variable in variables) {
    if (!variable.includes('__') && !unwanted_variables.includes(variable)) {
    let extraStyle = special_style_for_variable(variables[variable]);
    let newTuple = [variable, variables[variable].v, extraStyle];
    new_variables.push(newTuple);
    }
  }
  return new_variables;
}

export function get_trimmed_code() {
  try {
    // This module may or may not exist, so let's be extra careful here.
    const whitespace = ace.require("ace/ext/whitespace");
    whitespace.trimTrailingSpace(theGlobalEditor.session, true);
  } catch (e) {
    console.error(e);
  }
  // FH Feb: the above code turns out not to remove spaces from lines that contain only whitespace,
  // but that upsets the parser so this removes those spaces also:
  // Remove whitespace at the end of every line

  // ignore the lines with a breakpoint in it.
  let breakpoints = editor.session.getBreakpoints();
  let code = theGlobalEditor.getValue();
  var storage = window.localStorage;
  var debugLines = storage.getItem('debugLine');
  if (code) {
    let lines = code.split('\n');
    if(debugLines != null){
      lines = lines.slice(0, parseInt(debugLines) + 1);
    }
    for (let i = 0; i < lines.length; i++) {
      if (breakpoints[i] == 'ace_breakpoint') {
        lines[i] = '';
      }
      code = lines.join('\n');
    }
  }

  // regex for any number of whitespace \s*
  // g: global (replace all matches, not just the first one)
  return code.replace(/\s*$/gm, '');
}

export function confetti_cannon(){
  const canvas = document.getElementById('confetti');
  if (canvas) {
    canvas.classList.remove('hidden');
    // ignore this error, the function comes from CDN for now
    const jsConfetti = new JSConfetti({canvas})
    // timeout for the confetti to fall down
    setTimeout(function(){canvas.classList.add('hidden')}, 3000);
    let adventures = $('#adventures');
    let currentAdventure = $(adventures).find('.tab-selected').attr('data-tab');
    let customLevels = ['turtle', 'rock', 'haunted', 'restaurant', 'fortune', 'songs', 'dice']

    if(customLevels.includes(currentAdventure!)){
      let currentAdventureConfetti = getConfettiForAdventure(currentAdventure?? '');

      // @ts-ignore
      jsConfetti.addConfetti({
        emojis: currentAdventureConfetti,
        emojiSize: 45,
        confettiNumber: 100,
      });
    }

    else{
      jsConfetti.addConfetti();
    }

    const confettiButton = document.getElementById('confetti-button');
    if (confettiButton) {
      confettiButton.classList.add('hidden');
    }
  }
}

function getConfettiForAdventure(adventure: string){
  let emoji = Array.from(ErrorMessages[adventure])
  if (emoji != null){
    return emoji;
  }
  return [['🌈'], ['⚡️'], ['💥'], ['✨'], ['💫']];
}

export function ScrollOutputToBottom(){
$("#output").animate({ scrollTop: $(document).height() }, "slow");
  return false;
}

export function modalStepOne(level: number){
  createModal(level);
  let modal_editor = $('#modal-editor');
  initializeModalEditor(modal_editor);
}

function showSuccesMessage(){
  removeBulb();
  var allsuccessmessages = ErrorMessages['Transpile_success'];
  var randomnum: number = Math.floor(Math.random() * allsuccessmessages.length);
  success.show(allsuccessmessages[randomnum]);
}
function createModal(level:number ){
  let editor = "<div id='modal-editor' data-lskey=\"level_{level}__code\" class=\"w-full flex-1 text-lg rounded\" style='height:200px; width:50vw;'></div>".replace("{level}", level.toString());
  let title = ErrorMessages['Program_repair'];
  modal.repair(editor, 0, title);
}
export function turnIntoAceEditor(element: HTMLElement, isReadOnly: boolean): AceAjax.Editor {
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
      if (window.State.level) {
        const mode = getHighlighter(window.State.level);
        editor.session.setMode(mode);
      }
    }
    return editor;
  }

  function initializeModalEditor($editor: JQuery) {
    if (!$editor.length) return;
    // We expose the editor globally so it's available to other functions for resizing
    let editor = turnIntoAceEditor($editor.get(0)!, true);
    theModalEditor = editor;
    error.setEditor(editor);
    //small timeout to make sure the call with fixed code is complete.
    setTimeout(function(){}, 2000);

    window.Range = ace.require('ace/range').Range // get reference to ace/range

    // Load existing code from session, if it exists
    const storage = window.sessionStorage;
    if (storage) {
      const levelKey = $editor.data('lskey');
        let tempIndex = 0;
        let resultString = "";

        if(storage.getItem('fixed_{lvl}'.replace("{lvl}", levelKey))){
          resultString = storage.getItem('fixed_{lvl}'.replace("{lvl}", levelKey))?? "";
          let tempString = ""
          for (let i = 0; i < resultString.length + 1; i++) {
            setTimeout(function() {
              editor.setValue(tempString,tempIndex);
              tempString += resultString[tempIndex];
              tempIndex++;
            }, 150 * i);
          }
        }
        else{
          resultString = storage.getItem('warning_{lvl}'.replace("{lvl}", levelKey))?? "";
          editor.setValue(resultString);
        }
    }

    window.onbeforeunload = () => {
      // The browser doesn't show this message, rather it shows a default message.
      if (window.State.unsaved_changes && !window.State.no_unload_prompt) {
        return ErrorMessages['Unsaved_Changes'];
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
        runit (window.State.level, window.State.lang, "", function () {
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
export function toggle_developers_mode(enforced: boolean) {
  if ($('#developers_toggle').is(":checked") || enforced) {
      $('#adventures-tab').hide();
      pushAchievement("lets_focus");
  } else {
      $('#adventures-tab').show();
  }

  if ($('#adventures-tab').is(":hidden")) {
    $('#editor-area').removeClass('mt-5');
    $('#code_editor').css('height', 36 + "em");
    $('#code_output').css('height', 36 + "em");
    theGlobalEditor.resize();
  } else {
    $('#editor-area').addClass('mt-5');
    $('#code_editor').height('22rem');
    $('#code_output').height('22rem');
  }
}

export function load_profile(username: string, mail: string, birth_year: number, gender: string, country: string) {
  $('#profile').toggle();
  if ($('#profile').is(":visible")) {
      $('#username').html(username);
      $('#email').val(mail);
      $('#birth_year').val(birth_year);
      $('#gender').val(gender);
      $('#country').val(country);
  }
}

export function change_language(lang: string) {
  $.ajax({
    type: 'POST',
    url: '/change_language',
    data: JSON.stringify({
      lang: lang
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function(response: any) {
      if (response.succes){
        location.reload();
      }
    }).fail(function(xhr) {
      console.error(xhr);
    });
}

export function change_keyword_language(start_lang: string, new_lang: string) {
  $.ajax({
    type: 'POST',
    url: '/translate_keywords',
    data: JSON.stringify({
      code: ace.edit('editor').getValue(),
      start_lang: start_lang,
      goal_lang: new_lang,
      level: window.State.level
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function (response: any) {
    if (response.success) {
      ace.edit('editor').setValue(response.code);
      $('#editor').attr('lang', new_lang);
      update_view('main_editor_keyword_selector', new_lang);
    }
  }).fail(function (err) {
      modal.alert(err.responseText, 3000, true);
  });
}

function update_view(selector_container: string, new_lang: string) {
  $('#' + selector_container + ' > div').map(function() {
    if ($(this).attr('lang') == new_lang) {
      $(this).show();
    } else {
      $(this).hide();
    }
  });
}

export function select_profile_image(image: number) {
  $('.profile_image').removeClass("border-2 border-blue-600");
  $('#profile_image_' + image).addClass("border-2 border-blue-600");
  $('#profile_picture').val(image);
}

export function filter_programs() {
  const level = $('#explore_page_level').val();
  const adventure = $('#explore_page_adventure').val();
  window.open('?level=' + level + "&adventure=" + adventure, "_self");
}

export function filter_user_programs(username: string, own_request?: boolean) {
  const level = $('#user_program_page_level').val();
  const adventure = $('#user_program_page_adventure').val();
  if (own_request) {
    window.open('?level=' + level + "&adventure=" + adventure, "_self");
  } else {
    window.open('?user=' + username + '&level=' + level + "&adventure=" + adventure, "_self");
  }
}

export function filter_admin() {
  const filter = $('#admin_filter_category').val();
  if (filter == "email") {
    const substring = $('#email_filter_input').val();
    window.open('?filter=' + filter + "&substring=" + substring, "_self");
  } else if (filter == "language") {
    const lang = $('#language_filter_input').val();
    window.open('?filter=' + filter + "&language=" + lang, "_self");
  } else if (filter == "keyword_language") {
    const keyword_lang = $('#keyword_language_filter_input').val();
    window.open('?filter=' + filter + "&keyword_language=" + keyword_lang, "_self");
  } else {
    const start_date = $('#admin_start_date').val();
    const end_date = $('#admin_end_date').val();
    window.open('?filter=' + filter + "&start=" + start_date + "&end=" + end_date, "_self");
  }
}

if ($("#editor").length) {
  var editor = ace.edit("editor");
  editor.on("guttermousedown", function (e: any) {
    var editorContainer = document.getElementById("editor");
    var textContainer = editorContainer?.getElementsByClassName("ace_text-layer")[0];
    var lines = textContainer?.getElementsByClassName("ace_line");
    var target = e.domEvent.target;

    if (lines) {
      if (target.className.indexOf("ace_gutter-cell") == -1)
        return;

      if (e.clientX > 25 + target.getBoundingClientRect().left)
        return;

      var breakpoints = e.editor.session.getBreakpoints(row, 0);
      var row = e.getDocumentPosition().row;
      if (typeof breakpoints[row] === typeof undefined && row != e.editor.getLastVisibleRow() + 1) {
        e.editor.session.setBreakpoint(row);
        row = getCorrectVisibleRow(row, e.editor);
        lines[row].innerHTML = addDisabledClass(lines[row]);
        e.stop();
      } else {
        e.editor.session.clearBreakpoint(row);
        // calculating the correct line to edit
        row = getCorrectVisibleRow(row, e.editor);
        lines[row].innerHTML = removeDisabledClass(lines[row]);
        e.stop();
      }
    }
  });

  editor.renderer.on("afterRender", function () {
    var breakpoints = editor.session.getBreakpoints();
    adjustLines(breakpoints);
    setDebugLine()
  });
}

function getCorrectVisibleRow(row: number, editor: any) {
  var firstVisibleRow = editor.getFirstVisibleRow();
  return row - firstVisibleRow;
}

function adjustLines(disabledRow: []) {
  // We have to specify the correct editor here
  var editorContainer = document.getElementById("editor");
  var textContainer = editorContainer?.getElementsByClassName("ace_text-layer")[0];
  var lines = textContainer?.getElementsByClassName("ace_line");
  var firstVisibleRow = editor.getFirstVisibleRow();
  var lastVisibleRow = editor.getLastVisibleRow();

  if (lines) {
    var arr = disabledRow.slice(firstVisibleRow, lastVisibleRow + 1);

    for (var i = 0; i < arr.length; i++) {
      if (arr[i] == 'ace_breakpoint') {
        var currentLine = lines[i];
        currentLine.innerHTML = addDisabledClass(currentLine);
      } else {
        var currentLine = lines[i];
        currentLine.innerHTML = removeDisabledClass(currentLine);
      }
    }
  }
}

function debugRun() {
  if (window.State.level != null && window.State.lang != null) {
    runit(window.State.level, window.State.lang, "", function () {
      $('#output').focus();
    });
  }
}

export function startDebug() {
  if (step_debugger === true) {
    var debugButton = $("#debug_button");
    debugButton.hide();
    var continueButton = $("#debug_continue");
    var stopButton = $("#debug_stop");
    var resetButton = $("#debug_restart");
    var runButtonContainer = $("#runButtonContainer");

    runButtonContainer.hide();
    continueButton.show();
    stopButton.show();
    resetButton.show();

    incrementDebugLine();
    debugRun();
  }
}

export function resetDebug() {
  if (step_debugger === true) {
    var storage = window.localStorage;
    var debugLine = storage.getItem("debugLine");
    var continueButton = $("#debug_continue");
    continueButton.show();

    if (debugLine == null) {
      storage.setItem("debugLine", "0");
      clearDebugVariables();
      setDebugLine(true);
      debugRun();
      return;
    } else {
      storage.setItem("debugLine", "0");
      clearDebugVariables();
      setDebugLine(true);
      debugRun();
    }
  }
}

export function stopDebug() {
  if (step_debugger === true) {
    var debugButton = $("#debug_button");
    debugButton.show();
    var continueButton = $("#debug_continue");
    var stopButton = $("#debug_stop");
    var resetButton = $("#debug_restart");
    var runButtonContainer = $("#runButtonContainer");

    runButtonContainer.show();
    continueButton.hide();
    stopButton.hide();
    resetButton.hide();

    var storage = window.localStorage;
    var debugLine = storage.getItem("debugLine");

    clearDebugVariables();

    if (debugLine == null) {
      setDebugLine(true);
      return;
    } else {
      storage.removeItem("debugLine");
      setDebugLine(true);
    }
  }
}

function clearDebugVariables() {
  var storage = window.localStorage;
  var keysToRemove = {...localStorage};

  for (var key in keysToRemove) {
    if (key.includes("prompt-")) {
      storage.removeItem(key);
    }
  }
}

export function incrementDebugLine() {
  var storage = window.localStorage;
  var debugLine = storage.getItem("debugLine");
  if (debugLine == null) {
    storage.setItem("debugLine", "0");
    setDebugLine();
    return;
  } else {
    var debugLineInt = parseInt(debugLine);
    debugLineInt++;
    storage.setItem("debugLine", debugLineInt.toString());
  }
  setDebugLine();

  var lengthOfEntireEditor = theGlobalEditor.getValue().split("\n").filter(e => e).length;
  var debugLine = storage.getItem("debugLine");
  if (debugLine != null) {
    var currentLine = parseInt(debugLine);
    if (currentLine <= lengthOfEntireEditor) {
      debugRun();
    }
  }
}

function setDebugLine(reset: Boolean = false) {
  if (step_debugger === true) {
    var storage = window.localStorage;

    var editorContainer = document.getElementById("editor");
    var textContainer = editorContainer?.getElementsByClassName("ace_text-layer")[0];
    var lines = textContainer?.getElementsByClassName("ace_line");
    var firstVisibleRow = editor.getFirstVisibleRow();
    var lastVisibleRow = editor.getLastVisibleRow();
    var lengthOfEntireEditor = theGlobalEditor.getValue().split("\n").filter(e => e).length;
    var indexArray = []
    for (var x = firstVisibleRow; x <= lastVisibleRow; x++) {
      indexArray.push(x);
    }

    if (lines) {
      var debugLine = storage.getItem("debugLine");
      if (debugLine != null) {
        var debugLineNumber = parseInt(debugLine);
        for (var i = 0; i < indexArray.length; i++) {
          if (indexArray[i] == debugLineNumber) {
            lines[i].innerHTML = addDebugClass(lines[i]);
          } else {
            lines[i].innerHTML = removeDebugClass(lines[i]);
          }
          if (debugLineNumber == lengthOfEntireEditor) {
            stopDebug();
            var continueButton = $("#debug_continue");
            continueButton.hide();
            return;
          }
        }
      }
      if (reset) {
        for (var i = 0; i < indexArray.length; i++) {
          lines[i].innerHTML = removeDebugClass(lines[i]);
        }
        //force resetting the rendering of the ace editor to remove the highlighted line
        editor.resize(true);
      }
    }
  }
}

function addDisabledClass(str: Element) {
  if (!str.children[0]?.innerHTML?.includes("ace-disabled")) {
    return '<div class="ace-disabled">' + str.innerHTML + '</div>';
  }
  return str.innerHTML;
}

function removeDisabledClass(str: Element) {
  return str.innerHTML.replace('<div class="ace-disabled">', '').replace('</div>', '');
}

function addDebugClass(str: Element) {
  if (!str.children[0]?.innerHTML?.includes("debugLine")) {
    return '<div class="debugLine">' + str.innerHTML + '</div>';
  }
  return str.innerHTML;
}

function removeDebugClass(str: Element) {
  return str.innerHTML.replace('<div class="debugLine">', '').replace('</div>', '');
}


