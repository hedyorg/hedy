import { ClientMessages } from './client-messages';
import { modal, error, success, tryCatchPopup } from './modal';
import JSZip from "jszip";
import * as Tone from 'tone'
import { SwitchTabsEvent, Tabs } from './tabs';
import { MessageKey } from './message-translations';
import { turtle_prefix, pressed_prefix, normal_prefix, music_prefix } from './pythonPrefixes'
import { Adventure, isServerSaveInfo, ServerSaveInfo } from './types';
import { get_parsons_code, initializeParsons, loadParsonsExercise } from './parsons';
import { checkNow, onElementBecomesVisible } from './browser-helpers/on-element-becomes-visible';
import {
    incrementDebugLine,
    initializeDebugger,
    load_variables,
    startDebug,
    toggleVariableView
} from './debugging';
import { localDelete, localLoad, localSave } from './local';
import { initializeLoginLinks } from './auth';
import { postJson, postNoResponse } from './comm';
import { LocalSaveWarning } from './local-save-warning';
import { HedyEditor, EditorType } from './editor';
import { stopDebug } from "./debugging";
import { HedyCodeMirrorEditorCreator } from './cm-editor';
import { initializeActivity } from './user-activity';
import { IndexTabs, SwitchAdventureEvent } from './index-tabs';
export let theGlobalDebugger: any;
export let theGlobalEditor: HedyEditor;
export let theModalEditor: HedyEditor;
export let theGlobalSourcemap: { [x: string]: any; };
export const theLocalSaveWarning = new LocalSaveWarning();
const editorCreator: HedyCodeMirrorEditorCreator = new HedyCodeMirrorEditorCreator();
let last_code: string;

/**
 * Represents whether there's an open 'ask' prompt
 */
let askPromptOpen = false;
/**
 * Represents whether there's an open 'sleeping' prompt
 */
let sleepRunning = false;

// Many bits of code all over this file need this information globally.
// Not great but it'll do for now until we refactor this file some more.
let theAdventures: Record<string, Adventure> = {};
export let theLevel: number = 0;
export let theLanguage: string = '';
export let theKeywordLanguage: string = 'en';
let theStaticRoot: string = '';
let currentTab: string;
let theUserIsLoggedIn: boolean;
//create a synth and connect it to the main output (your speakers)
//const synth = new Tone.Synth().toDestination();

const synth = new Tone.PolySynth(Tone.Synth).toDestination();

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
  initializeCopyToClipboard();

  // Close the dropdown menu if the user clicks outside of it
  $(document).on("click", function(event){
    // The following is not needed anymore, but it saves the next for loop if the click is not for dropdown.
    if (!$(event.target).closest(".dropdown").length) {
      $('.dropdown_menu').slideUp("medium");
      $('.cheatsheet_menu').slideUp("medium");
      return;
    }

    const allDropdowns = $('.dropdown_menu')
    for (const dd of allDropdowns) {
      // find the closest dropdown button (element) that initiated the event
      const c = $(dd).closest('.dropdown')[0]
      // if the click event target is not within or close to the container, slide up the dropdown menu
      if (!$(event.target).closest(c).length) {
        $(dd).slideUp('fast');
      }
    }
  });

  $('#search_language').on('keyup', function() {
    let search_query = ($('#search_language').val() as string).toLowerCase();
    $('.language').each(function(){
      let languageName = $(this).html().toLowerCase();
      let englishName = $(this).attr('data-english');
      if (englishName !== undefined && (languageName.includes(search_query) || englishName.toLowerCase().includes(search_query))) {
          $(this).show();
        } else {
          $(this).hide();
          $('#add_language_btn').show();
        }
    });
  });

  // All input elements with data-autosubmit="true" automatically submit their enclosing form
  $('*[data-autosubmit="true"]').on('change', (ev) => {
    $(ev.target).closest('form').trigger('submit');
  });

  initializeLoginLinks();

  initializeActivity();
}

export interface InitializeCodePageOptions {
  readonly page: 'code' | 'tryit';
  readonly level: number;
  readonly lang: string;
  readonly adventures: Adventure[];
  readonly initial_tab: string;
  readonly current_user_name?: string;
  readonly suppress_save_and_load?: boolean;
  readonly enforce_developers_mode?: boolean;
}

/**
 * Initialize the actual code page
 */
