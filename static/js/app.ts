// It's important that this file gets loaded first
import './syntaxModesRules';

import { modal, error, success } from './modal';
import { Markers } from './markers';

export let theGlobalEditor: AceAjax.Editor;
export let theModalEditor: AceAjax.Editor;
let markers: Markers;

let last_code: string;

const turtle_prefix =
`# coding=utf8
import random, time, turtle
t = turtle.Turtle()
t.shape("turtle")
t.hideturtle()
t.penup()
t.left(90)
t.pendown()
t.speed(3)
t.showturtle()
`;

const pygame_prefix =
`# coding=utf8
import pygame
import buttons
pygame.init()
canvas = pygame.display.set_mode((711,300))
canvas.fill(pygame.Color(247, 250, 252, 255))
pygame_end = False

button_list = []
def create_button(name):
  if name not in button_list:
    button_list.append(name)
    buttons.add(name)

`;

const pygame_suffix =
`# coding=utf8
pygame_end = True
pygame.quit()
`;

const normal_prefix =
`# coding=utf8
import random, time
global int_saver
global convert_numerals # needed for recursion to work
int_saver = int
def int(s):
  if isinstance(s, str):
    numerals_dict = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '𑁦': '0', '𑁧': '1', '𑁨': '2', '𑁩': '3', '𑁪': '4', '𑁫': '5', '𑁬': '6', '𑁭': '7', '𑁮': '8', '𑁯': '9', '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4', '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9', '੦': '0', '੧': '1', '੨': '2', '੩': '3', '੪': '4', '੫': '5', '੬': '6', '੭': '7', '੮': '8', '੯': '9', '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9', '೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9', '୦': '0', '୧': '1', '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8', '୯': '9', '൦': '0', '൧': '1', '൨': '2', '൩': '3', '൪': '4', '൫': '5', '൬': '6', '൭': '7', '൮': '8', '൯': '9', '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9', '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9', '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4', '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9', '༠': '0', '༡': '1', '༢': '2', '༣': '3', '༤': '4', '༥': '5', '༦': '6', '༧': '7', '༨': '8', '༩': '9', '᠐': '0', '᠑': '1', '᠒': '2', '᠓': '3', '᠔': '4', '᠕': '5', '᠖': '6', '᠗': '7', '᠘': '8', '᠙': '9', '០': '0', '១': '1', '២': '2', '៣': '3', '៤': '4', '៥': '5', '៦': '6', '៧': '7', '៨': '8', '៩': '9', '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9', '໐': '0', '໑': '1', '໒': '2', '໓': '3', '໔': '4', '໕': '5', '໖': '6', '໗': '7', '໘': '8', '໙': '9', '꧐': '0', '꧑': '1', '꧒': '2', '꧓': '3', '꧔': '4', '꧕': '5', '꧖': '6', '꧗': '7', '꧘': '8', '꧙': '9', '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9', '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0'}
    latin_numerals = ''.join([numerals_dict.get(letter, letter) for letter in s])
    return int_saver(latin_numerals)
  return(int_saver(s))

def convert_numerals(alphabet, number):
  numerals_dict_return = {
    'Latin': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'Brahmi': ['𑁦', '𑁧', '𑁨', '𑁩', '𑁪', '𑁫', '𑁬', '𑁭', '𑁮', '𑁯'],
    'Devanagari': ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
    'Gujarati': ['૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯'],
    'Gurmukhi': ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯'],
    'Bengali': ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'],
    'Kannada': ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'],
    'Odia': ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯'],
    'Malayalam': ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯'],
    'Tamil': ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯'],
    'Telugu':['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'],
    'Burmese':['၀', '၁', '၂', '၃', '၄', '၅', '၆', '၇', '၈', '၉'],
    'Tibetan':['༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩'],
    'Mongolian':['᠐', '᠑', '᠒', '᠓', '᠔', '᠕', '᠖', '᠗', '᠘', '᠙'],
    'Khmer':['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩'],
    'Thai':['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙'],
    'Lao':['໐', '໑', '໒', '໓', '໔', '໕', '໖', '໗', '໘', '໙'],
    'Javanese':['꧐', '꧑', '꧒', '꧓', '꧔', '꧕', '꧖', '꧗', '꧘', '꧙'],
    'Arabic':['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'],
    'Persian':['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'],
    'Urdu': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']}

  numerals_list = numerals_dict_return[alphabet]
  number=str(number)

  number = str(number)
  if number.isnumeric():
    numerals_list = numerals_dict_return[alphabet]
    all_numerals_converted = [numerals_list[int(digit)] for digit in number]
    return ''.join(all_numerals_converted)
  else:
    return number
`;

