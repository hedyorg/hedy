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
  $('*[data-tab]').click(function (e) {
    const tab = $(e.target);
    const allTabs = tab.siblings('*[data-tab]');
    const tabName = tab.data('tab').replace ('t-', '');

    // If there are unsaved changes, we warn the user before changing tabs.
    if (window.State.unsaved_changes) {
      var leave = confirm (window.auth.texts.unsaved_changes);
      if (! leave) {
        e.preventDefault();
        return false;
      }
      // If user wants to override the unsaved program, reset unsaved_changes
      window.State.unsaved_changes = false;
    }

    window.State.adventure_name = tabName === 'level' ? undefined : tabName;

    const target = $('*[data-tabtarget="t-' + tabName + '"]');
    const allTargets = target.siblings('*[data-tabtarget]');

    allTabs.removeClass('tab-selected');
    tab.addClass('tab-selected');

    allTargets.addClass('hidden');
    target.removeClass('hidden');

    const adventures = {};
    window.State.adventures.map (function (adventure) {
      adventures [adventure.short_name] = adventure;
    });

    // If the loaded program (directly requested by link with id) matches the currently selected tab, use that, overriding the loaded program that came in the adventure or level.
    if (window.State.loaded_program && (window.State.adventure_name_onload || 'level') === tabName) {
      $ ('#program_name').val (window.State.loaded_program.name);
      window.editor.setValue (window.State.loaded_program.code);
    }
    // If there's a loaded program for the adventure or level now selected, use it.
    else if (adventures [tabName].loaded_program) {
      $ ('#program_name').val (adventures [tabName].loaded_program.name);
      window.editor.setValue (adventures [tabName].loaded_program.code);
    }
    // If there's no loaded program (either requested by id or associated to the adventure/level), load defaults.
    else if (tabName === 'level') {
      $ ('#program_name').val (window.State.default_program_name);
      window.editor.setValue (window.State.default_program);
    }
    else {
      $ ('#program_name').val (adventures [tabName].default_save_name + ' - ' + window.State.level_title + ' ' + window.State.level);
      window.editor.setValue (adventures [tabName].start_code);
    }

    window.editor.clearSelection ();
    window.State.unsaved_changes = false;

    e.preventDefault();
    return false;
  });

  // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
  // We click on `level` to load a program associated with level, if any.
  const adventureName = window.State && window.State.adventure_name;
  $('[data-tab="t-' + (adventureName || 'level') + '"]').click ();
});