export function initializeCodePage(options: InitializeCodePageOptions) {
  theUserIsLoggedIn = !!options.current_user_name;
  if (theUserIsLoggedIn) {
    theLocalSaveWarning.setLoggedIn();
  }

  // Event listener to close the adventures dropdown when you click outside of it
  document.addEventListener('click', (ev) => {
    const target = ev.target as HTMLElement;
    const parent = document.getElementById('level_adventure_title');
    if (parent?.contains(target)) {
      return;
    }
    if ($('#dropdown-level:visible').length) {
      $('#dropdown-level').slideToggle('medium');
      document.getElementById('dropdown_index_arrow')?.classList.toggle('rotate-180');
    }
  });

  theAdventures = Object.fromEntries((options.adventures ?? []).map(a => [a.short_name, a]));

  // theLevel will already have been set during initializeApp
  if (theLevel != options.level) {
    throw new Error(`initializeApp set level to ${JSON.stringify(theLevel)} but initializeCodePage sets it to ${JSON.stringify(options.level)}`);
  }
  theLanguage = options.lang;

  // *** EDITOR SETUP ***
  const $editor = $('#editor');
  if ($editor.length) {
    const dir = $('body').attr('dir');
    theGlobalEditor = editorCreator.initializeEditorWithGutter($editor, EditorType.MAIN, dir);
    attachMainEditorEvents(theGlobalEditor);
    initializeDebugger({
      editor: theGlobalEditor,
      level: theLevel,
      language: theLanguage,
      keywordLanguage: theKeywordLanguage,
    });
  }

  const anchor = window.location.hash.substring(1);

  const validAnchor = [...Object.keys(theAdventures), 'parsons', 'quiz'].includes(anchor) ? anchor : undefined;
  let tabs: any;
  const isTryItPage = options.page == 'tryit';
  if (isTryItPage) {
    tabs = new IndexTabs({
      // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
      // We click on `level` to load a program associated with level, if any.
      initialTab: validAnchor ?? options.initial_tab,
      level: options.level
    });
  } else {
    tabs = new Tabs({
      // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
      // We click on `level` to load a program associated with level, if any.
      initialTab: validAnchor ?? options.initial_tab,
    });
  }
  tabs.on('beforeSwitch', () => {
    // If there are unsaved changes, we warn the user before changing tabs.
    saveIfNecessary();
  });

  tabs.on('afterSwitch', (ev: SwitchTabsEvent | SwitchAdventureEvent) => {
    currentTab = ev.newTab;
    const adventure = theAdventures[currentTab];

    if (!options.suppress_save_and_load) {
      // Load initial code from local storage, if available
      const programFromLs = localLoad(currentTabLsKey());
      // if we are in raw (used in slides) we don't want to load from local storage, we always want to show startcode
      if (programFromLs && adventure) {
        adventure.editor_contents = programFromLs.code;
        adventure.save_name = programFromLs.saveName;
        adventure.save_info = 'local-storage';
      }
    }
    reconfigurePageBasedOnTab(isTryItPage, options.enforce_developers_mode);
    checkNow();
    theLocalSaveWarning.switchTab();
  });

  initializeSpeech();

  // Share/hand in modals
  $('#share_program_button').on('click', () => $('#share_modal').show());
  $('#hand_in_button').on('click', () => $('#hand_in_modal').show());
  initializeShareProgramButtons();
  initializeHandInButton();

  if (options.suppress_save_and_load) {
    disableAutomaticSaving();
  }

  // Save if user navigates away
  window.addEventListener('beforeunload', () => saveIfNecessary(), { capture: true });

  // Save if program name is changed
  $('#program_name').on('blur', () => saveIfNecessary());

  // Scroll to this level in the adventures side pane
  document.getElementById(`level_${options.level}_header`)?.scrollIntoView({block: 'center'});
}

