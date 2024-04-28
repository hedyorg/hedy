import { ClientMessages } from './client-messages';
import { modal, error, success, tryCatchPopup } from './modal';
import JSZip from "jszip";
import * as Tone from 'tone'
import { Tabs } from './tabs';
import { MessageKey } from './message-translations';
import { turtle_prefix, pressed_prefix, normal_prefix, music_prefix } from './pythonPrefixes'
import { Achievement, Adventure, isServerSaveInfo, ServerSaveInfo } from './types';
import { startIntroTutorial } from './tutorials/tutorial';
import { get_parsons_code, initializeParsons, loadParsonsExercise } from './parsons';
import { checkNow, onElementBecomesVisible } from './browser-helpers/on-element-becomes-visible';
import {
    incrementDebugLine,
    initializeDebugger,
    load_variables,
    startDebug
} from './debugging';
import { localDelete, localLoad, localSave } from './local';
import { initializeLoginLinks } from './auth';
import { postJson, postNoResponse } from './comm';
import { LocalSaveWarning } from './local-save-warning';
import { HedyEditor, EditorType } from './editor';
import { stopDebug } from "./debugging";
import { HedyCodeMirrorEditorCreator } from './cm-editor';
import { initializeTranslation } from './lezer-parsers/tokens';
import { initializeActivity } from './user-activity';

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
      $(".dropdown-menu").slideUp("medium");
      $(".cheatsheet-menu").slideUp("medium");
      return;
    }

    const allDropdowns = $('.dropdown-menu')
    for (const dd of allDropdowns) {
      // find the closest dropdown button (element) that initiated the event
      const c = $(dd).closest('.dropdown')[0]
      // if the click event target is not within or close to the container, slide up the dropdown menu
      if (!$(event.target).closest(c).length) {
        $(dd).slideUp('fast');
      }
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

  initializeActivity();
}

export interface InitializeCodePageOptions {
  readonly page: 'code';
  readonly level: number;
  readonly lang: string;
  readonly adventures: Adventure[];
  readonly start_tutorial?: boolean;
  readonly initial_tab: string;
  readonly current_user_name?: string;
  readonly suppress_save_and_load_for_slides?: boolean;
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
    initializeTranslation({keywordLanguage: theKeywordLanguage, level: theLevel});
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

