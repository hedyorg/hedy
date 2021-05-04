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

    window.State.adventure_name = tabName === 'level' ? undefined : tabName;

    const target = $('*[data-tabtarget="t-' + tabName + '"]');
    const allTargets = target.siblings('*[data-tabtarget]');

    allTabs.removeClass('tab-selected');
    tab.addClass('tab-selected');

    allTargets.addClass('hidden');
    target.removeClass('hidden');

    // Logic for updating the input with program name and the actual program in the editor.
    if (tabName === 'level') {
       // If the page was loaded with a program that belongs to an adventure (hence not a program belonging to a level), when switching to levels, restore defaults.
       if (window.State.adventure_name_onload) {
          $ ('#program_name').val (window.State.default_program_name);
          window.editor.setValue (window.State.default_program);
       }
       // Otherwise, restore the saved program.
       else {
          $ ('#program_name').val (window.State.loaded_program_name);
          window.editor.setValue (window.State.loaded_program);
       }
    }
    else {
      window.State.adventures.map (function (adventure) {
         // If the adventure being iterated is not the selected one, return.
         if (adventure.short_name !== tabName) return;
         // If the adventure has no saved program, load default name and program from the adventure.
         if (! adventure.loaded_program) {
            $ ('#program_name').val (tabName + ' - ' + window.State.level_title + ' ' + window.State.level);
            return window.editor.setValue (adventure.start_code);
         }
         // If the loaded program is from the current adventure, use that, overriding the loaded program that came in the adventure.
         if (window.State.loaded_program && window.State.adventure_name_onload === tabName) {
            $ ('#program_name').val (window.State.loaded_program_name);
            return window.editor.setValue (window.State.loaded_program);
         }
         // Otherwise, use the loaded program from the adventure.
         window.editor.setValue (adventure.loaded_program);
         $ ('#program_name').val (adventure.loaded_program_name);
      });
    }
    window.editor.clearSelection ();

    e.preventDefault();
    return false;
  });

  // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
  if (window.State.adventure_name) {
     $('[data-tab="t-' + window.State.adventure_name + '"]') [0].click ();
  }
});