function attachMainEditorEvents(editor: HedyEditor) {

  editor.on('change', () => {
    theLocalSaveWarning.setProgramLength(theGlobalEditor.contents.split('\n').length);
  });

  // If prompt is shown and user enters text in the editor, hide the prompt.
  editor.on('change', function() {
    if (askPromptOpen) {
      stopit();
      theGlobalEditor.focus(); // Make sure the editor has focus, so we can continue typing
    }
    if ($('#ask_modal').is(':visible')) $('#inline_modal').hide();
    askPromptOpen = false;
    $('#runit').css('background-color', '');
    theGlobalEditor.clearErrors();
    theGlobalEditor.clearIncorrectLines();
    //removing the debugging state when loading in the editor
    stopDebug();
  });

  editor.on('click', (event: MouseEvent) => {
    editor.skipFaultyHandler(event);
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
      runit (theLevel, theLanguage, false, "", "run",function () {
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
}

export interface InitializeViewProgramPageOptions {
  readonly page: 'view-program';
  readonly level: number;
  readonly lang: string;
  readonly code: string;
}

export function initializeViewProgramPage(options: InitializeViewProgramPageOptions) {
  theLevel = options.level;
  theLanguage = options.lang;

  // We need to enable the main editor for the program page as well
  const dir = $('body').attr('dir');
  theGlobalEditor = editorCreator.initializeEditorWithGutter($('#editor'), EditorType.MAIN, dir);
  attachMainEditorEvents(theGlobalEditor);
  theGlobalEditor.contents = options.code;
  initializeDebugger({
    editor: theGlobalEditor,
    level: theLevel,
    language: theLanguage,
    keywordLanguage: theKeywordLanguage,
  });
}

export function initializeHighlightedCodeBlocks(where: Element, initializeAll?: boolean) {
  const dir = $("body").attr("dir");
  initializeParsons();
  // Any code blocks we find inside 'turn-pre-into-ace' get turned into
  // read-only editors (for syntax highlighting)
  for (const container of $(where).find('.turn-pre-into-ace').get()) {
    for (const preview of $(container).find('pre').get()) {
      $(preview)
        .addClass('relative text-lg rounded overflow-x-hidden')
        // We set the language of the editor to the current keyword_language -> needed when copying to main editor
        .attr('data-lang', theKeywordLanguage);
      // If the request comes from HTMX initialize all directly
        if (initializeAll) {
          convertPreviewToEditor(preview, container, dir)
        } else {
        // Only turn into an editor if the editor scrolls into view
        // Otherwise, the teacher manual Frequent Mistakes page is SUPER SLOW to load.
        onElementBecomesVisible(preview, () => {
          convertPreviewToEditor(preview, container, dir)
        });
      }
    }
  }
}

function convertPreviewToEditor(preview: HTMLPreElement, container: HTMLElement, dir?: string) {
  const codeNode = preview.querySelector('code')
  let code: string;
  // In case it has a child <code> node
  if (codeNode) {
    codeNode.hidden = true
    code = codeNode.innerText
  } else {
    code = preview.textContent || "";
    preview.textContent = "";
  }

  // Create this example editor
  const exampleEditor = editorCreator.initializeReadOnlyEditor(preview, dir);
  // Strip trailing newline, it renders better
  exampleEditor.contents = code;
  exampleEditor.contents = exampleEditor.contents.trimEnd();
  // And add an overlay button to the editor if requested via a show-copy-button class, either
  // on the <pre> itself OR on the element that has the '.turn-pre-into-ace' class.
  if ($(preview).hasClass('show-copy-button') || $(container).hasClass('show-copy-button')) {
    const adventure = container.closest('[data-tabtarget]')?.getAttribute('data-tabtarget');
    const buttonContainer = $('<div>').addClass('absolute ltr:right-0 rtl:left-0 top-0 mx-1 mt-1').appendTo(preview);
    let symbol = "⇥";
    if (dir === "rtl") {
      symbol = "⇤";
    }
    $('<button>').css({ fontFamily: 'sans-serif' }).addClass('yellow-btn').attr('data-cy', `paste_example_code_${adventure}`).text(symbol).appendTo(buttonContainer).click(function() {
      if (!theGlobalEditor?.isReadOnly) {
        theGlobalEditor.contents = exampleEditor.contents + '\n';
      }
      update_view("main_editor_keyword_selector", <string>$(preview).attr('data-lang'));
      stopit();
      clearOutput();
    });
  }

  // Try to find the level for this code block. We first look at the 'level'
  // attribute on the <pre> element itself.  This is to preserve legacy
  // behavior, I'm not sure where this is still used. The modern way is to look
  // for 'data-level' attributes on the element itself and any containing element.
  // Same for 'lang' and 'data-lang'.
  const levelStr = $(preview).attr('level') ?? $(preview).closest('[data-level]').attr('data-level');
  const kwlang = $(preview).attr('lang') ?? $(preview).closest('[data-kwlang]').attr('data-kwlang');
  if (levelStr) {
    const level = parseInt(levelStr, 10);
    exampleEditor.setHighlighterForLevel(level, kwlang ?? 'en');
  }
}

export function getHighlighter(level: number) {
  return `ace/mode/level${level}`;
}

export function stopit() {
  // We bucket-fix stop the current program by setting the run limit to 1ms
  Sk.execLimit = 1;
  clearTimeouts();
  $('#stopit').hide();
  $('#runit').show();
  $('#ask_modal').hide();
  document.onkeydown = null;
  $('#keybinding_modal').hide();
  $('#sleep_modal').hide();

  if (sleepRunning) {
    sleepRunning = false;
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
  const buttonsDiv = $('#dynamic_buttons');
  buttonsDiv.empty();
  buttonsDiv.hide();
}

export async function runit(level: number, lang: string, raw: boolean, disabled_prompt: string, run_type: "run" | "debug" | "continue", cb: () => void) {
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

  // We set the run limit to 1ms -> make sure that the previous programs stops (if there is any)
  Sk.execLimit = 1;
  $('#runit').hide();
  $('#stopit').show();
  $('#save_files_container').hide();

  if (run_type !== 'continue') {
    clearOutput();
  }

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
    // console.log('Original program:\n', code);

    const adventure = theAdventures[adventureName];
    let program_data;

    if (run_type === 'run' || run_type === 'debug') {
      try {
        cancelPendingAutomaticSave();
        let data = {
          level: `${level}`,
          code: code,
          lang: lang,
          skip_faulty: false,
          is_debug: run_type === 'debug',
          read_aloud : !!$('#speak_dropdown').val(),
          adventure_name: adventureName,
          short_name: adventure ? adventure.short_name : undefined,
          raw: raw,

          // Save under an existing id if this field is set
          program_id: isServerSaveInfo(adventure?.save_info) ? adventure.save_info.id : undefined,
          save_name: saveNameFromInput(),
        };

        let response = await postJson('/parse', data);
        program_data = response;
        console.log('Response', response);
        if (response.Warning && $('#editor').is(":visible")) {
          //storeFixedCode(response, level);
          error.showWarning(response.Warning);
        }


        if (adventure && response.save_info) {
          adventure.save_info = response.save_info;
          adventure.editor_contents = code;
        }

        if (response.Error) {
          error.show("", response.Error);
          if (response.Location && response.Location[0] != "?") {
            //storeFixedCode(response, level);
            // Location can be either [row, col] or just [row].
            theGlobalEditor.highlightError(response.Location[0], response.Location[1]);
          }
          $('#stopit').hide();
          $('#runit').show();
          return;
        }
      } catch (e: any) {
        console.error(e);
        if (e.internetError) {
          error.show(ClientMessages['Connection_error'], ClientMessages['CheckInternet']);
        } else {
          error.show(ClientMessages['Other_error'], ClientMessages['ServerError']);
        }
      }
    } else {
      program_data = theGlobalDebugger.get_program_data();
    }

    runPythonProgram(program_data.Code, program_data.source_map, program_data.has_turtle, program_data.has_pressed, program_data.has_sleep, program_data.has_clear, program_data.has_music, program_data.Warning, program_data.variables, program_data.is_modified ,cb, run_type).catch(function(err: any) {
      // The err is null if we don't understand it -> don't show anything
      if (err != null) {
        error.show(ClientMessages['Execute_error'], err.message);
        reportClientError(level, code, err.message);
      }
    });


  } catch (e: any) {
    modal.notifyError(e.responseText);
  }
}

export async function saveMachineFiles() {
  const response = await postJson('/generate_machine_files', {
    level: theLevel,
    code: get_active_and_trimmed_code(),
    lang: theLanguage,
  });

  if (response.filename) {
    // Download the file
    window.location.replace('/download_machine_files/' + response.filename);
  }
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
  const lines = theGlobalEditor.contents.split('\n')
  if (lines[lines.length-1] !== '') {
    theGlobalEditor.contents += '\n' + exampleCode;
  } else {
    theGlobalEditor.contents += exampleCode;
  }
}

export function viewProgramLink(programId: string) {
  return window.location.origin + '/hedy/' + programId + '/view';
}

function updateProgramCount() {
  const programCountDiv = $('#program_count');
  const countText = programCountDiv.text();
  const regex = /(\d+)/;
  const match = countText.match(regex);

  if (match && match.length > 0) {
    const currentCount = parseInt(match[0]);
    const newCount = currentCount - 1;
    const newText = countText.replace(regex, newCount.toString());
    programCountDiv.text(newText);
  }
}

function updateSelectOptions(selectName: string) {
  let optionsArray: string[] = [];
  const select = $(`select[name='${selectName}']`);

  // grabs all the levels and names from the remaining adventures
  $(`[id="program_${selectName}"]`).each(function() {
      const text = $(this).text().trim();
        if (selectName == 'level'){
          const number = text.match(/\d+/)
          if (number && !optionsArray.includes(number[0])) {
            optionsArray.push(number[0]);
          }
        } else if (!optionsArray.includes(text)){
          optionsArray.push(text);
          }
  });

  if (selectName == 'level'){
    optionsArray.sort();
  }
  // grabs the -- level -- or -- adventure -- from the options
  const firstOption = select.find('option:first').text().trim();
  optionsArray.unshift(firstOption);

  select.empty();
  optionsArray.forEach(optionText => {
    const option = $('<option></option>').text(optionText);
    select.append(option);
  });
}

export async function delete_program(id: string, prompt: string) {
  await modal.confirmP(prompt);
  await tryCatchPopup(async () => {
    $('#program_' + id).remove();
    // only shows the remaining levels and programs in the options
    updateSelectOptions('level');
    updateSelectOptions('adventure');
    // this function decreases the total programs saved
    updateProgramCount();
    const response = await postJson('/programs/delete', { id });

    // issue request on the Bar component.
    modal.notifySuccess(response.message);
  });
}

function set_favourite(id: string, set: boolean) {
    $('.favourite_program_container').removeClass('text-yellow-400');
    $('.favourite_program_container').addClass('text-white');
    $('.favourite_program_container').attr("data-starred", "false");

    if (set) {
        $('#favourite_program_container_' + id).removeClass('text-white');
        $('#favourite_program_container_' + id).addClass('text-yellow-400');
    }
    $('#favourite_program_container_' + id).attr("data-starred", JSON.stringify(set));
}

export async function set_favourite_program(id: string, promptSet: string, promptUnset: string) {
  let set = JSON.parse($('#favourite_program_container_' + id).attr("data-starred")?.toLowerCase() || "");
  await modal.confirmP(set ? promptUnset : promptSet);
  await tryCatchPopup(async () => {
    const response = await postJson('/programs/set_favourite', { id, set: !set });
    // TODO: response with 200, assumed.
    set_favourite(id, !set)
    modal.notifySuccess(response.message);
  });
}

function change_to_submitted (id: string) {
    // Index is a front-end unique given to each program container and children
    // This value enables us to remove, hide or show specific element without connecting to the server (again)
    $('#non_submitted_button_container_' + id).remove();
    $('#submitted_button_container_' + id).show();
    $('#submitted_header_' + id).show();
    $('#program_' + id).removeClass("border-orange-400");
    $('#program_' + id).addClass("border-gray-400 bg-gray-400");
}

export function submit_program (id: string) {
  tryCatchPopup(async () => {
    await postJson('/programs/submit', { id });
    change_to_submitted(id);
  });
}

function change_to_unsubmitted () {
    $('#unsubmit-program-button').hide();
    $('#submitted-program-title').hide();
    $('#submitted-program-details').hide();
}

export async function unsubmit_program (id: string, prompt: string) {
  await modal.confirmP(prompt);
  tryCatchPopup(async () => {
    const response = await postJson('/programs/unsubmit', { id });
    modal.notifySuccess(response.message);
    change_to_unsubmitted();
  });
}

export function report_program(prompt: string, id: string) {
  tryCatchPopup(async () => {
    await modal.confirmP(prompt);
    const response = await postJson('/programs/report', { id });
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
  postJson('/report_error', {
    level: `${level}`,
    code: code,
    page: window.location.href,
    client_error: client_error,
  });
}

window.onerror = function reportClientException(message, source, line_number, column_number, error) {
  postJson('/client_exception', {
    message: message,
    source: source,
    line_number: line_number,
    column_number: column_number,
    error: error,
    url: window.location.href,
    user_agent: navigator.userAgent,
  });
}

export function runPythonProgram(this: any, code: string, sourceMap: any, hasTurtle: boolean, hasPressed: boolean, hasSleep: number[], hasClear: boolean, hasMusic: boolean, hasWarnings: boolean, variables: any, isModified: boolean, cb: () => void, run_type: "run" | "debug" | "continue") {
  // If we are in the Parsons problem -> use a different output
  let outputDiv = $('#output');
  let skip_faulty_found_errors = false;
  let warning_box_shown = false;

  if (sourceMap){
    theGlobalSourcemap = sourceMap;
    // We loop through the mappings and underline a mapping if it contains an error
    for (const index in sourceMap) {
      const map = sourceMap[index];

      const range = {
        startLine: map.hedy_range.from_line,
        startColumn: map.hedy_range.from_column,
        endLine: map.hedy_range.to_line,
        endColumn: map.hedy_range.to_column
      }

      if (map.error != null) {
        skip_faulty_found_errors = true;
        theGlobalEditor.setIncorrectLine(range, Number(index));
      }

      // Only show the warning box for the first error shown
      if (skip_faulty_found_errors && !warning_box_shown) {
        error.showFadingWarning(ClientMessages['Errors_found']);
        warning_box_shown = true;
      }
    }
  }

  let skulptExternalLibraries:{[index: string]:any} = {
      './extensions.js': {
        path: theStaticRoot + "/vendor/skulpt-stdlib-extensions.js",
      },
  };

  Sk.pre = "output";
  const turtleConfig = (Sk.TurtleGraphics || (Sk.TurtleGraphics = {}));
  turtleConfig.target = 'turtlecanvas';
  // If the adventures are not shown  -> increase height of turtleConfig
  if ($('#adventures_tab').is(":hidden")) {
      turtleConfig.height = 600;
      turtleConfig.worldHeight = 600;
  } else if ($('#turtlecanvas').attr("raw") == 'yes'){
      turtleConfig.height = 150;
      turtleConfig.worldHeight = 250;
  }
  else {
      turtleConfig.height = 250;
      turtleConfig.worldHeight = 250;
  }
  // Always set the width to output panel width -> match the UI
  turtleConfig.width = outputDiv.width();
  turtleConfig.worldWidth = outputDiv.width();

  let code_prefix = normal_prefix;

  if (!hasTurtle) {
    // There might still be a visible turtle panel. If the new program does not use the Turtle,
    // remove it (by clearing the '#turtlecanvas' div)
    $('#turtlecanvas').empty();
  }

  if (hasTurtle) {
    code_prefix += turtle_prefix;
    $('#turtlecanvas').show();
  }

  if (hasPressed) {
    code_prefix += pressed_prefix;
  }

  if (hasMusic) {
    code_prefix += music_prefix;
    $('#turtlecanvas').show();
  }

  if (hasSleep && theLevel < 7) {
    function executeWithDelay(index: number) {
      return new Promise((resolve, reject) => {
        if (index >= hasSleep.length) {
          resolve(reject);
          return;
        }

        const sleepTime = hasSleep[index];
        if (sleepTime) {
          $('#sleep_modal').show();
          sleepRunning = true;
          setTimeout(() => {
            $('#sleep_modal').hide();
            sleepRunning = false;
            setTimeout(() => {
              resolve(reject);
            }, 100);
          }, (sleepTime * 1000) - 100);
        } else {
          setTimeout(() => {
            resolve(reject);
          }, 100);
        }
      });
    }

    async function executeAllDelays() {
      for (let i = 0; i < hasSleep.length; i++) {
        await executeWithDelay(i);
      }
    }
    executeAllDelays()
  }

  code = code_prefix + code;

  (Sk as any).builtins.play = new Sk.builtin.func((notes:any) => {
    //const now = Tone.now()
    const note_name = notes.v;

    //play note_name for the duration of an 16th note
    synth.triggerAttackRelease(note_name, "16n");

  });
  if (run_type === "run") {
    $('#variable_list').empty();
    toggleVariableView();
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
        $('#runit').show();
        if (Sk.execLimit != 1) {
          return ClientMessages ['Program_too_long'];
        } else {
          return null;
        }
      },
      // We want to make the timeout function a bit more sophisticated that simply setting a value
      // In levels 1-6 users are unable to create loops and programs with a lot of lines are caught server-sided
      // So: a very large limit in these levels, keep the limit on other ones.
      execLimit: (function () {
        const level = theLevel;
        if (hasTurtle || hasPressed || hasMusic) {
          // We don't want a timeout when using the turtle, if_pressed or music -> just set one for 10 minutes
          return (6000000);
        }
        if (level < 7) {
          // Also on a level < 7 (as we don't support loops yet), a timeout is redundant -> just set one for 5 minutes
          return (3000000);
        }
        // Set a time-out of either 30 seconds when having a sleep and 10 seconds when not
        return ((hasSleep) ? 30000 : 10000);
      }) ()
    });

    const currentProgram: number = Number(sessionStorage.getItem('currentProgram') || 0) + 1;
    sessionStorage.setItem('currentProgram', currentProgram.toString());

    return Sk.misceval.asyncToPromise(() =>
      Sk.importMainWithBody("<stdin>", false, code, true), {
        "*": () => {
          // We don't do anything here...
        }
      },
      currentProgram
     ).then(function(_mod) {
      console.log('Program executed');
      const pythonVariables = Sk.globals;
      load_variables(pythonVariables);
      $('#stopit').hide();
      $('#runit').show();

      document.onkeydown = null;
      $('#keybinding_modal').hide();

      if (hasTurtle) {
        $('#save_files_container').show();
      }

      // Check if the program was correct but the output window is empty: Return a warning
      if ((!hasClear) && $('#output').is(':empty') && $('#turtlecanvas').is(':empty') && !hasMusic) {
        error.showWarning(ClientMessages['Empty_output']);
        return;
      }
      if (!hasWarnings && code !== last_code) {
          showSuccessMessage(isModified);
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

  } else if (run_type === "debug") {

    theGlobalDebugger = new Sk.Debugger('<stdin>', incrementDebugLine, stopDebug);
    theGlobalSourcemap = sourceMap;

    Sk.configure({
      output: outf,
      read: builtinRead,
      inputfun: inputFromInlineModal,
      inputfunTakesPrompt: true,
      __future__: Sk.python3,
      debugging: true,
      breakpoints: theGlobalDebugger.check_breakpoints.bind(theGlobalDebugger),
      execLimit: null
    });

    let lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
      // lines with dummy variable name are not meant to be shown to the user, skip them.
      if (lines[i].includes("# __BREAKPOINT__") && !lines[i].includes('x__x__x__x')) {
        // breakpoints are 1-indexed
        theGlobalDebugger.add_breakpoint('<stdin>.py', i + 1, '0', false);
      }
    }

    // Do not show success message if we found errors that we skipped
    if (!hasWarnings && code !== last_code && !skip_faulty_found_errors) {
        last_code = code;
    }

    theGlobalDebugger.set_code_starting_line(code_prefix.split('\n').length - 1);
    theGlobalDebugger.set_code_lines(code.split('\n'));
    theGlobalDebugger.set_program_data({
      Code: code,
      source_map: sourceMap,
      has_turtle: hasTurtle,
      has_clear: hasClear,
      has_music: hasMusic,
      Warning: hasWarnings,
      variables: variables
    });

    startDebug();

    return theGlobalDebugger.startDebugger(
      () => Sk.importMainWithBody("<stdin>", false, code, true),
      theGlobalDebugger
    ).then(
      function () {
        console.log('Program executed');

        $('#stopit').hide();
        $('#runit').show();

        stopDebug();

        document.onkeydown = null;
        $('#keybinding_modal').hide();

        if (hasTurtle) {
          $('#save_files_container').show();
        }

        if (cb) cb ();
      }
    ).catch(function(err: any) {
      const errorMessage = errorMessageFromSkulptError(err) || null;
      if (!errorMessage) {
        throw null;
      }
      throw new Error(errorMessage);
    });

  } else {
    // Disable continue button, until the current instruction is completed.
    // The button is enabled again in incrementDebugLine()
    document.getElementById('debug_continue')!.setAttribute('disabled', 'disabled');
    // maybe remove debug marker here
    return theGlobalDebugger.continueForward()
      .catch(function(err: any) {
        console.error(err)
        const errorMessage = errorMessageFromSkulptError(err) || null;
        if (!errorMessage) {
          throw null;
        }
        throw new Error(errorMessage);
    });
  }

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

      let request = new XMLHttpRequest();
      request.open("GET", tmpPath, false);
      request.send();

      if (request.status !== 200) {
        return void 0
      }

      return request.responseText
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
    document.onkeydown = null;
    $('#keybinding_modal').hide();

    return new Promise(function(ok) {
      askPromptOpen = true;

      const input = $('#ask_modal input[type="text"]');
      $('#ask_modal .caption').text(prompt);
      input.val('');
      input.attr('placeholder', prompt);
      speak(prompt)

      setTimeout(function() {
        input.focus();
      }, 0);
      $('#ask_modal form').one('submit', function(event) {
        askPromptOpen = false;
        event.preventDefault();
        $('#ask_modal').hide();

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
        $('#ask_modal').show();

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
  $('*[data-tabtarget="quiz"]').html ('<iframe id="quiz_iframe" class="w-full" title="Quiz" src="/quiz/start/' + level + '"></iframe>');
}

export async function store_parsons_attempt(order: Array<string>, correct: boolean) {
  try {
    await postJson('/store_parsons_order', {
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

export function get_active_and_trimmed_code() {
  theGlobalEditor.trimTrailingSpace();
  const storage = window.localStorage;
  const debugLine = storage.getItem("debugLine");
  return theGlobalEditor.getActiveContents(debugLine);
}

export function getEditorContents() {
  return theGlobalEditor.contents;
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

    const confettiButton = document.getElementById('confetti_button');
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
  let $modalEditor = $('#modal_editor');
  if ($modalEditor.length) {
    const dir = $('body').attr('dir');
    theModalEditor = editorCreator.initializeEditorWithGutter($modalEditor, EditorType.MODAL, dir);
  }
}

function showSuccessMessage(isModified: boolean){
  removeBulb();
  var allsuccessmessages = ClientMessages['Transpile_success'].split('\n');
  var randomnum: number = Math.floor(Math.random() * allsuccessmessages.length);
  success.show(allsuccessmessages[randomnum], isModified);
}

function createModal(level:number ){
  let editor = "<div id='modal_editor' class=\"w-full flex-1 text-lg rounded\" style='height:200px; width:50vw;'></div>".replace("{level}", level.toString());
  let title = ClientMessages['Program_repair'];
  modal.repair(editor, 0, title);
}

// Remove this function when enabling the new design
export function setDevelopersMode(event='click', enforceDevMode: boolean) {
  let enable: boolean = false;
  switch (event) {
    case 'load':
      const lastSelection = window.localStorage.getItem('developer_mode') === 'true';
      enable = enforceDevMode || lastSelection;
      $('#developers_toggle').prop('checked', enable);
      break;

    case 'click':
      // Toggled
      enable = $('#developers_toggle').prop('checked');
      break;
  }
  if (!enforceDevMode) window.localStorage.setItem('developer_mode', `${enable}`)
  toggleDevelopersMode(!!enforceDevMode)
}

// Remove this function when enabling the new design
function toggleDevelopersMode(enforceDevMode: boolean) {
  const enable = window.localStorage.getItem('developer_mode') === 'true' || enforceDevMode;
  // DevMode hides the tabs and makes resizable elements track the appropriate size.
  // (Driving from HTML attributes is more flexible on what gets resized, and avoids duplicating
  // size literals between HTML and JavaScript).
  $('#adventures_tab').toggle(!enable || currentTab === 'quiz' || currentTab === 'parsons');
  // this is for the new design, it needs to be removed once we ship it
  $('#adventures').toggle(!enable || currentTab === 'quiz' || currentTab === 'parsons');
  // Parsons dont need a fixed height
  if (currentTab === 'parsons') return

  $('[data-editorheight]').each((_, el) => {
    const heights = $(el).data('editorheight').split(',') as string[];
    $(el).css('height', heights[enable ? 1 : 0]);
  });
}

export function saveForTeacherTable(table: string) {
  let show_table = window.localStorage.getItem(table);
  window.localStorage.setItem(table, (show_table !== 'true').toString())
  const arrow = document.querySelector('#' + table + '_arrow') as HTMLElement;
  const table_ele = document.getElementById(table)!
  const show_label = document.getElementById(table + '_show')!
  const hide_label = document.getElementById(table + '_hide')!
  table_ele.classList.toggle('hidden')
  show_label.classList.toggle('hidden')
  hide_label.classList.toggle('hidden')
  arrow.classList.toggle('rotate-180');
}

export function getForTeacherTable(table: string) {
  let show_table = window.localStorage.getItem(table);
  const table_ele = document.getElementById(table)!
  const arrow = document.getElementById(table + '_arrow')!;
  const show_label = document.getElementById(table + '_show')!
  const hide_label = document.getElementById(table + '_hide')!

  table_ele.classList.toggle('hidden', show_table !== 'true');
  show_label.classList.toggle('hidden', show_table === 'true');
  hide_label.classList.toggle('hidden', show_table !== 'true');
  arrow.classList.toggle('rotate-180', show_table === 'true');
}

/**
 * Run a code block, show an error message if we catch an exception
 */
export async function tryCatchErrorBox(cb: () => void | Promise<void>) {
  try {
    return await cb();
  } catch (e: any) {
    console.log('Error', e);
    error.show("", e.message);
  }
}

export function toggle_keyword_language(current_lang: string, new_lang: string) {
  tryCatchErrorBox(async () => {
    const response = await postJson('/translate_keywords', {
      code: theGlobalEditor.contents,
      start_lang: current_lang,
      goal_lang: new_lang,
      level: theLevel,
    });
    if (response) {
      const code = response.code
      theGlobalEditor.contents = code;
      const saveName = saveNameFromInput();

      // save translated code to local storage
      // such that it can be fetched after reload
      localSave(currentTabLsKey(), { saveName, code });
      $('#editor').attr('data-lang', new_lang);

      // update the whole page (example codes)
      const hash = window.location.hash;
      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);
      urlParams.set('keyword_language', new_lang)
      window.location.search = urlParams.toString()
      window.open(hash, "_self");

      // if in iframe, reload the topper window level.
      if (window.top && !(window as any).Cypress) {
        window.top.location.reload();
      }

    }
  });
}

export function toggle_blur_code() {
  // Switch the both icons from hiding / showing
  $('.blur_toggle').toggle();

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
    const response = await postJson('/change_language', { lang });
    if (response) {
      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);

      if (lang === 'en' || urlParams.get("language") !== null) {
        urlParams.set("language", lang)
        urlParams.set('keyword_language', lang);
        window.location.search = urlParams.toString();
      } else {
        location.reload();
      }
    }
  });
}

function update_view(selector_container: string, new_lang: string) {
  $('#' + selector_container + ' > div').map(function() {
    if ($(this).attr('data-lang') == new_lang) {
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

export function hide_editor() {
  $('#fold_in_toggle_container').hide(); // remove once we get rid of old version
  $('#hide_editor').hide();
  $('#code_editor').addClass('lg:hidden block');
  $('#code_output').addClass('lg:col-span-2');
  $('#show_editor').show();
  $('#fold_out_toggle_container').show(); // remove once we get rid of old version
}

export function show_editor() {
  $('#fold_out_toggle_container').hide(); // remove once we get rid of old version
  $('#show_editor').hide();
  $('#code_editor').removeClass('lg:hidden block');
  $('#code_output').removeClass('lg:col-span-2');
  $('#hide_editor').show();
  $('#fold_in_toggle_container').show(); // remove once we get rid of old version
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
  var iframe : any = document.getElementById(`level_${level}_slides`)!;
  iframe.setAttribute('src',`/slides/${level}`);
  $(`#level_${level}_slides`).on('load', function (){
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
  const isParsonsTab = currentTab === 'parsons'
  const isCodeTab = !(currentTab === 'quiz' || isParsonsTab);
 // .toggle(bool) sets visibility based on the boolean

  // Explanation area is visible for non-code tabs, or when we are NOT in developer's mode
  $('#adventures_tab').toggle(!(isCodeTab && $('#developers_toggle').is(":checked")));
  $('#developers_toggle_container').toggle(isCodeTab);
  // this is for the new design, it needs to be removed once we ship it
  $('#adventures').toggle(true);
  $('#level_header input').toggle(isCodeTab);
  $('#parsons_code_container').toggle(currentTab === 'parsons');
  $('#editor_area').toggle(isCodeTab || currentTab === 'parsons');
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
    // Remove once we get rid of the old version
    $('#hand_in_button')
      .toggleClass('active-bluebar-btn', isSubmitted);

    // Show <...data-view="if-submitted"> only if we have a public url
    $('[data-view="if-submitted"]').toggle(isSubmitted);
    $('[data-view="if-not-submitted"]').toggle(!isSubmitted);
    const icon = document.querySelector(`*[data-tab="${adventure.short_name}"][data-level="${theLevel}"] > div > i[data-status-icon]`);
    icon?.classList.toggle('fa-paper-plane', isSubmitted && !icon?.classList.contains('fa-circle-check'));
    const hand_in_btn = document.getElementById('hand_in');
    if (isSubmitted) {
      hand_in_btn?.setAttribute('disabled', 'disabled');
    } else {
      hand_in_btn?.removeAttribute('disabled');
    }
    theGlobalEditor.isReadOnly = isSubmitted;
    // All of these are for the buttons added in the new version of the code-page
    $('#program_name_container').show()
    $('#share_program_button').show()
    $('#read_outloud_button_container').show()
    $('#cheatsheet_dropdown_container').show()
    $('#commands_dropdown_container').show()
    $('#hand_in_button').show()
  }
  if (currentTab === 'parsons'){
    $('#share_program_button').hide()
    $('#read_outloud_button_container').hide()
    $('#cheatsheet_dropdown_container').hide()
    $('#commands_dropdown_container').show()
    $('#hand_in_button').hide()
    $('#clear').hide()
  }
  if (currentTab === 'quiz'){
    $('#share_program_button').hide()
    $('#read_outloud_button_container').hide()
    $('#cheatsheet_dropdown_container').hide()
    $('#commands_dropdown_container').hide()
    $('#hand_in_button').hide()
  }
}

/**
 * Load parsons and update the editors height accordingly
 */
function configureParson() {
  loadParsonsExercise(theLevel, 1);
  // parsons could have 5 lines to arrange which requires more space, so remove the fixed height from the editor
  document.getElementById('code_editor')!.style.height = '100%'
  document.getElementById('code_output')!.style.height = '100%'
}

/**
 * After switching tabs, show/hide elements
 */
function reconfigurePageBasedOnTab(isTryItPage?: boolean, enforceDevMode?: boolean) {
  resetWindow();
  updatePageElements();

  if (!isTryItPage) {
    if (currentTab === 'parsons') {
      configureParson();
      show_editor();
      $('#fold_in_toggle_container').hide();
    } else {
      toggleDevelopersMode(!!enforceDevMode);
    }
    $('#fold_in_toggle_container').show();
  }

  const adventure = theAdventures[currentTab];
  if (adventure) {
    $ ('#program_name').val(adventure.save_name);
    theGlobalEditor.contents = adventure.editor_contents;
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
      // Async-safe copy of current tab
      const adventure = theAdventures[currentTab];

      tryCatchPopup(async () => {
        await saveIfNecessary();

        const saveInfo = isServerSaveInfo(adventure?.save_info) ? adventure?.save_info : undefined;
        if (!saveInfo) {
          throw new Error('This program does not have an id');
        }
        await postNoResponse(`/programs/share/${saveInfo.id}`, {})
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
        const response = await postJson('/programs/submit', {
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
  const programChanged = theGlobalEditor.contents !== adventure.editor_contents;
  const nameChanged = $('#program_name').val() !== adventure.save_name;
  const localStorageCanBeSavedToServer = theUserIsLoggedIn && adventure.save_info === 'local-storage';
  const isUnchangeable = isServerSaveInfo(adventure.save_info) ? adventure.save_info.submitted : false;

  // Do not autosave the program if the size is very small compared to the previous
  // save. This protects against accidental `Ctrl-A, hit a key` and everything is gone. Clicking the
  // "Run" button will always save regardless of size.
  const wasSavedBefore = adventure.save_info !== undefined;
  const suspiciouslySmallFraction = 0.5;
  const programSuspiciouslyShrunk = wasSavedBefore && theGlobalEditor.contents.length < adventure.editor_contents.length * suspiciouslySmallFraction;

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


let autoSaveEnabled = true;

function disableAutomaticSaving() {
  autoSaveEnabled = false;
}

async function saveIfNecessary() {
  if (!autoSaveEnabled) {
    return;
  }

  // Async-safe copy of current tab
  const adventureName = currentTab;
  const adventure = theAdventures[adventureName];
  if (!programNeedsSaving(adventureName) || !adventure) {
    return;
  }

  console.info('Saving program automatically...');

  const code = theGlobalEditor.contents;
  const saveName = saveNameFromInput();


  if (theUserIsLoggedIn && saveName) {
    const saveInfo = isServerSaveInfo(adventure.save_info) ? adventure.save_info : undefined;
    const response = await postJson('/programs', {
      level: theLevel,
      lang:  theLanguage,
      name:  saveName,
      code:  code,
      adventure_name: adventureName,
      program_id: saveInfo?.id,
      // We pass 'public' in here to save the backend a lookup
      share: saveInfo?.public,
      short_name: adventure.short_name,
    });

    // Record that we saved successfully
    adventure.editor_contents = code;
    if (response.save_info) {
      adventure.save_info = response.save_info;
    }
    localDelete(currentTabLsKey());
  } else {
    localSave(currentTabLsKey(), { saveName, code });
    adventure.editor_contents = code;
  }
}

function currentTabLsKey() {
  return `save-${currentTab}-${theLevel}`;
}

export function goToLevel(level: any) {
  const hash = window.location.hash
  let newPath = window.location.pathname.replace(/\/\d+/, `/${level}`);
  if (!newPath.includes(level)) {
    newPath = window.location.pathname + `/${level}`
  }
  window.location.pathname = newPath
  window.location.hash = hash
}

export function emptyEditor() {
  theGlobalEditor.contents = ""
}


export function open_index_pane(e: Event) {
  const target = e.target as HTMLElement;
  const button = target.closest('button');
  if (!button) return;
  const level = button.id.split('_')[1];
  const pane = document.getElementById(`level_${level}_pane`);
  if (!pane) return;
  // If this pane is already open, close it
  // Otherwise, close all other panes and open this one
  if (pane.classList.contains('sliding-content-open')) {
    pane.classList.remove('sliding-content-open');
    pane.classList.add('sliding-content-closed');
    document.getElementById(`level_${level}_arrow`)?.classList.toggle('rotate-180');
  } else {
    document.querySelectorAll('.sliding-content-open').forEach((el) => {
      el.classList.remove('sliding-content-open');
      el.classList.add('sliding-content-closed');
      const level = el.id.split('_')[1];
      const arrow = document.getElementById(`level_${level}_arrow`);
      arrow?.classList.toggle('rotate-180');
    });
    // Open the selected pane
    pane.classList.remove('sliding-content-closed');
    pane.classList.add('sliding-content-open');
    const arrow = document.getElementById(`level_${level}_arrow`);
    arrow?.classList.toggle('rotate-180');
    // sleep for 400 miliseconds to settle animations
    setTimeout(() => {
      pane.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      const opened_level_button = pane?.previousElementSibling
      opened_level_button?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 400);
  }
}

export function open_index_dropdown(e: Event) {
  $('#dropdown-level').slideToggle('medium');
  document.getElementById('dropdown_index_arrow')?.classList.toggle('rotate-180');
  const target = e.target as HTMLElement;
  const button = target.closest('button');
  if (!button) return;
  const opened_pane = document.querySelector('.sliding-content-open');
  const opened_level_button = opened_pane?.previousElementSibling
  opened_level_button?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}