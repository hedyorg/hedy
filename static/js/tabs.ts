import { modal } from './modal';
import { theGlobalEditor } from './app';

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
$(function() {
function resetWindow() {
    $ ('#warningbox').hide ();
    $ ('#errorbox').hide ();
    $ ('#okbox').hide ();
    const output = $('#output');
    const variable_button = $(output).find('#variable_button');
    const variables = $(output).find('#variables');
    output.empty();
    $ ('#turtlecanvas').empty ();
    output.append(variable_button);
    output.append(variables);
    window.State.unsaved_changes = false;
  }

  function switchToTab(tabName: string) {
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
    window.State.adventures?.map (function(adventure: Adventure) {
      adventures [adventure.short_name] = adventure;
    });

    // @ts-ignore
    document.getElementById("repair_button").style.visibility = "hidden";
    resetWindow();

      if (tabName === 'quiz') {
        // If the developers mode is still on -> reverse and THEN show the quiz tab
        if ($('#developers_toggle').is(":checked")) {
          $('#developers_toggle').prop('checked', false);
          $('#editor-area').addClass('mt-5');
          $('#code_editor').height('22rem');
          $('#code_output').height('22rem');
          $('#adventures-tab').show();
        }
      $ ('#adventures-tab').css('height', '');
      $ ('#adventures-tab').css('min-height', '14em');
      $ ('#adventures-tab').css('max-height', '100%');
      $ ('#level-header input').hide ();
      $ ('#editor-area').hide ();
      $('#developers_toggle_container').hide ();
      return;
    }
    $ ('#adventures-tab').css('max-height', '20em')
    $('#developers_toggle_container').show ();
    $ ('#level-header input').show ();
    $ ('#editor-area').show ();


    // If the loaded program (directly requested by link with id) matches the currently selected tab, use that, overriding the loaded program that came in the adventure or level.
    if (window.State.loaded_program && (window.State.adventure_name_onload) === tabName) {
      $ ('#program_name').val (window.State.loaded_program.name);
      theGlobalEditor?.setValue (window.State.loaded_program.code);
    }
    // If there's a loaded program for the adventure or level now selected, use it.
    else if (adventures[tabName]?.loaded_program) {
      $ ('#program_name').val (adventures[tabName].loaded_program!.name);
      theGlobalEditor?.setValue (adventures[tabName].loaded_program!.code);
    }
    // If there's no loaded program (either requested by id or associated to the adventure/level), load defaults.
    else if (window.State.default_program_name && window.State.default_program) {
      $ ('#program_name').val(window.State.default_program_name);
      theGlobalEditor?.setValue(window.State.default_program);
    }
    else {
      if (tab.hasClass('teacher_tab')) {
        $ ('#program_name').val (tabName);
        window.State.adventure_name = tabName;
        theGlobalEditor?.setValue ("");
      } else {
        if (adventures[tabName].default_save_name == 'intro') {
          $('#program_name').val(window.State.level_title + ' ' + window.State.level);
        } else {
          $('#program_name').val(adventures [tabName].default_save_name + ' - ' + window.State.level_title + ' ' + window.State.level);
        }
        theGlobalEditor?.setValue(adventures [tabName].start_code);
      }
    }

    window.State.adventure_name = tabName === 'intro' ? undefined : tabName;
    theGlobalEditor?.clearSelection();
    // If user wants to override the unsaved program, reset unsaved_changes
    window.State.unsaved_changes = false;
  }

  $('*[data-tab]').click(function (e) {
    const tab = $(e.target);
    const tabName = tab.data('tab');

    e.preventDefault ();

    // If there are unsaved changes, we warn the user before changing tabs.
    if (window.State.unsaved_changes) modal.confirm(ErrorMessages['Unsaved_Changes'], () => switchToTab(tabName));
    else switchToTab(tabName);

    // Do a 'replaceState' to add a '#anchor' to the URL
    const hashFragment = tabName !== 'level' ? tabName : '';
    if (window.history) { window.history.replaceState(null, '', '#' + hashFragment); }
  });

  // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
  // We click on `level` to load a program associated with level, if any.
  if (window.State && window.State.adventure_name) {
    switchToTab(window.State.adventure_name);
  }
  else if (window.location.hash) {
    // If we have an '#anchor' in the URL, switch to that tab
    const hashFragment = window.location.hash.replace(/^#/, '');
    if (hashFragment) {
      switchToTab(hashFragment);
    }
  }
});