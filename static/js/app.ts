import { initializeSyntaxHighlighter } from './syntaxModesRules';
import { ClientMessages } from './client-messages';
import { modal, error, success, tryCatchPopup } from './modal';
import JSZip from "jszip";
import { Tabs } from './tabs';
import { MessageKey } from './message-translations';
import { turtle_prefix, pygame_prefix, normal_prefix } from './pythonPrefixes'
import { Achievement, Adventure, isServerSaveInfo, ServerSaveInfo } from './types';
import { startIntroTutorial } from './tutorials/tutorial';
import { loadParsonsExercise } from './parsons';
import { checkNow, onElementBecomesVisible } from './browser-helpers/on-element-becomes-visible';
import { initializeDebugger, load_variables } from './debugging';
import { localDelete, localLoad, localSave } from './local';
import { initializeLoginLinks } from './auth';
import { postJson } from './comm';
import { LocalSaveWarning } from './local-save-warning';
import { HedyEditor, EditorType } from './editor';
import { stopDebug } from "./debugging";
import {  HedyCodeMirrorEditorCreator } from './cm-editor';
import { HedyAceEditorCreator } from './ace-editor';

export let theGlobalEditor: HedyEditor;
export let theModalEditor: HedyEditor;
export let theGlobalSourcemap: { [x: string]: any; };
export const theLocalSaveWarning = new LocalSaveWarning();
const editorCreator: HedyCodeMirrorEditorCreator = new HedyCodeMirrorEditorCreator();
const aceEditorCreator: HedyAceEditorCreator = new HedyAceEditorCreator();
let last_code: string;

/**
 * Used to record and undo pygame-related settings
 */
let pygameRunning = false;
/**
 * Represents whether there's an open 'ask' prompt
 */
let askPromptOpen = false;

// Many bits of code all over this file need this information globally.
// Not great but it'll do for now until we refactor this file some more.
let theAdventures: Record<string, Adventure> = {};
export let theLevel: number = 0;
export let theLanguage: string = '';
let theKeywordLanguage: string = 'en';
let theStaticRoot: string = '';
let currentTab: string;
let theUserIsLoggedIn: boolean;

const pygame_suffix =
`# coding=utf8
pygame_end = True
pygame.quit()
`;

const slides_template = `
<!DOCTYPE html>
<html class="sl-root decks export offline loaded">

<head>
	<meta name="viewport"
		content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, minimal-ui">
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<title>Slides Level - 1</title>
	<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>

<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
	<div class="reveal">
		<div class="slides">
			{replace}
		</div>
	</div>

	<!-- Initialize the presentation -->
	<script>
		Reveal.initialize({
			width: 960,
			height: 700,
			margin: 0.05,


			hash: true,
			controls: true,
			progress: true,
			mouseWheel: false,
			showNotes: false,
			slideNumber: false,
			fragmentInURL: true,

			autoSlide: 0,
			autoSlideStoppable: true,

			autoAnimateMatcher: SL.deck.AutoAnimate.matcher,

			center: false,
			shuffle: false,
			loop: false,
			rtl: false,
			navigationMode: "default",

			transition: "slide",
			backgroundTransition: "slide",

			highlight: {
				escapeHTML: false
			},

			plugins: [RevealZoom, RevealNotes, RevealMarkdown, RevealHighlight]
		});
	</script>
</body>
</html>
`;

export interface InitializeAppOptions {
  readonly level: number;
  readonly keywordLanguage: string;
  /**
   * The URL root where static content is hosted
   */
  readonly staticRoot?: string;
}

/**
 * Initialize "global" parts of the main app
 */
export function initializeApp(options: InitializeAppOptions) {
  theLevel = options.level;
  theKeywordLanguage = options.keywordLanguage;
  theStaticRoot = options.staticRoot ?? '';
  // When we are in Alpha or in dev the static root already points to an internal directory
  theStaticRoot = theStaticRoot === '/' ? '' : theStaticRoot;
  initializeSyntaxHighlighter({
    keywordLanguage: options.keywordLanguage,
  });
  initializeHighlightedCodeBlocks(document.body);
  initializeCopyToClipboard();

  // Close the dropdown menu if the user clicks outside of it
  $(document).on("click", function(event){
      if(!$(event.target).closest(".dropdown").length){
          $(".dropdown-menu").slideUp("medium");
          $(".cheatsheet-menu").slideUp("medium");
      }
  });

  $("#search_language").on('keyup', function() {
      let search_query = ($("#search_language").val() as string).toLowerCase();
      $(".language").each(function(){
          if ($(this).html().toLowerCase().includes(search_query)) {
              $(this).show();
          } else {
              $(this).hide();
          }
      });
  });

  // All input elements with data-autosubmit="true" automatically submit their enclosing form
  $('*[data-autosubmit="true"]').on('change', (ev) => {
    $(ev.target).closest('form').trigger('submit');
  });

  initializeLoginLinks();
}

export interface InitializeCodePageOptions {
  readonly page: 'code';
  readonly level: number;
  readonly lang: string;
  readonly adventures: Adventure[];
  readonly start_tutorial?: boolean;
  readonly initial_tab: string;
  readonly current_user_name?: string;
}

