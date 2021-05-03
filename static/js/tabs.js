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

    if (tabName !== 'level') window.State.adventure_name = tabName;

    const target = $('*[data-tabtarget="t-' + tabName + '"]');
    const allTargets = target.siblings('*[data-tabtarget]');

    allTabs.removeClass('tab-selected');
    tab.addClass('tab-selected');

    allTargets.addClass('hidden');
    target.removeClass('hidden');

    // If reloading the default tab, show the default program (loaded_program or start_code)
    if (tabName === 'level') {
       window.editor.setValue (window.State.default_program);
       $ ('#program_name').val (window.State.default_program_name);
    }
    else {
      var foundSaved;
      window.State.adventures.map (function (adventure) {
         // If loading an adventure tab and there's a saved game, restore the loaded_program or start_code to the editor.
         if (adventure.short_name !== tabName && adventure.loaded_program) return;
         window.editor.setValue (adventure.loaded_program);
         $ ('#program_name').val (adventure.loaded_program_name);
         foundSaved = true;
      });
      if (! foundSaved) $ ('#program_name').val (tabName + ' - ' + window.State.level_title + ' ' + window.State.level);
    }
    window.editor.clearSelection ();

    e.preventDefault();
    return false;
  });

  // If we're opening an adventure from the beginning (either through a link to /hedy/adventures or through a saved program for an adventure), we click on the relevant tab.
  if (window.State.adventure_name) {
     console.log ('click', '[data-tabtarget="t-' + window.State.adventure_name + '"]');
     $('[data-tab="t-' + window.State.adventure_name + '"]') [0].click ();
  }
});