// Close the dropdown menu if the user clicks outside of it
$(document).on("click", function(event){
    if(!$(event.target).closest(".dropdown").length){
        $(".dropdown-menu").slideUp("medium");
        $(".cheatsheet-menu").slideUp("medium");
    }
});

(function() {
  // A bunch of code expects a global "State" object. Set it here if not
  // set yet.
  if (!window.State) {
    window.State = {};
  }

  // Set const value to determine the current page direction -> useful for ace editor settings
  const dir = $("body").attr("dir");

  // *** EDITOR SETUP ***
  initializeMainEditor($('#editor'));

  // Any code blocks we find inside 'turn-pre-into-ace' get turned into
  // read-only editors (for syntax highlighting)
  for (const preview of $('.turn-pre-into-ace pre').get()) {
    $(preview).addClass('text-lg rounded');
    // We set the language of the editor to the current keyword_language -> needed when copying to main editor
    $(preview).attr('lang', <string>window.State.keyword_language);
    $(preview).addClass('overflow-x-hidden');
    const exampleEditor = turnIntoAceEditor(preview, true);

    // Fits to content size
    exampleEditor.setOptions({ maxLines: Infinity });
    if ($(preview).hasClass('common-mistakes')) {
      exampleEditor.setOptions({ minLines: 5 });
    } else if ($(preview).hasClass('cheatsheet')) {
      exampleEditor.setOptions({ minLines: 1 });
    } else if ($(preview).hasClass('parsons')) {
      exampleEditor.setOptions({
        minLines: 1,
        showGutter: false,
        showPrintMargin: false,
        highlightActiveLine: false
      });
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
        stopit();
        clearOutput();
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
    theGlobalEditor.setShowPrintMargin(false);
    theGlobalEditor.renderer.setScrollMargin(0, 0, 0, 20)
    error.setEditor(editor);
    markers = new Markers(theGlobalEditor);

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
        if (window.State.disable_run) {
          stopit();
          editor.focus(); // Make sure the editor has focus, so we can continue typing
        }
        if ($('#ask-modal').is (':visible')) $('#inline-modal').hide();
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
      // Remove the cursor
      editor.renderer.$cursorLayer.element.style.display = "none";
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

function clearErrors(editor: AceAjax.Editor) {
  // Not sure if we use annotations everywhere, but this was
  // here already.
  editor.session.clearAnnotations();
  markers.clearErrors();
}

export function stopit() {
  if (window.State.pygame_running) {
      // when running pygame, raise the pygame quit event
      Sk.insertPyGameEvent("quit");
      Sk.unbindPygameListeners();

      window.State.pygame_running = false;
      document.onkeydown = null;
      $('#pygame-modal').hide();
      $('#stopit').hide();
      $('#runit').show();
  }
  else
  {
      // We bucket-fix stop the current program by setting the run limit to 1ms
      Sk.execLimit = 1;
      clearTimeouts();
      $('#stopit').hide();
      $('#runit').show();

      // This gets a bit complex: if we do have some input modal waiting, fake submit it and hide it
      // This way the Promise is no longer "waiting" and can no longer mess with our next program
      if ($('#ask-modal').is(":visible")) {
        $('#ask-modal form').submit();
        $('#ask-modal').hide();
      }
  }

  window.State.disable_run = false;
}

function clearOutput() {
  const outputDiv = $('#output');
  //Saving the variable button because sk will overwrite the output div
  const variableButton = outputDiv.find('#variable_button');
  const variables = outputDiv.find('#variables');
  outputDiv.empty();

  outputDiv.addClass("overflow-auto");
  outputDiv.append(variableButton);
  outputDiv.append(variables);
  error.hide();
  success.hide();

  // Clear the user created buttons.
  const buttonsDiv = $('#dynamic-buttons');
  buttonsDiv.empty();
  buttonsDiv.hide();
}

export function runit(level: string, lang: string, disabled_prompt: string, cb: () => void) {
  if (window.State.disable_run) {
    // If there is no message -> don't show a prompt
    if (disabled_prompt) {
      return modal.alert(disabled_prompt, 3000, true);
    } return;
  }

  // Make sure to stop previous PyGame event listeners
  if (typeof Sk.unbindPygameListeners === 'function') {
    Sk.unbindPygameListeners();
  }

  // We set the run limit to 1ms -> make sure that the previous programs stops (if there is any)
  Sk.execLimit = 1;
  $('#runit').hide();
  $('#stopit').show();
  $('#saveFiles').hide();
  clearOutput();

  try {
    level = level.toString();
    var editor = theGlobalEditor;
    var code = "";
    if ($('#parsons_container').is(":visible")) {
      window.State.unsaved_changes = false; // We don't want to throw this pop-up
      code = get_parsons_code();
      // We return no code if all lines are empty or there is a mistake -> clear errors and do nothing
      if (!code) {
        clearErrors(editor);
        stopit();
        return;
      } else {
        // Add the onclick on the button -> only show if there is another exercise to load (set with an onclick)
        if ($('#next_parson_button').attr('onclick')) {
          $('#next_parson_button').show();
        }
      }
    } else {
      code = get_active_and_trimmed_code();
      if (code.length == 0) {
        clearErrors(editor);
        stopit();
        return;
      }
    }

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
        tutorial: $('#code_output').hasClass("z-40"), // if so -> tutorial mode
        read_aloud : !!$('#speak_dropdown').val(),
        adventure_name: window.State.adventure_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response: any) {
      console.log('Response', response);
      if (response.Warning && $('#editor').is(":visible")) {
        //storeFixedCode(response, level);
        error.showWarning(ErrorMessages['Transpile_warning'], response.Warning);
      }
      if (response.achievements) {
        showAchievements(response.achievements, false, "");
      }
      if (response.Error) {
        error.show(ErrorMessages['Transpile_error'], response.Error);
        if (response.Location && response.Location[0] != "?") {
          //storeFixedCode(response, level);
          // Location can be either [row, col] or just [row].
          markers.highlightAceError(response.Location[0], response.Location[1]);
        }
        $('#stopit').hide();
        $('#runit').show();
        return;
      }
      runPythonProgram(response.Code, response.has_turtle, response.has_pygame, response.has_sleep, response.Warning, cb).catch(function(err) {
        // The err is null if we don't understand it -> don't show anything
        if (err != null) {
          error.show(ErrorMessages['Execute_error'], err.message);
          reportClientError(level, code, err.message);
        }
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
    modal.alert(e.responseText, 3000, true);
  }
}

export function saveMachineFiles() {
  $.ajax({
    type: 'POST',
    url: '/generate_machine_files',
    data: JSON.stringify({
      level: window.State.level,
      code: get_active_and_trimmed_code(),
      lang: window.State.lang,
    }),
    contentType: 'application/json',
    dataType: 'json'
    }).done(function(response: any) {
      if (response.filename) {
        // Download the file
        window.location.replace('/download_machine_files/' + response.filename);
      }
  });
}

// function storeFixedCode(response: any, level: string) {
//   if (response.FixedCode) {
//     sessionStorage.setItem ("fixed_level_{lvl}__code".replace("{lvl}", level), response.FixedCode);
//     showBulb(level);
//   }
// }

// function showBulb(level: string){
//   const parsedlevel = parseInt(level)
//   if(parsedlevel <= 2){
//     const repair_button = $('#repair_button');
//     repair_button.show();
//     repair_button.attr('onclick', 'hedyApp.modalStepOne(' + parsedlevel + ');event.preventDefault();');
//   }
//}


// We've observed that this code may gets invoked 100s of times in quick succession. Don't
// ever push the same achievement more than once per page load to avoid this.
const ACHIEVEMENTS_PUSHED: Record<string, boolean> = {};

export function pushAchievement(achievement: string) {
  if (ACHIEVEMENTS_PUSHED[achievement]) {
      console.error('Achievement already pushed, this may be a programming issue: ', achievement);
      return;
  }
  ACHIEVEMENTS_PUSHED[achievement] = true;

  $.ajax({
    type: 'POST',
    url: '/achievements/push-achievement',
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

export function closeAchievement() {
  $('#achievement_pop-up').hide();
  if ($('#achievement_pop-up').attr('reload')) {
    $('#achievement_pop-up').removeAttr('reload');
    $('#achievement_pop-up').removeAttr('redirect');
    return location.reload();
  }
  if ($('#achievement_pop-up').attr('redirect')) {
    const redirect = <string>$('#achievement_pop-up').attr('redirect');
    $('#achievement_pop-up').removeAttr('reload');
    $('#achievement_pop-up').removeAttr('redirect');
    return window.location.pathname = redirect;
  }
  // If for some reason both situation don't happen we still want to make sure the attributes are removed
  $('#achievement_pop-up').removeAttr('reload');
  $('#achievement_pop-up').removeAttr('redirect');
}

export function showAchievements(achievements: any[], reload: boolean, redirect: string) {
  fnAsync(achievements, 0);
  if (reload) {
    $('#achievement_pop-up').attr('reload', 'true');
    setTimeout(function(){
      $('#achievement_pop-up').removeAttr('reload');
      $('#achievement_pop-up').removeAttr('redirect');
      location.reload();
     }, achievements.length * 6000);
  }
  if (redirect) {
    $('#achievement_pop-up').attr('redirect', redirect);
    setTimeout(function(){
      $('#achievement_pop-up').removeAttr('reload');
      $('#achievement_pop-up').removeAttr('redirect');
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
        $('#achievement_reached_statics').text(achievement[2]);
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
      $('#modal-copy-button').attr('onclick', "hedyApp.copy_to_clipboard('" + viewProgramLink(response.id) + "', '" + response.share_message + "')");
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
      modal.alert (response.message, 3000, false);
      if (Public) {
        change_shared(true, index);
      } else {
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

export function set_explore_favourite(id: string, favourite: number) {
  let prompt = "Are you sure you want to remove this program as a \"Hedy\'s choice\" program?";
  if (favourite) {
    prompt = "Are you sure you want to set this program as a \"Hedy\'s choice\" program?";
  }
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'POST',
      url: '/programs/set_hedy_choice',
      data: JSON.stringify({
        id: id,
        favourite: favourite
    }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
        modal.alert(response.message, 3000, false);
        if (favourite == 1) {
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

export function report_program(prompt: string, id: string) {
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'POST',
      url: '/programs/report',
      data: JSON.stringify({
        id: id,
    }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
        modal.alert(response.message, 3000, false);
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

  // Hide all modals to make sure the copy clipboard modal is hidden as well -> show alert() with feedback
  modal.hide();
  modal.alert(prompt, 3000, false);
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

export function runPythonProgram(this: any, code: string, hasTurtle: boolean, hasPygame: boolean, hasSleep: boolean, hasWarnings: boolean, cb: () => void) {
  // If we are in the Parsons problem -> use a different output
  let outputDiv = $('#output');

  //Saving the variable button because sk will overwrite the output div
  const variableButton = outputDiv.find('#variable_button');
  const variables = outputDiv.find('#variables');
  outputDiv.empty();
  outputDiv.append(variableButton);
  outputDiv.append(variables);

  const storage = window.localStorage;
  let skulptExternalLibraries:{[index: string]:any} = {};
  let debug = storage.getItem("debugLine");

  Sk.pre = "output";
  const turtleConfig = (Sk.TurtleGraphics || (Sk.TurtleGraphics = {}));
  turtleConfig.target = 'turtlecanvas';
  // If the adventures are not shown  -> increase height of turtleConfig
  if ($('#adventures-tab').is(":hidden")) {
      turtleConfig.height = 600;
      turtleConfig.worldHeight = 600;
  } else {
      turtleConfig.height = 300;
      turtleConfig.worldHeight = 300;
  }
  // Always set the width to output panel width -> match the UI
  turtleConfig.width = outputDiv.width();
  turtleConfig.worldWidth = outputDiv.width();

  let code_prefix = normal_prefix;

  if (!hasTurtle && !hasPygame) {
    // There might still be a visible turtle panel. If the new program does not use the Turtle,
    // remove it (by clearing the '#turtlecanvas' div)
    $('#turtlecanvas').empty();
  }

  if (hasTurtle) {
    code_prefix += turtle_prefix;
    $('#turtlecanvas').show();
  }

  if (hasPygame){
    skulptExternalLibraries = {
      './pygame.js': {
        path: "/vendor/pygame_4_skulpt/init.js",
      },
      './display.js': {
        path: "/vendor/pygame_4_skulpt/display.js",
      },
      './draw.js': {
        path: "/vendor/pygame_4_skulpt/draw.js",
      },
      './event.js': {
        path: "/vendor/pygame_4_skulpt/event.js",
      },
      './font.js': {
        path: "/vendor/pygame_4_skulpt/font.js",
      },
      './image.js': {
        path: "/vendor/pygame_4_skulpt/image.js",
      },
      './key.js': {
        path: "/vendor/pygame_4_skulpt/key.js",
      },
      './mouse.js': {
        path: "/vendor/pygame_4_skulpt/mouse.js",
      },
      './transform.js': {
        path: "/vendor/pygame_4_skulpt/transform.js",
      },
      './locals.js': {
        path: "/vendor/pygame_4_skulpt/locals.js",
      },
      './time.js': {
        path: "/vendor/pygame_4_skulpt/time.js",
      },
      './version.js': {
        path: "/vendor/pygame_4_skulpt/version.js",
      },
      './buttons.js': {
          path: "/js/buttons.js",
      },
    };

    code_prefix += pygame_prefix;

    initSkulpt4Pygame();
    initCanvas4PyGame();

    const codeContainsInputFunctionBeforePygame = new RegExp(
      "input\\([\\s\\S]*\\)[\\s\\S]*while not pygame_end", 'gm'
    ).test(code);

    if (!hasTurtle && !codeContainsInputFunctionBeforePygame) {
      $('#pygame-modal').show();
    }

    document.onkeydown = animateKeys;
    window.State.pygame_running = true;
  }

  code = code_prefix + code;
  if (hasPygame) code += pygame_suffix;

  Sk.configure({
    output: outf,
    read: builtinRead,
    inputfun: inputFromInlineModal,
    inputfunTakesPrompt: true,
    setTimeout: timeout,
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
      if (hasTurtle || hasPygame) {
        // We don't want a timeout when using the turtle or pygame -> just set one for 10 minutes
        return (6000000);
      }
      if (level < 7) {
        // Also on a level < 7 (as we don't support loops yet), a timeout is redundant -> just set one for 5 minutes
        return (3000000);
      }
      // Set a time-out of either 20 seconds when having a sleep and 5 seconds when not
      return ((hasSleep) ? 20000 : 5000);
    }) ()
  });

  return Sk.misceval.asyncToPromise(() =>
    Sk.importMainWithBody("<stdin>", false, code, true), {
      "*": () => {
        // We don't do anything here...
      }
    }
   ).then(function(_mod) {
    console.log('Program executed');
    const pythonVariables = Sk.globals;
    load_variables(pythonVariables);
    $('#stopit').hide();
    $('#runit').show();

    if (hasPygame) {
      document.onkeydown = null;
      $('#pygame-modal').hide();
    }

    if (hasTurtle) {
      $('#saveFiles').show();
    }

    // Check if the program was correct but the output window is empty: Return a warning
    if ($('#output').is(':empty') && $('#turtlecanvas').is(':empty')) {
      if(!debug){
        pushAchievement("error_or_empty");
        error.showWarning(ErrorMessages['Transpile_warning'], ErrorMessages['Empty_output']);
      }
      return;
    }
    if (!hasWarnings && code !== last_code && !debug) {
        showSuccesMessage();
        last_code = code;
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
    addToOutput(text, 'white');
    speak(text)
  }

  function builtinRead(x: string) {
    if (x in skulptExternalLibraries) {
      const tmpPath = skulptExternalLibraries[x]["path"];
      if (x === "./pygame.js") {
        return Sk.misceval.promiseToSuspension(
          fetch(tmpPath)
              .then(r => r.text()))

      } else {
        let request = new XMLHttpRequest();
        request.open("GET", tmpPath, false);
        request.send();

        if (request.status !== 200) {
          return void 0
        }

        return request.responseText
      }
    }

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

    if (window.State.pygame_running) {
      Sk.unbindPygameListeners();
      document.onkeydown = null;
      $('#pygame-modal').hide();
    }

    return new Promise(function(ok) {
      window.State.disable_run = true;

      const input = $('#ask-modal input[type="text"]');
      $('#ask-modal .caption').text(prompt);
      input.val('');
      input.attr('placeholder', prompt);
      speak(prompt)

      setTimeout(function() {
        input.focus();
      }, 0);
      $('#ask-modal form').one('submit', function(event) {
        window.State.disable_run = false;
        event.preventDefault();
        $('#ask-modal').hide();

        if (hasTurtle) {
          $('#turtlecanvas').show();
        }

        if (window.State.pygame_running) {
          Sk.bindPygameListeners();
          document.onkeydown = animateKeys;

          if (!hasTurtle) {
            $('#pygame-modal').show();
          }
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
        $('#ask-modal').show();
      });
    } else {
      return new Promise(function (ok) {
        ok(storage.getItem("prompt-" + prompt));
      });
    }
  }
}

function resetTurtleTarget() {
    if (Sk.TurtleGraphics !== undefined) {

      let selector = Sk.TurtleGraphics.target;
      let target = typeof selector === "string" ? document.getElementById(selector) : selector;
      if (target !== null && target !== undefined){
        // clear canvas container
        while (target.firstChild) {
          target.removeChild(target.firstChild);
        }
        return target;
      }

    }

    return null;
}

function animateKeys(event: KeyboardEvent) {
    const keyColors = ['#cbd5e0', '#bee3f8', '#4299e1', '#ff617b', '#ae81ea', '#68d391'];
    const output = $("#output");

    if (output !== null) {
      let keyElement = $("<div></div>");
      output.append(keyElement);

      keyElement.text(event.key);
      keyElement.css('color', keyColors[Math.floor(Math.random() * keyColors.length)]);
      keyElement.addClass('animate-keys')

      setTimeout(function () {
        keyElement.remove()
      }, 1500);
    }
}

function initCanvas4PyGame() {
    let currentTarget = resetTurtleTarget();

    let div1 = document.createElement("div");

    if (currentTarget !== null) {
      currentTarget.appendChild(div1);
      $(div1).addClass("modal");
      $(div1).css("text-align", "center");
      $(div1).css("display", "none");

      let div2 = document.createElement("div");
      $(div2).addClass("modal-dialog modal-lg");
      $(div2).css("display", "inline-block");
      $(div2).width(self.width + 42);
      $(div2).attr("role", "document");
      div1.appendChild(div2);

      let div3 = document.createElement("div");
      $(div3).addClass("modal-content");
      div2.appendChild(div3);

      let div4 = document.createElement("div");
      $(div4).addClass("modal-header d-flex justify-content-between");
      let div5 = document.createElement("div");
      $(div5).addClass("modal-body");
      let div6 = document.createElement("div");
      $(div6).addClass("modal-footer");
      let div7 = document.createElement("div");
      $(div7).addClass("col-md-8");
      let div8 = document.createElement("div");
      $(div8).addClass("col-md-4");

      div3.appendChild(div4);
      div3.appendChild(div5);
      div3.appendChild(div6);

      $(Sk.main_canvas).css("border", "none");
      $(Sk.main_canvas).css("display", "none");
      div5.appendChild(Sk.main_canvas);
    }
}

function initSkulpt4Pygame() {
    Sk.main_canvas = document.createElement("canvas");
    Sk.configure({
        killableWhile: true,
        killableFor: true,
        __future__: Sk.python3,
    });
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

//Feature flag for variable and values view
var variable_view = false;

if(window.State.level != null){
  let level = Number(window.State.level);
  variable_view = level >= 2;
  hide_if_no_variables();
}

function hide_if_no_variables(){
  if($('#variables #variable-list li').length == 0){
    $('#variable_button').hide();
  }
  else{
    $('#variable_button').show();
  }
}

//Hides the HTML DIV for variables if feature flag is false
if (!variable_view) {
  $('#variables').hide();
  $('#variable_button').hide();
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
  if (variable_view === true) {
    const variableList = $('#variable-list');
    if (variableList.hasClass('hidden')) {
      variableList.removeClass('hidden');
    }
  }
}

export function load_variables(variables: any) {
  if (variable_view === true) {
    variables = clean_variables(variables);
    const variableList = $('#variable-list');
    variableList.empty();
    for (const i in variables) {
      // Only append if the variable contains any data (and is not undefined)
      if (variables[i][1]) {
        variableList.append(`<li style=color:${variables[i][2]}>${variables[i][0]}: ${variables[i][1]}</li>`);
      }
    }
    hide_if_no_variables();
  }
}

// Color-coding string, numbers, booleans and lists
// This will be cool to use in the future!
// Just change the colors to use it
function special_style_for_variable(variable: Variable) {
  let result = '';
  let parsedVariable = parseInt(variable.v as string);
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
function clean_variables(variables: Record<string, Variable>) {
  const new_variables = [];
  const unwanted_variables = ["random", "time", "int_saver", "int_$rw$", "turtle", "t"];
  for (const variable in variables) {
    if (!variable.includes('__') && !unwanted_variables.includes(variable)) {
      let extraStyle = special_style_for_variable(variables[variable]);
      let name = unfixReserved(variable);
      let newTuple = [name, variables[variable].v, extraStyle];
      new_variables.push(newTuple);
    }
  }
  return new_variables;
}

function unfixReserved(name: string) {
  return name.replace(/_\$rw\$$/, "");
}

function store_parsons_attempt(order: Array<string>, correct: boolean) {
  $.ajax({
    type: 'POST',
    url: '/store_parsons_order',
    data: JSON.stringify({
      level: window.State.level,
      exercise: $('#next_parson_button').attr('current_exercise'),
      order: order,
      correct: correct
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function() {
    // Let's do nothing: saving is not a user relevant action -> no feedback required
    }).fail(function(xhr) {
      console.error(xhr);
    });
}


// Todo: As the parsons functionality will rapidly increase, we should probably all store this in a dedicated file (?)
function get_parsons_code() {
    let code = "";
    let count = 1;
    let order = new Array();
    let mistake = false;

    $('.compiler-parsons-box').each(function() {
      // We are only interested in the visible code lines
      if ($(this).parent().is(':visible')) {
        // When the value is 0 there is no code box in the expected spot
        let text = $(this).attr('code') || "";
        if (text.length > 1) {
          // Also add a newline as we removed this from the YAML structure
          code += text + "\n";
        }
        $(this).parents().removeClass('border-black');
        let index = $(this).attr('index') || 999;
        if (index == count) {
          $(this).parents().addClass('border-green-500');
        } else {
          mistake = true;
          $(this).parents().addClass('border-red-500');
        }
        order.push(index);
        count += 1;
      }
    });
    // Before returning the code we want to a-sync store the attempt in the database
    // We only have to set the order and level, rest is handled by the back-end
    store_parsons_attempt(order, !mistake);
    if (mistake) {
      return "";
    }

    return code.replace(/ +$/mg, '');
}

export function get_active_and_trimmed_code() {

  try {
    // This module may or may not exist, so let's be extra careful here.
    const whitespace = ace.require("ace/ext/whitespace");
    whitespace.trimTrailingSpace(theGlobalEditor.session, true);
  } catch (e) {
    console.error(e);
  }

  // ignore the lines with a breakpoint in it.
  const breakpoints = getBreakpoints(editor);
  let code = theGlobalEditor.getValue();
  const storage = window.localStorage;
  const debugLines = storage.getItem('debugLine');

  if (code) {
    let lines = code.split('\n');
    if(debugLines != null){
      lines = lines.slice(0, parseInt(debugLines) + 1);
    }
    for (let i = 0; i < lines.length; i++) {
      if (breakpoints[i] == BP_DISABLED_LINE) {
        lines[i] = '';
      }
    }
    code = lines.join('\n');
  }

  return code;
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

      jsConfetti.addConfetti({
        emojis: currentAdventureConfetti,
        emojiSize: 45,
        confettiNumber: 100,
      });
    }
    else {
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
      $('#blur_toggle_container').show();
      pushAchievement("lets_focus");
  } else {
      $('#blur_toggle_container').hide();
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

export function toggle_keyword_language(lang: string) {
  window.open('?keyword_language=' + lang, "_self");
}

export function toggle_blur_code() {
  // Switch the both icons from hiding / showing
  $('.blur-toggle').toggle();

  // Keep track of a element attribute "blurred" to indicate if blurred or not
  if ($('#editor').attr('blurred') == 'true') {
    $('#editor').css("filter", "");
    $('#editor').css("-webkit-filter", "");
    $('#editor').attr('blurred', 'false');
  } else {
    $('#editor').css("filter", "blur(3px)");
    $('#editor').css("-webkit-filter", "blur(3px)");
    $('#editor').attr('blurred', 'true');
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
        // Check if keyword_language is set to change it to English
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.get('keyword_language') !== null) {
          urlParams.set('keyword_language', 'en');
          window.location.search = urlParams.toString();
        } else {
          location.reload();
        }
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
  $('#image').val(image);
}

export function filter_programs() {
  const level = $('#explore_page_level').val();
  const adventure = $('#explore_page_adventure').val();
  const language = $('#explore_page_language').val();
  window.open('?level=' + level + "&adventure=" + adventure + "&lang=" + language, "_self");
}

export function filter_user_programs(username: string, own_request?: boolean) {
  const level = $('#user_program_page_level').val();
  const adventure = $('#user_program_page_adventure').val();
  const filter = $('input[name="submitted"]:checked').val();
  if (own_request) {
    window.open('?level=' + level + "&adventure=" + adventure + "&filter=" + filter, "_self");
  } else {
    window.open('?user=' + username + '&level=' + level + "&adventure=" + adventure + "&filter=" + filter, "_self");
  }
}

export function filter_admin() {
  const params: Record<string, any> = {};

  const filter = $('#admin_filter_category').val();
  params['filter'] = filter;

  if ($('#hidden-page-input').val()) {
    params['page'] = $('#hidden-page-input').val();
  }

  switch (filter) {
    case 'email':
    case 'username':
      params['substring'] = $('#email_filter_input').val();
      break;
    case 'language':
      params['language'] = $('#language_filter_input').val();
      break;
    case 'keyword_language':
      params['keyword_language'] = $('#keyword_language_filter_input').val();
      break;
    default:
      params['start'] = $('#admin_start_date').val();
      params['end'] = $('#admin_end_date').val();
      break;
  }

  const queryString = Object.entries(params).map(([k, v]) => k + '=' + encodeURIComponent(v)).join('&');
  window.open('?' + queryString, '_self');
}

/**
 * Add types for the gutter event
 */
interface GutterMouseDownEvent {
  readonly domEvent: MouseEvent;
  readonly clientX: number;
  readonly clientY: number;
  readonly editor: AceAjax.Editor;

  getDocumentPosition(): AceAjax.Position;
  stop(): void;
}

/**
 * The '@types/ace' package has the type of breakpoints incorrect
 *
 * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
 * but can be something you pick yourself.
 */
function getBreakpoints(editor: AceAjax.Editor): Breakpoints {
  return editor.session.getBreakpoints() as unknown as Breakpoints;
}

type Breakpoints = Record<number, string>;

/**
 * The 'ace_breakpoint' style has been overridden to show a sleeping emoji in the gutter
 */
const BP_DISABLED_LINE = 'ace_breakpoint';

function get_shift_key(event: Event | undefined) {
  // @ts-ignore
  if (event.shiftKey) {
    return true;
  } return false;
}

if ($("#editor").length) {
  var editor: AceAjax.Editor = ace.edit("editor");
  editor.on("guttermousedown", function (e: GutterMouseDownEvent) {
    const target = e.domEvent.target as HTMLElement;

    // Not actually the gutter
    if (target.className.indexOf("ace_gutter-cell") == -1)
      return;

    if (e.clientX > 25 + target.getBoundingClientRect().left)
      return;

    const breakpoints = getBreakpoints(e.editor);

    let row = e.getDocumentPosition().row;
    if (breakpoints[row] === undefined && row !== e.editor.getLastVisibleRow() + 1) {
      // If the shift key is pressed mark all rows between the current one and the first one above that is a debug line
      if (get_shift_key(event)) {
        let highest_key = row;
        for (const key in breakpoints) {
          const number_key = parseInt(key);
          if (number_key < row) {
            highest_key = number_key;
          }
        }
        for (let i = highest_key; i <= row; i++) {
          e.editor.session.setBreakpoint(i, BP_DISABLED_LINE);
        }
      } else {
        e.editor.session.setBreakpoint(row, BP_DISABLED_LINE);
      }
    } else {
      e.editor.session.clearBreakpoint(row);
    }
    e.stop();
  });

  editor.session.on('changeBreakpoint', () => updateBreakpointVisuals(editor));
}

/**
 * Render markers for all lines that have breakpoints
 *
 * (Breakpoints mean "disabled lines" in Hedy).
 */
function updateBreakpointVisuals(editor: AceAjax.Editor) {
  const breakpoints = getBreakpoints(editor);

  const disabledLines = Object.entries(breakpoints)
    .filter(([_, bpClass]) => bpClass === BP_DISABLED_LINE)
    .map(([line, _]) => line)
    .map(x => parseInt(x, 10));

  markers.strikethroughLines(disabledLines);
}

function debugRun() {
  let language = window.State.lang ?? window.State.keyword_language;
  if (window.State.level != null && language != null) {
    runit(window.State.level, language, "", function () {
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
  }
}

export function resetDebug() {
  if (step_debugger === true) {
    var storage = window.localStorage;
    var continueButton = $("#debug_continue");
    continueButton.show();

    storage.setItem("debugLine", "0");
    clearDebugVariables();
    markCurrentDebuggerLine();
    debugRun();
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
    storage.removeItem("debugLine");

    clearDebugVariables();
    markCurrentDebuggerLine();
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

  const nextDebugLine = debugLine == null
    ? 0
    : parseInt(debugLine, 10) + 1;

  storage.setItem("debugLine", nextDebugLine.toString());
  markCurrentDebuggerLine();

  var lengthOfEntireEditor = theGlobalEditor.getValue().split("\n").filter(e => e).length;
  if (nextDebugLine < lengthOfEntireEditor) {
    debugRun();
  } else {
    stopDebug();
  }
}

function markCurrentDebuggerLine() {
  if (!step_debugger) { return; }

  const storage = window.localStorage;
  var debugLine = storage?.getItem("debugLine");

  if (debugLine != null) {
    var debugLineNumber = parseInt(debugLine, 10);
    markers.setDebuggerCurrentLine(debugLineNumber);
  } else {
    markers.setDebuggerCurrentLine(undefined);
  }
}

export function hide_editor() {
  $('#fold_in_toggle_container').hide();
  $('#code_editor').toggle();
  $('#code_output').addClass('col-span-2');
  $('#fold_out_toggle_container').show();
}

export function show_editor() {
  $('#fold_out_toggle_container').hide();
  $('#code_editor').toggle();
  $('#code_output').removeClass('col-span-2');
  $('#fold_in_toggle_container').show();
}

// See https://github.com/skulpt/skulpt/pull/579#issue-156538278 for the JS version of this code
// We support multiple timers, even though it's unlikely we would ever need them
let timers: number[] = [];

const timeout = (func: () => void, delay: number) => {
  let id: number;
  const wrapper = () => {
    let idx = timers.indexOf(id);
    if (idx > -1) {
      timers.splice(idx, 1);
    }
    func();
  };
  id = window.setTimeout(wrapper, delay);
  timers.push(id);
};

const clearTimeouts = () => {
  timers.forEach(clearTimeout);
  timers = [];
};