/**
 * Initialize the actual code page
 */
export function initializeCodePage(options: InitializeCodePageOptions) {
  theUserIsLoggedIn = !!options.current_user_name;
  if (theUserIsLoggedIn) {
    theLocalSaveWarning.setLoggedIn();
  }

  theAdventures = Object.fromEntries((options.adventures ?? []).map(a => [a.short_name, a]));

  // theLevel will already have been set during initializeApp
  if (theLevel != options.level) {
    throw new Error(`initializeApp set level to ${JSON.stringify(theLevel)} but initializeCodePage sets it to ${JSON.stringify(options.level)}`);
  }
  theLanguage = options.lang;

  // *** EDITOR SETUP ***
  const $editor = $('#editor');
  if ($editor.length) {
    const dir = $("body").attr("dir");
    theGlobalEditor = editorCreator.initializeEditorWithGutter($editor, EditorType.MAIN, dir);
    attachMainEditorEvents(theGlobalEditor);
    error.setEditor(theGlobalEditor);
    initializeDebugger({
      editor: theGlobalEditor,    
      level: theLevel,
      language: theLanguage,
    });
  }

  const anchor = window.location.hash.substring(1);

  const validAnchor = [...Object.keys(theAdventures), 'parsons', 'quiz'].includes(anchor) ? anchor : undefined;

  const tabs = new Tabs({
    // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
    // We click on `level` to load a program associated with level, if any.
    initialTab: validAnchor ?? options.initial_tab,
  });

  tabs.on('beforeSwitch', () => {
    // If there are unsaved changes, we warn the user before changing tabs.
    saveIfNecessary();
  });

  tabs.on('afterSwitch', (ev) => {
    currentTab = ev.newTab;
    const adventure = theAdventures[currentTab];

    // Load initial code from local storage, if available
    const programFromLs = localLoad(currentTabLsKey());
    // if we are in raw (used in slides) we don't want to load from local storage, we always want to show startcode
    if (programFromLs && adventure && ($('#turtlecanvas').attr("raw") != 'yes')) {
      adventure.start_code = programFromLs.code;
      adventure.save_name = programFromLs.saveName;
      adventure.save_info = 'local-storage';
    }

    reconfigurePageBasedOnTab();
    checkNow();
    theLocalSaveWarning.switchTab();
  });

  initializeSpeech();

  if (options.start_tutorial) {
    startIntroTutorial();
  }

  // Share/hand in modals
  $('#share_program_button').on('click', () => $('#share-modal').show());
  $('#hand_in_button').on('click', () => $('#hand-in-modal').show());
  initializeShareProgramButtons();
  initializeHandInButton();

  // Save if user navigates away
  window.addEventListener('beforeunload', () => saveIfNecessary(), { capture: true });

  // Save if program name is changed
  $('#program_name').on('blur', () => saveIfNecessary());
}

function attachMainEditorEvents(editor: HedyEditor) {

  editor.on('change', () => {
    theLocalSaveWarning.setProgramLength(theGlobalEditor.contents.split('\n').length);
    // theGlobalEditor.markers.clearIncorrectLines(); => part of skip faulty feauture
  });

  // If prompt is shown and user enters text in the editor, hide the prompt.
  editor.on('change', function() {
    // TODO: When the user clicks back in the editor when an ask is open
    // it then loses focus the moment the user starts editing again
    if (askPromptOpen) {
      stopit();
      theGlobalEditor.focus(); // Make sure the editor has focus, so we can continue typing
    }
    if ($('#ask-modal').is(':visible')) $('#inline-modal').hide();
    askPromptOpen = false;
    $('#runit').css('background-color', '');
    theGlobalEditor.clearErrors();
    //removing the debugging state when loading in the editor
    stopDebug();
  });

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
      if (!theLevel || !theLanguage) {
        throw new Error('Oh no');
      }
      runit (theLevel, theLanguage, "", function () {
        $ ('#output').focus ();
      });
    }
    // We don't use jquery because it doesn't return true for this equality check.
    if (keyCode === 37 && document.activeElement === document.getElementById ('output')) {
      theGlobalEditor.focus();
      theGlobalEditor.moveCursorToEndOfFile();
    }
  });
  window.addEventListener ('keyup', function (ev) {
    triggerAutomaticSave();
    const keyCode = ev.keyCode;
    if (keyCode === 18) {
      altPressed = false;
      return;
    }
  });

  // Removed until we can fix the skip lines feature
  // We show the error message when clicking on the skipped code
  // this._editor.on("click", function(e) {
  //   let position = e.getDocumentPosition()
  //   position = e.editor.renderer.textToScreenCoordinates(position.row, position.column)

  //   let element = document.elementFromPoint(position.pageX, position.pageY)
  //   if (element !== null && element.className.includes("ace_incorrect_hedy_code")){
  //     let mapIndex = element.classList[0].replace('ace_incorrect_hedy_code_', '');
  //     let mapError = theGlobalSourcemap[mapIndex];

  //     $('#okbox').hide ();
  //     $('#warningbox').hide();
  //     $('#errorbox').hide();
  //     error.show(ClientMessages['Transpile_error'], mapError.error);
  //   }
  // });
}