    if (!options.suppress_save_and_load_for_slides) {
      // Load initial code from local storage, if available
      const programFromLs = localLoad(currentTabLsKey());
      // if we are in raw (used in slides) we don't want to load from local storage, we always want to show startcode
      if (programFromLs && adventure) {
        adventure.editor_contents = programFromLs.code;
        adventure.save_name = programFromLs.saveName;
        adventure.save_info = 'local-storage';
      }
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

  if (options.suppress_save_and_load_for_slides) {
    disableAutomaticSaving();
  }

  // Save if user navigates away
  window.addEventListener('beforeunload', () => saveIfNecessary(), { capture: true });

  // Save if program name is changed
  $('#program_name').on('blur', () => saveIfNecessary());
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
    if ($('#ask-modal').is(':visible')) $('#inline-modal').hide();
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
  const dir = $("body").attr("dir");
  theGlobalEditor = editorCreator.initializeEditorWithGutter($('#editor'), EditorType.MAIN, dir);
  initializeTranslation({
    keywordLanguage: options.lang,
    level: options.level
  });
  attachMainEditorEvents(theGlobalEditor);
  theGlobalEditor.contents = options.code;
  initializeDebugger({
    editor: theGlobalEditor,
    level: theLevel,
    language: theLanguage,
    keywordLanguage: theKeywordLanguage,
  });
}

export function initializeHighlightedCodeBlocks(where: Element) {
  const dir = $("body").attr("dir");
  initializeParsons();
  if (theLevel) {
    initializeTranslation({
      keywordLanguage: theKeywordLanguage,
      level: theLevel
    })
  }
  // Any code blocks we find inside 'turn-pre-into-ace' get turned into
  // read-only editors (for syntax highlighting)
  for (const container of $(where).find('.turn-pre-into-ace').get()) {
    for (const preview of $(container).find('pre').get()) {
      $(preview)
        .addClass('relative text-lg rounded overflow-x-hidden')
        // We set the language of the editor to the current keyword_language -> needed when copying to main editor
        .attr('lang', theKeywordLanguage);

      // Only turn into an editor if the editor scrolls into view
      // Otherwise, the teacher manual Frequent Mistakes page is SUPER SLOW to load.
      onElementBecomesVisible(preview, () => {
        const codeNode = preview.querySelector('code')
        let code: string;
        // In case it has a child <code> node
        if(codeNode) {
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
          const buttonContainer = $('<div>').addClass('absolute ltr:right-0 rtl:left-0 top-0 mx-1 mt-1').appendTo(preview);
          let symbol = "⇥";
          if (dir === "rtl") {
            symbol = "⇤";
          }
          const adventure = container.getAttribute('data-tabtarget')
          $('<button>').css({ fontFamily: 'sans-serif' }).addClass('yellow-btn').attr('data-cy', `paste-example-code-${adventure}`).text(symbol).appendTo(buttonContainer).click(function() {
            if (!theGlobalEditor?.isReadOnly) {
              theGlobalEditor.contents = exampleEditor.contents + '\n';
            }
            update_view("main_editor_keyword_selector", <string>$(preview).attr('lang'));
            stopit();
            clearOutput();
          });
        }
        const levelStr = $(preview).attr('level');
        const lang = $(preview).attr('lang');
        if (levelStr && lang) {
          initializeTranslation({
            keywordLanguage: lang,
            level: parseInt(levelStr, 10),
          })
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
  // We bucket-fix stop the current program by setting the run limit to 1ms
  Sk.execLimit = 1;
  clearTimeouts();
  $('#stopit').hide();
  $('#runit').show();
  $('#ask-modal').hide();
  document.onkeydown = null;
  $('#keybinding-modal').hide();
  $('#sleep-modal').hide();
  
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
  const buttonsDiv = $('#dynamic-buttons');
  buttonsDiv.empty();
  buttonsDiv.hide();
}

export async function runit(level: number, lang: string, raw: boolean, disabled_prompt: string, run_type: "run" | "debug" | "continue", cb: () => void) {
  // Copy 'currentTab' into a variable, so that our event handlers don't mess up
  // if the user changes tabs while we're waiting for a response
  const adventureName = currentTab;

     if (run_type === 'debug' || run_type === 'continue') {
          if($('#variables #variable-list li').length == 0){
            $('#variable_button').hide();
            $('#variables').hide();
            $('#variables-expand').hide();
          }
          else{
            $('#variable_button').show();
            $('#variables').show();
            $('#variables-expand').show();
          }
          setTimeout(() => {
                $('#variables-expand').hide();
                $('#variables').hide();
          }, 5000);

     }

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
  $('#saveFilesContainer').hide();

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
          tutorial: $('#code_output').hasClass("z-40"), // if so -> tutorial mode
          read_aloud : !!$('#speak_dropdown').val(),
          adventure_name: adventureName,
          short_name: adventure ? adventure.short_name : undefined,
          raw: raw,

          // Save under an existing id if this field is set
          program_id: isServerSaveInfo(adventure?.save_info) ? adventure.save_info.id : undefined,
          save_name: saveNameFromInput(),
        };

        let response = await postJsonWithAchievements('/parse', data);

        program_data = response;
        console.log('Response', response);

        if (response.Warning && $('#editor').is(":visible")) {
          //storeFixedCode(response, level);
          error.showWarning(ClientMessages['Transpile_warning'], response.Warning);
        }

        showAchievements(response.achievements, false, "");
        if (adventure && response.save_info) {
          adventure.save_info = response.save_info;
          adventure.editor_contents = code;
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

    runPythonProgram(program_data.Code, program_data.source_map, program_data.has_turtle, program_data.has_pressed, program_data.has_sleep, program_data.has_clear, program_data.has_music, program_data.Warning, program_data.is_modified ,cb, run_type).catch(function(err: any) {
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
  const lines = theGlobalEditor.contents.split('\n')
  if (lines[lines.length-1] !== '') {
    theGlobalEditor.contents += '\n' + exampleCode;
  } else {
    theGlobalEditor.contents += exampleCode;
  }
  //As the commands try-it buttons only contain english code -> make sure the selected language is english
  if (!($('#editor').attr('lang') == 'en')) {
      $('#editor').attr('lang', 'en');
      update_view("main_editor_keyword_selector", "en");
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
      console.log(optionsArray);
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
    const response = await postJsonWithAchievements('/programs/delete', { id });
    showAchievements(response.achievement, true, "");
    // issue request on the Bar component.
    console.log("resp", response)
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
    const response = await postJsonWithAchievements('/programs/set_favourite', { id, set: !set });
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
    await postJsonWithAchievements('/programs/submit', { id });
    change_to_submitted(id);
  });
}

export function unsubmit_program (id: string) {
  tryCatchPopup(async () => {
    const response = await postJsonWithAchievements('/programs/unsubmit', { id });
    modal.notifySuccess(response.message);
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

export function runPythonProgram(this: any, code: string, sourceMap: any, hasTurtle: boolean, hasPressed: boolean, hasSleep: number[], hasClear: boolean, hasMusic: boolean, hasWarnings: boolean, isModified: boolean, cb: () => void, run_type: "run" | "debug" | "continue") {
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
        error.showFadingWarning(ClientMessages['Execute_error'], ClientMessages['Errors_found']);
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

  if (!hasTurtle) {
    // There might still be a visible turtle panel. If the new program does not use the Turtle,
    // remove it (by clearing the '#turtlecanvas' div)
    $('#turtlecanvas').empty();
  }

  if (hasTurtle) {
    code_prefix += turtle_prefix;
    resetTurtleTarget();
    $('#turtlecanvas').show();
  }

  if (hasPressed) {
    code_prefix += pressed_prefix;
  }

  if (hasMusic) {
    code_prefix += music_prefix;
    $('#turtlecanvas').show();
  }

  if (hasSleep) {
    function executeWithDelay(index: number) {
      return new Promise((resolve, reject) => {
        if (index >= hasSleep.length) {
          resolve(reject);
          return;
        }

        const sleepTime = hasSleep[index];
        if (sleepTime) {
          $('#sleep-modal').show();
          sleepRunning = true;
          setTimeout(() => {
            $('#sleep-modal').hide();
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
          pushAchievement("hedy_hacking");
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
        if (hasTurtle || hasMusic) {
          // We don't want a timeout when using the turtle or music -> just set one for 10 minutes
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
      $('#keybinding-modal').hide();

      if (hasTurtle) {
        $('#saveFilesContainer').show();
      }

      // Check if the program was correct but the output window is empty: Return a warning
      if ((!hasClear) && $('#output').is(':empty') && $('#turtlecanvas').is(':empty')) {
        pushAchievement("error_or_empty");
        error.showWarning(ClientMessages['Transpile_warning'], ClientMessages['Empty_output']);
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
      Warning: hasWarnings
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
        $('#keybinding-modal').hide();

        if (hasTurtle) {
          $('#saveFilesContainer').show();
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
    $('#keybinding-modal').hide();

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
    const output = $('#output');
    output.show();
  }
  const variablesExpand = $('#variables-expand');
  if (variablesExpand.is(":hidden")) {
    variablesExpand.show();
    $("#variables").trigger("click")
  }
  else {
    variablesExpand.hide();
  }
}

export async function store_parsons_attempt(order: Array<string>, correct: boolean) {
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

export function get_active_and_trimmed_code() {
  theGlobalEditor.trimTrailingSpace();
  const storage = window.localStorage;
  const debugLine = storage.getItem("debugLine");
  return theGlobalEditor.getActiveContents(debugLine);
}

export function getEditorContents() {
  return theGlobalEditor.contents;
}

export function expandVariableView() {
  const openVariables = $('#open-variables');
  openVariables.hide();
  const closeVariables = $('#close-variables');
  if(closeVariables.hasClass('hidden')){
      closeVariables.removeClass('hidden');
  }

  const variables = $('#variables');
  variables.removeClass('h-24');
  variables.addClass('h-full');
  const output = $('#output');
  output.hide();
}

export function closeVariableView() {
  const openVariables = $('#open-variables');
  openVariables.show();
  const closeVariables = $('#close-variables');
  if(!closeVariables.hasClass('hidden')){
      closeVariables.addClass('hidden');
  }

    const variables = $('#variables');
  variables.addClass('h-24');
  variables.removeClass('h-full');
    const output = $('#output');
  output.show();
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

function showSuccessMessage(isModified: boolean){
  removeBulb();
  var allsuccessmessages = ClientMessages['Transpile_success'].split('\n');
  var randomnum: number = Math.floor(Math.random() * allsuccessmessages.length);
  success.show(allsuccessmessages[randomnum], isModified);
}

function createModal(level:number ){
  let editor = "<div id='modal-editor' class=\"w-full flex-1 text-lg rounded\" style='height:200px; width:50vw;'></div>".replace("{level}", level.toString());
  let title = ClientMessages['Program_repair'];
  modal.repair(editor, 0, title);
}

export function toggleDevelopersMode(event='click', enforceDevMode: boolean) {
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
      window.localStorage.setItem('developer_mode', `${enable}`);
      if (enable) {
        pushAchievement("lets_focus");
      }
      break;
  }

  // DevMode hides the tabs and makes resizable elements track the appropriate size.
  // (Driving from HTML attributes is more flexible on what gets resized, and avoids duplicating
  // size literals between HTML and JavaScript).
  $('#adventures').toggle(!enable);
  // Parsons dont need a fixed height
  if (currentTab === 'parsons') return
  $('[data-devmodeheight]').each((_, el) => {
    const heights = $(el).data('devmodeheight').split(',') as string[];
    $(el).css('height', heights[enable ? 1 : 0]);
  });
}

export function saveForTeacherTable(table: string) {
  let open = window.localStorage.getItem(table);
  const arrow = document.querySelector('#' + table + '_arrow') as HTMLElement;
  if (open == 'true'){
    window.localStorage.setItem(table, 'false')
    $('#' + table).hide();
    arrow.classList.remove('rotate-180');
  } else {
    window.localStorage.setItem(table, 'true')
    $('#' + table).show();
    arrow.classList.add('rotate-180');
  }
}

export function getForTeacherTable(table: string) {
  let open = window.localStorage.getItem(table);
  const arrow = document.querySelector('#' + table + '_arrow') as HTMLElement;
  if (open == 'true'){
    $('#' + table).show();
    arrow.classList.add('rotate-180');
  } else {
    $('#' + table).hide()
    arrow.classList.remove('rotate-180');
  }
}

/**
 * Run a code block, show an error message if we catch an exception
 */
export async function tryCatchErrorBox(cb: () => void | Promise<void>) {
  try {
    return await cb();
  } catch (e: any) {
    console.log('Error', e);
    error.show(ClientMessages['Transpile_error'], e.message);
  }
}

export function toggle_keyword_language(current_lang: string, new_lang: string) {
  tryCatchErrorBox(async () => {
    const response = await postJsonWithAchievements('/translate_keywords', {
      code: theGlobalEditor.contents,
      start_lang: current_lang,
      goal_lang: new_lang,
      level: theLevel,
    });

    if (response.success) {
      const code = response.code
      theGlobalEditor.contents = code;
      const saveName = saveNameFromInput();

      // save translated code to local storage
      // such that it can be fetched after reload
      localSave(currentTabLsKey(), { saveName, code });
      $('#editor').attr('lang', new_lang);

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
    if (response.success) {
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
    // remove the fixed height from the editor
    document.getElementById('code_editor')!.style.height = '100%'
    document.getElementById('code_output')!.style.height = '100%'
    return;
  } else {
    $('[data-devmodeheight]').each((_, el) => {
      const heights = $(el).data('devmodeheight').split(',') as string[];
      $(el).css('height', heights[0]);
    });
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
    const response = await postJsonWithAchievements('/programs', {
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
