import { modal } from './modal';
import { theGlobalEditor } from './app';
import {loadParsonsExercise} from "./parsons";
import { Adventure, APP_STATE, clearUnsavedChanges, hasUnsavedChanges } from './state';
import { ClientMessages } from './client-messages';

let _currentTab: string | undefined;

/**
 * Activate tabs
 *
 * Protocol:
 *
 * - Tabs consist of a TAB (the sticky-outy bit) and a TARGET
 *   (the pane that gets shown and hidden).
 *
 * - TABS should have: <... data-tab="SOME-ID">
 *
 * - TARGETS should have: <... data-tabtarget="SOME-ID">
 *
 * When a TAB is clicked, the TARGET with the matching id is shown
 * (and all other TARGETS in the same containing HTML element are hidden).
 *
 * The active TAB is indicated by the  '.tab-selected' class, the active
 * TARGET by the *absence* of the '.hidden' class.
 */
export function initializeTabs() {
  $('*[data-tab]').on('click', (e) => {
    const tab = $(e.target);
    const tabName = tab.data('tab');

    e.preventDefault ();

    // If there are unsaved changes, we warn the user before changing tabs.
    if (hasUnsavedChanges()) {
      modal.confirm(ClientMessages['Unsaved_Changes'], () => switchToTab(tabName));
    } else {
      switchToTab(tabName);
    }

    // Do a 'replaceState' to add a '#anchor' to the URL
    const hashFragment = tabName !== 'level' ? tabName : '';
    if (window.history) { window.history.replaceState(null, '', '#' + hashFragment); }
  });

  // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
  // We click on `level` to load a program associated with level, if any.
  if (APP_STATE.loaded_program?.adventure_name) {
    switchToTab(APP_STATE.loaded_program?.adventure_name);
  }
  else if (window.location.hash) {
    // If we have an '#anchor' in the URL, switch to that tab
    const hashFragment = window.location.hash.replace(/^#/, '');
    if (hashFragment) {
      switchToTab(hashFragment);
    }
  } else {
    // If this is not the case: open the first tab we find
    let tabname = $('.tab:first').attr('data-tab');
    if (tabname) {
      switchToTab(tabname);
    }
  }
}

export function currentTab() {
  return _currentTab;
}

/**
 * Hide all things that may have been dynamically shown
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
  clearUnsavedChanges();
}

function switchToTab(tabName: string) {
  _currentTab = tabName;

  // Find the tab that leads to this selection, and its siblings
  const tab = $('*[data-tab="' + tabName + '"]');
  const allTabs = tab.siblings('*[data-tab]');

  // Find the target associated with this selection, and its siblings
  const target = $('*[data-tabtarget="' + tabName + '"]');
  const allTargets = target.siblings('*[data-tabtarget]');

  // Fix classes
  allTabs.removeClass('tab-selected');
  tab.addClass('tab-selected');

  allTargets.addClass('hidden');
  target.removeClass('hidden');

  const adventures: Record<string, Adventure> = {};
  APP_STATE.adventures?.map (function(adventure: Adventure) {
    adventures [adventure.short_name] = adventure;
  });

  resetWindow();

  const isCodeTab = !(tabName === 'quiz' || tabName === 'parsons');

  // .toggle(bool) sets visibility based on the boolean

  // Explanation area is visible for non-code tabs, or when we are NOT in developer's mode
  $('#adventures-tab').toggle(!(isCodeTab && $('#developers_toggle').is(":checked")));
  $('#developers_toggle_container').toggle(isCodeTab);
  $('#level-header input').toggle(isCodeTab);
  $('#parsons_code_container').toggle(tabName === 'parsons');
  $('#editor-area').toggle(isCodeTab || tabName === 'parsons');
  $('#editor').toggle(isCodeTab);
  $('#debug_container').toggle(isCodeTab);

  if (tabName === 'parsons') {
    loadParsonsExercise(APP_STATE.level, 1);
    return;
  }

  // If the loaded program (directly requested by link with id) matches the currently selected tab, use that, overriding the loaded program that came in the adventure or level.
  if (APP_STATE.loaded_program?.adventure_name === tabName) {
    $ ('#program_name').val (APP_STATE.loaded_program.name);
    theGlobalEditor?.setValue (APP_STATE.loaded_program.code);
  }
  // If there's a loaded program for the adventure or level now selected, use it.
  else if (adventures[tabName]?.loaded_program) {
    $ ('#program_name').val (adventures[tabName].loaded_program!.name);
    theGlobalEditor?.setValue (adventures[tabName].loaded_program!.code);
  }
  else {
    if (tab.hasClass('teacher_tab')) {
      $ ('#program_name').val (tabName);
      theGlobalEditor?.setValue ("");
    } else {
      const adventure = adventures[tabName];
      if (adventure) {
        if (adventure.default_save_name == 'intro') {
          $('#program_name').val(`${ClientMessages.level_title} ${APP_STATE.level}`);
        } else {
          $('#program_name').val(`${adventure.default_save_name} - ${ClientMessages.level_title} ${APP_STATE.level}`);
        }
        theGlobalEditor?.setValue(adventure.start_code);
      }
    }
  }

  theGlobalEditor?.clearSelection();
  theGlobalEditor?.session.clearBreakpoints();

  // If user wants to override the unsaved program, reset unsaved_changes
  clearUnsavedChanges();
}