export interface InitializeViewProgramPageOptions {
  readonly page: 'view-program';
  readonly level: number;
  readonly lang: string;
}

export function initializeViewProgramPage(options: InitializeViewProgramPageOptions) {
  theLevel = options.level;
  theLanguage = options.lang;

  // We need to enable the main editor for the program page as well
  const dir = $("body").attr("dir");
  theGlobalEditor = editorCreator.initializeEditorWithGutter($('#editor'), EditorType.MAIN, dir);
  attachMainEditorEvents(theGlobalEditor);
  error.setEditor(theGlobalEditor);
  initializeDebugger({
    editor: theGlobalEditor,    
    level: theLevel,
    language: theLanguage,
  });
}

export function initializeHighlightedCodeBlocks(where: Element) {
  const dir = $("body").attr("dir");

  // Any code blocks we find inside 'turn-pre-into-ace' get turned into
  // read-only editors (for syntax highlighting)
  for (const container of $(where).find('.turn-pre-into-ace').get()) {
    for (const preview of $(container).find('pre').get()) {
      $(preview)
        .addClass('text-lg rounded overflow-x-hidden')
        // We set the language of the editor to the current keyword_language -> needed when copying to main editor
        .attr('lang', theKeywordLanguage);

      // Only turn into an editor if the editor scrolls into view
      // Otherwise, the teacher manual Frequent Mistakes page is SUPER SLOW to load.
      onElementBecomesVisible(preview, () => {
        // Create this example editor
        const exampleEditor = aceEditorCreator.initializeReadOnlyEditor(preview, dir);
        // Strip trailing newline, it renders better
        exampleEditor.contents = exampleEditor.contents.trimRight();
        // And add an overlay button to the editor if requested via a show-copy-button class, either
        // on the <pre> itself OR on the element that has the '.turn-pre-into-ace' class.
        if ($(preview).hasClass('show-copy-button') || $(container).hasClass('show-copy-button')) {
          const buttonContainer = $('<div>').addClass('absolute ltr:-right-1 rtl:left-2 w-16').css({top: 5}).appendTo(preview);
          let symbol = "⇥";
          if (dir === "rtl") {
            symbol = "⇤";
          }
          $('<button>').css({ fontFamily: 'sans-serif' }).addClass('yellow-btn').text(symbol).appendTo(buttonContainer).click(function() {
            if (!theGlobalEditor?.isReadOnly) {
              theGlobalEditor.contents = exampleEditor.contents + '\n';
            }
            update_view("main_editor_keyword_selector", <string>$(preview).attr('lang'));
            stopit();
            clearOutput();
          });
        }

        const levelStr = $(preview).attr('level');
        if (levelStr) {
          exampleEditor.setHighlighterForLevel(parseInt(levelStr, 10));
        }
      });
    }
  }
}

export function getHighlighter(level: number) {
  return `ace/mode/level${level}`;
}

export function stopit() {
  if (pygameRunning) {
      // when running pygame, raise the pygame quit event
      Sk.insertPyGameEvent("quit");
      Sk.unbindPygameListeners();

      pygameRunning = false;
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

  askPromptOpen = false;
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

export async function runit(level: number, lang: string, disabled_prompt: string, cb: () => void) {
  // Copy 'currentTab' into a variable, so that our event handlers don't mess up
  // if the user changes tabs while we're waiting for a response
  const adventureName = currentTab;

  if (askPromptOpen) {
    // If there is no message -> don't show a prompt
    if (disabled_prompt) {
      return modal.notifyError(disabled_prompt);
    }
    return;
  }

  theLocalSaveWarning.clickRun();

  // Make sure to stop previous PyGame event listeners
  if (typeof Sk.unbindPygameListeners === 'function') {
    Sk.unbindPygameListeners();
  }

  // We set the run limit to 1ms -> make sure that the previous programs stops (if there is any)
  Sk.execLimit = 1;
  $('#runit').hide();
  $('#stopit').show();
  $('#saveFilesContainer').hide();
  clearOutput();

  try {
    var editor = theGlobalEditor;
    var code = "";
    if ($('#parsons_container').is(":visible")) {
      code = get_parsons_code();
      // We return no code if all lines are empty or there is a mistake -> clear errors and do nothing
      if (!code) {
        editor.clearErrors();
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
        editor.clearErrors()
        stopit();
        return;
      }
    }

    editor.clearErrors()
    removeBulb();
    console.log('Original program:\n', code);

    const adventure = theAdventures[adventureName];

    try {
      cancelPendingAutomaticSave();
      let data = {
        level: `${level}`,
        code: code,
        lang: lang,
        skip_faulty: false,
        tutorial: $('#code_output').hasClass("z-40"), // if so -> tutorial mode
        read_aloud : !!$('#speak_dropdown').val(),
        adventure_name: adventureName,

        // Save under an existing id if this field is set
        program_id: isServerSaveInfo(adventure?.save_info) ? adventure.save_info.id : undefined,
        save_name: saveNameFromInput(),
      };

      let response = await postJsonWithAchievements('/parse', data);
      console.log('Response', response);

      if (response.Warning && $('#editor').is(":visible")) {
        //storeFixedCode(response, level);
        error.showWarning(ClientMessages['Transpile_warning'], response.Warning);
      }

      // if (!data.skip_faulty && response.Error) {
      //   data.skip_faulty = true;
      //   error.showWarningSpinner();
      //   error.showWarning(ClientMessages['Execute_error'], ClientMessages['Errors_found']);
      //   response = await postJsonWithAchievements('/parse', data);
      //   error.hide(true);
      // }

      showAchievements(response.achievements, false, "");
      if (adventure && response.save_info) {
        adventure.save_info = response.save_info;
        adventure.start_code = code;
      }
      if (response.Error) {
        error.show(ClientMessages['Transpile_error'], response.Error);
        if (response.Location && response.Location[0] != "?") {
          //storeFixedCode(response, level);
          // Location can be either [row, col] or just [row].
          theGlobalEditor.highlightError(response.Location[0], response.Location[1]);
        }
        $('#stopit').hide();
        $('#runit').show();
        return;
      }
      runPythonProgram(response.Code, response.source_map, response.has_turtle, response.has_pygame, response.has_sleep, response.Warning, cb).catch(function(err) {
        // The err is null if we don't understand it -> don't show anything
        if (err != null) {
          error.show(ClientMessages['Execute_error'], err.message);
          reportClientError(level, code, err.message);
        }
      });
    } catch (e: any) {
      console.error(e);
      if (e.internetError) {
        error.show(ClientMessages['Connection_error'], ClientMessages['CheckInternet']);
      } else {
        error.show(ClientMessages['Other_error'], ClientMessages['ServerError']);
      }
    }
  } catch (e: any) {
    modal.notifyError(e.responseText);
  }
}

export async function saveMachineFiles() {
  const response = await postJsonWithAchievements('/generate_machine_files', {
    level: theLevel,
    code: get_active_and_trimmed_code(),
    lang: theLanguage,
  });

  if (response.filename) {
    // Download the file
    window.location.replace('/download_machine_files/' + response.filename);
  }
}

// We've observed that this code may gets invoked 100s of times in quick succession. Don't
// ever push the same achievement more than once per page load to avoid this.
const ACHIEVEMENTS_PUSHED: Record<string, boolean> = {};

export async function pushAchievement(achievement: string) {
  if (ACHIEVEMENTS_PUSHED[achievement]) {
      console.warn('Achievement already pushed, this may be a programming issue: ', achievement);
      return;
  }
  ACHIEVEMENTS_PUSHED[achievement] = true;

  try {
    const response = await postJson('/achievements/push-achievement', { achievement });
    showAchievements(response.achievements, false, "");
  } catch {
    // This might fail commonly with a 403 (not logged in). Ignore any errors anyway.
  }
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

export async function showAchievements(achievements: Achievement[] | undefined, reload: boolean, redirect: string) {
  if (!achievements || achievements.length === 0) {
    return;
  }

  for (const achievement of achievements) {
    await showAchievement(achievement);
  }

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

function showAchievement(achievement: Achievement) {
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
  if (theGlobalEditor?.isReadOnly) {
    return;
  }

  theGlobalEditor.contents = exampleCode + '\n';
  //As the commands try-it buttons only contain english code -> make sure the selected language is english
  if (!($('#editor').attr('lang') == 'en')) {
      $('#editor').attr('lang', 'en');
      update_view("main_editor_keyword_selector", "en");
  }
}

export function viewProgramLink(programId: string) {
  return window.location.origin + '/hedy/' + programId + '/view';
}

export async function delete_program(id: string, index: number, prompt: string) {
  await modal.confirmP(prompt);
  await tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/programs/delete', { id });
    showAchievements(response.achievement, true, "");
    $('#program_' + index).remove();
    modal.notifySuccess(response.message);
  });
}

function set_favourite(index: number) {
    $('.favourite_program_container').removeClass('text-yellow-400');
    $('.favourite_program_container').addClass('text-white');

    $('#favourite_program_container_' + index).removeClass('text-white');
    $('#favourite_program_container_' + index).addClass('text-yellow-400');
}

export async function set_favourite_program(id: string, index: number, prompt: string) {
  await modal.confirmP(prompt);
  await tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/programs/set_favourite', { id });
    set_favourite(index)
    modal.notifySuccess(response.message);
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
  tryCatchPopup(async () => {
    await postJsonWithAchievements('/programs/submit', { id });
    change_to_submitted(index);
  });
}

export async function set_explore_favourite(id: string, favourite: number) {
  let prompt = "Are you sure you want to remove this program as a \"Hedy\'s choice\" program?";
  if (favourite) {
    prompt = "Are you sure you want to set this program as a \"Hedy\'s choice\" program?";
  }
  await modal.confirmP(prompt);

  await tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/programs/set_hedy_choice', {
      id: id,
      favourite: favourite
    });

    modal.notifySuccess(response.message);
    $('#' + id).toggleClass('text-white', favourite !== 1);
    $('#' + id).toggleClass('text-yellow-500', favourite === 1);
  });
}

export function report_program(prompt: string, id: string) {
  tryCatchPopup(async () => {
    await modal.confirmP(prompt);
    const response = await postJsonWithAchievements('/programs/report', { id });
    modal.notifySuccess(response.message);
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
  modal.notifySuccess(prompt, 3000);
}

/**
 * Do a POST with the error to the server so we can log it
 */
function reportClientError(level: number, code: string, client_error: string) {
  postJsonWithAchievements('/report_error', {
    level: `${level}`,
    code: code,
    page: window.location.href,
    client_error: client_error,
  });
}

window.onerror = function reportClientException(message, source, line_number, column_number, error) {
  postJsonWithAchievements('/client_exception', {
    message: message,
    source: source,
    line_number: line_number,
    column_number: column_number,
    error: error,
    url: window.location.href,
    user_agent: navigator.userAgent,
  });
}

export function runPythonProgram(this: any, code: string, sourceMap: any, hasTurtle: boolean, hasPygame: boolean, hasSleep: boolean, hasWarnings: boolean, cb: () => void) {
  // If we are in the Parsons problem -> use a different output
  let outputDiv = $('#output');

  if (sourceMap){
    // theGlobalSourcemap = sourceMap;
    // let Range = ace.require("ace/range").Range

    // // We loop through the mappings and underline a mapping if it contains an error
    // for (const index in sourceMap) {
    //   const map = sourceMap[index];
    //   const range = new Range(
    //     map.hedy_range.from_line-1, map.hedy_range.from_column-1,
    //     map.hedy_range.to_line-1, map.hedy_range.to_column-1
    //   )

    //   if (map.error != null){
    //     theGlobalEditor.markers.addMarker(range, `ace_incorrect_hedy_code_${index}`, "text", true);
    //   }
    // }
  }

  //Saving the variable button because sk will overwrite the output div
  const variableButton = outputDiv.find('#variable_button');
  const variables = outputDiv.find('#variables');
  outputDiv.empty();
  outputDiv.append(variableButton);
  outputDiv.append(variables);

  const storage = window.localStorage;
  let skulptExternalLibraries:{[index: string]:any} = {
      './extensions.js': {
        path: theStaticRoot + "/vendor/skulpt-stdlib-extensions.js",
      },
  };
  let debug = storage.getItem("debugLine");

  Sk.pre = "output";
  const turtleConfig = (Sk.TurtleGraphics || (Sk.TurtleGraphics = {}));
  turtleConfig.target = 'turtlecanvas';
  // If the adventures are not shown  -> increase height of turtleConfig
  if ($('#adventures-tab').is(":hidden")) {
      turtleConfig.height = 600;
      turtleConfig.worldHeight = 600;
  } else if ($('#turtlecanvas').attr("raw") == 'yes'){
      turtleConfig.height = 150;
      turtleConfig.worldHeight = 250;
  }
  else {
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
      './extensions.js': {
        path: theStaticRoot + "/vendor/skulpt-stdlib-extensions.js",
      },
      './pygame.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/init.js",
      },
      './display.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/display.js",
      },
      './draw.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/draw.js",
      },
      './event.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/event.js",
      },
      './font.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/font.js",
      },
      './image.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/image.js",
      },
      './key.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/key.js",
      },
      './mouse.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/mouse.js",
      },
      './transform.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/transform.js",
      },
      './locals.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/locals.js",
      },
      './time.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/time.js",
      },
      './version.js': {
        path: theStaticRoot + "/vendor/pygame_4_skulpt/version.js",
      },
      './buttons.js': {
          path: theStaticRoot + "/js/buttons.js",
      },
    };

    code_prefix += pygame_prefix;

    initSkulpt4Pygame();
    initCanvas4PyGame();
    let pygameModal = $('#pygame-modal');

    const codeContainsInputFunctionBeforePygame = new RegExp(
      "input\\([\\s\\S]*\\)[\\s\\S]*while not pygame_end", 'gm'
    ).test(code);

    if (!codeContainsInputFunctionBeforePygame) {
      pygameModal.show();
    }

    if (hasTurtle) {
      pygameModal.addClass('absolute');
      pygameModal.addClass('bottom-0');
      pygameModal.addClass('w-full');
    } else {
      pygameModal.removeClass('absolute');
      pygameModal.removeClass('bottom-0');
      pygameModal.removeClass('w-full');
    }

    document.onkeydown = animateKeys;
    pygameRunning = true;
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
        return ClientMessages ['Program_too_long'];
      } else {
        return null;
      }
    },
    // We want to make the timeout function a bit more sophisticated that simply setting a value
    // In levels 1-6 users are unable to create loops and programs with a lot of lines are caught server-sided
    // So: a very large limit in these levels, keep the limit on other onces.
    execLimit: (function () {
      const level = theLevel;
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
      $('#saveFilesContainer').show();
    }

    // Check if the program was correct but the output window is empty: Return a warning
    if ($('#output').is(':empty') && $('#turtlecanvas').is(':empty')) {
      if(!debug){
        pushAchievement("error_or_empty");
        error.showWarning(ClientMessages['Transpile_warning'], ClientMessages['Empty_output']);
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
    scrollOutputToBottom();
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

    if (pygameRunning) {
      Sk.unbindPygameListeners();
      document.onkeydown = null;
      $('#pygame-modal').hide();
    }

    return new Promise(function(ok) {
      askPromptOpen = true;

      const input = $('#ask-modal input[type="text"]');
      $('#ask-modal .caption').text(prompt);
      input.val('');
      input.attr('placeholder', prompt);
      speak(prompt)

      setTimeout(function() {
        input.focus();
      }, 0);
      $('#ask-modal form').one('submit', function(event) {
        askPromptOpen = false;
        event.preventDefault();
        $('#ask-modal').hide();

        if (hasTurtle) {
          $('#turtlecanvas').show();
        }

        if (pygameRunning) {
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

        // Scroll the output div to the bottom so you can see the question
        scrollOutputToBottom();
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

      // I'm not sure what the code below was supposed to do,
      // but it was referring to 'self.width' which does not
      // exist, and the result would be 'undefined + 42 == NaN'.
      //
      // (as any to make TypeScript allow the nonsensical addition)
      $(div2).width(undefined as any + 42);
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

function initializeSpeech() {
  // If we are running under cypress, always show the languages dropdown (even if the browser doesn't
  // have TTS capabilities), so that we can test if the logic for showing the dropdown at least runs
  // successfully.
  const isBeingTested = !!(window as any).Cypress;

  if (!window.speechSynthesis && !isBeingTested) { return; /* No point in even trying */ }
  if (!theLanguage) { return; /* Not on a code page */ }

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

    const voices = findVoices(theLanguage);

    if (voices.length > 0 || isBeingTested) {
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

async function store_parsons_attempt(order: Array<string>, correct: boolean) {
  try {
    await postJsonWithAchievements('/store_parsons_order', {
      level: theLevel,
      exercise: $('#next_parson_button').attr('current_exercise'),
      order: order,
      correct: correct
    });
  } catch (e) {
    // Let's do nothing: saving is not a user relevant action -> no feedback required
    console.error(e);
  };
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
  theGlobalEditor.trimTrailingSpace();
  const storage = window.localStorage;
  const debugLine = storage.getItem("debugLine");
  return theGlobalEditor.getActiveContents(debugLine);
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
      let currentAdventureConfetti = getConfettiForAdventure(currentAdventure ?? '' as any);

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

function getConfettiForAdventure(adventure: MessageKey){
  if (ClientMessages[adventure]) {
    return Array.from(ClientMessages[adventure]).filter(x => x !== ',' && x !== ' ');
  }
  return [['🌈'], ['⚡️'], ['💥'], ['✨'], ['💫']];
}

/**
 * Scroll the output to bottom immediately
 */
function scrollOutputToBottom() {
  const outputDiv = $('#output');
  outputDiv.scrollTop(outputDiv.prop('scrollHeight'));
}

export function modalStepOne(level: number){
  createModal(level);
  let $modalEditor = $('#modal-editor');
  if ($modalEditor.length) {
    const dir = $("body").attr("dir");
    theModalEditor = editorCreator.initializeEditorWithGutter($modalEditor, EditorType.MODAL, dir);
  }
}

function showSuccesMessage(){
  removeBulb();
  var allsuccessmessages = ClientMessages['Transpile_success'].split('\n');
  var randomnum: number = Math.floor(Math.random() * allsuccessmessages.length);
  success.show(allsuccessmessages[randomnum]);
}

function createModal(level:number ){
  let editor = "<div id='modal-editor' class=\"w-full flex-1 text-lg rounded\" style='height:200px; width:50vw;'></div>".replace("{level}", level.toString());
  let title = ClientMessages['Program_repair'];
  modal.repair(editor, 0, title);
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
    theGlobalEditor.resize(576);
  } else {
    $('#editor-area').addClass('mt-5');
    $('#code_editor').height('22rem');
    $('#code_output').height('22rem');
    theGlobalEditor.resize(352);
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

export async function change_language(lang: string) {
  await tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/change_language', { lang });
    if (response.succes) {
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
  });
}

/**
 * Post JSON, return the result on success, throw an exception on failure
 *
 * Automatically handles any achievements the server might send our way.
 */
async function postJsonWithAchievements(url: string, data: any): Promise<any> {
  const response = await postJson(url, data);
  showAchievements(response.achievement, true, "");
  return response;
}

export function change_keyword_language(start_lang: string, new_lang: string) {
  tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/translate_keywords', {
      code: theGlobalEditor,
      start_lang: start_lang,
      goal_lang: new_lang,
      level: theLevel,
    });

    if (response.success) {
      theGlobalEditor.contents = response.code;
      $('#editor').attr('lang', new_lang);
      update_view('main_editor_keyword_selector', new_lang);
    }
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

export function downloadSlides(level: number) {
  var iframe : any = document.getElementById(`level-${level}-slides`)!;
  iframe.setAttribute('src',`/slides/${level}`);
  $(`#level-${level}-slides`).on('load', function (){
    var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
    var slides = innerDoc.getElementsByTagName('section');
    var slidesHTML = ''
    for (let i = 0; i < slides.length; i++) {
      var innerIframe = slides[i].getElementsByTagName('iframe');
      for (let j = 0; j < innerIframe.length; j++) {
        var a = document.createElement('a');
        a.href = 'https://www.hedy.org' + innerIframe[j].getAttribute('src');
        a.appendChild(document.createTextNode(a.href));
        slides[i].appendChild(a);
        slides[i].removeChild(innerIframe[j]);
      }
      slidesHTML += '\n'+ slides[i].outerHTML;
    }

    var template = slides_template.replace('{replace}', slidesHTML);
    var zip = JSZip();
    zip.file('index.html', template);
    zip.folder("lib");
    zip.folder(`hedy-level-${level}`);
    zip.generateAsync({type: 'blob'})
       .then(function(content: any) {
          download(content, `hedy-level-${level}.zip`, "zip");
       });
  })
}

function download(data: any, filename: any, type: any) {
  var file = new Blob([data], {type: type});
  var a = document.createElement("a"),
  url = URL.createObjectURL(file);
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  setTimeout(function() {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
}

/**
 * Hide all things that may have been dynamically shown when switching tabs
 *
 * Reset the state of the editor.
 */
function resetWindow() {
  $('#warningbox').hide ();
  $('#errorbox').hide ();
  $('#okbox').hide ();
  $('#repair_button').hide();
  const output = $('#output');
  const variable_button = $(output).find('#variable_button');
  const variables = $(output).find('#variables');
  output.empty();
  $('#turtlecanvas').empty();
  output.append(variable_button);
  output.append(variables);
  theGlobalEditor?.clearSelection();
  theGlobalEditor?.clearBreakpoints();
}

/**
 * Update page element visibilities/states based on the state of the current tab
 */
function updatePageElements() {
  const isCodeTab = !(currentTab === 'quiz' || currentTab === 'parsons');

  // .toggle(bool) sets visibility based on the boolean

  // Explanation area is visible for non-code tabs, or when we are NOT in developer's mode
  $('#adventures-tab').toggle(!(isCodeTab && $('#developers_toggle').is(":checked")));
  $('#developers_toggle_container').toggle(isCodeTab);
  $('#level-header input').toggle(isCodeTab);
  $('#parsons_code_container').toggle(currentTab === 'parsons');
  $('#editor-area').toggle(isCodeTab || currentTab === 'parsons');
  $('#editor').toggle(isCodeTab);
  $('#debug_container').toggle(isCodeTab);
  $('#program_name_container').toggle(isCodeTab);
  theGlobalEditor.isReadOnly = false;

  const adventure = theAdventures[currentTab];
  if (adventure) {
    const saveInfo: ServerSaveInfo = isServerSaveInfo(adventure.save_info)
      ? adventure.save_info
      : { id : '*dummy*' };

    // SHARING SETTINGS
    // Star on "share" button is filled if program is already public, outlined otherwise
    const isPublic = !!saveInfo.public;
    $('#share_program_button')
      .toggleClass('active-bluebar-btn', isPublic);
    $(`#share-${isPublic ? 'public' : 'private'}`).prop('checked', true);

    // Show <...data-view="if-public-url"> only if we have a public url
    $('[data-view="if-public"]').toggle(isPublic);
    $('[data-view="if-public-url"]').toggle(!!saveInfo.public_url);
    $('input[data-view="public-url"]').val(saveInfo.public_url ?? '');

    // Paper plane on "hand in" button is filled if program is already submitted, outlined otherwise
    const isSubmitted = !!saveInfo.submitted;
    $('#hand_in_button')
      .toggleClass('active-bluebar-btn', isSubmitted);

    // Show <...data-view="if-submitted"> only if we have a public url
    $('[data-view="if-submitted"]').toggle(isSubmitted);
    $('[data-view="if-not-submitted"]').toggle(!isSubmitted);

    theGlobalEditor.isReadOnly = isSubmitted;
  }
}

/**
 * After switching tabs, show/hide elements
 */
function reconfigurePageBasedOnTab() {
  resetWindow();

  updatePageElements();

  if (currentTab === 'parsons') {
    loadParsonsExercise(theLevel, 1);
    return;
  }

  const adventure = theAdventures[currentTab];
  if (adventure) {
    $ ('#program_name').val(adventure.save_name);
    theGlobalEditor.contents = adventure.start_code;
  }
}

/**
 * Find the containing modal for the event target, and close it
 *
 * The modal will be the containing HTML element that has data-modal="true".
 *
 * Intended to be used from HTML: click="hedyApp.closeContainingModal(this)"
 */
export function closeContainingModal(target: HTMLElement) {
  $(target).closest('[data-modal="true"]').hide();
}

function initializeShareProgramButtons() {
  $('input[type="radio"][name="public"]').on('change', (ev) => {
    if ((ev.target as HTMLInputElement).checked) {
      const isPublic = $(ev.target).val() === '1' ? true : false;

      // Async-safe copy of current tab
      const adventure = theAdventures[currentTab];

      tryCatchPopup(async () => {
        await saveIfNecessary();

        const saveInfo = isServerSaveInfo(adventure?.save_info) ? adventure?.save_info : undefined;
        if (!saveInfo) {
          throw new Error('This program does not have an id');
        }

        const response = await postJsonWithAchievements('/programs/share', {
          id: saveInfo.id,
          public: isPublic,
        });

        modal.notifySuccess(response.message);
        if (response.save_info) {
          adventure.save_info = response.save_info;
        }
        updatePageElements();
      });
    }
  })
}

function initializeHandInButton() {
  $('#do_hand_in_button').on('click', () => {
      // Async-safe copy of current tab
      const adventure = theAdventures[currentTab];

      tryCatchPopup(async () => {
        await saveIfNecessary();

        const saveInfo = isServerSaveInfo(adventure?.save_info) ? adventure.save_info : undefined;
        if (!saveInfo) {
          throw new Error('This program does not have an id');
        }
        const response = await postJsonWithAchievements('/programs/submit', {
          id: saveInfo.id,
        });

        modal.notifySuccess(response.message);
        if (response.save_info) {
          adventure.save_info = response.save_info;
        }
        updatePageElements();
      });
  });
}

/**
 * Initialize copy to clipboard buttons.
 *
 * For all elements with data-action="copy-to-clipboard", find the containing
 * data-copy="container" items and an <input> in there, and copy it to the clipboard.
 */
function initializeCopyToClipboard() {
  $('[data-action="copy-to-clipboard"]').on('click', (ev) => {
    const text = $(ev.target).closest('[data-copy="container"]').find('input').val();
    if (typeof text === 'string') {
      copy_to_clipboard(text, ClientMessages.copy_link_to_share);
    }
  });
}

function saveNameFromInput(): string {
  return $('#program_name').val() as string;
}

function programNeedsSaving(adventureName: string) {
  const adventure = theAdventures[adventureName];
  if (!adventure) {
    return false;
  }

  // We need to save if the content changed, OR if we have the opportunity to
  // save a program that was loaded from local storage to the server.
  // (Submitted programs are never saved again).
  const programChanged = theGlobalEditor.contents !== adventure.start_code;
  const nameChanged = $('#program_name').val() !== adventure.save_name;
  const localStorageCanBeSavedToServer = theUserIsLoggedIn && adventure.save_info === 'local-storage';
  const isUnchangeable = isServerSaveInfo(adventure.save_info) ? adventure.save_info.submitted : false;

  // Do not autosave the program if the size is very small compared to the previous
  // save. This protects against accidental `Ctrl-A, hit a key` and everything is gone. Clicking the
  // "Run" button will always save regardless of size.
  const wasSavedBefore = adventure.save_info !== undefined;
  const suspiciouslySmallFraction = 0.5;
  const programSuspiciouslyShrunk = wasSavedBefore && theGlobalEditor.contents.length < adventure.start_code.length * suspiciouslySmallFraction;

  return (programChanged || nameChanged || localStorageCanBeSavedToServer) && !isUnchangeable && !programSuspiciouslyShrunk;
}

/**
 * (Re)set a timer to trigger a save in N second
 */
let saveTimer: number | undefined;
export function triggerAutomaticSave() {
  const saveSeconds = 20;
  cancelPendingAutomaticSave();
  saveTimer = window.setTimeout(() => saveIfNecessary(), saveSeconds * 1000);
}

function cancelPendingAutomaticSave() {
  if (saveTimer) {
    window.clearTimeout(saveTimer);
  }
}

async function saveIfNecessary() {
  // Async-safe copy of current tab
  const adventureName = currentTab;
  const adventure = theAdventures[adventureName];
  if (!programNeedsSaving(adventureName) || !adventure) {
    return;
  }

  console.info('Saving program automatically...');

  const code = theGlobalEditor.contents;
  const saveName = saveNameFromInput();


  if (theUserIsLoggedIn) {
    const saveInfo = isServerSaveInfo(adventure.save_info) ? adventure.save_info : undefined;
    const response = await postJsonWithAchievements('/programs', {
      level: theLevel,
      lang:  theLanguage,
      name:  saveName,
      code:  code,
      adventure_name: adventureName,
      program_id: saveInfo?.id,
      // We pass 'public' in here to save the backend a lookup
      share: saveInfo?.public,
    });

    // Record that we saved successfully
    adventure.start_code = code;
    if (response.save_info) {
      adventure.save_info = response.save_info;
    }
    localDelete(currentTabLsKey());
  } else {
    localSave(currentTabLsKey(), { saveName, code });
    adventure.start_code = code;
  }
}

function currentTabLsKey() {
  return `save-${currentTab}-${theLevel}`;
}

export async function share_program(id: string, index: number, Public: boolean, prompt: string) {
  await modal.confirmP(prompt);
  await tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/programs/share', { id, public: Public });
    showAchievements(response.achievement, true, "");
    if (Public) {
      change_shared(true, index);
    } else {
      change_shared(false, index);
    }
    modal.notifySuccess(response.message);
  });
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