import {pushAchievement, runit, theGlobalEditor} from "../app";
import {addHighlightBorder, relocatePopup, removeBorder, tutorialPopup} from "./utils";
import { clearUnsavedChanges } from '../browser-helpers/unsaved-changes';

let current_step = 0;

export function startIntro() {
  current_step = 1;
  $('#adventures').hide();
  $('#variables_container').hide();
  theGlobalEditor.contents = "";

  tutorialPopup("intro", current_step);
}

export function callNextIntroStep() {
  current_step += 1;

  if (current_step == 2) {
    codeEditorStep();
  } else if (current_step == 3) {
    codeOutputStep();
  } else if (current_step == 4) {
    runButtonStep();
  } else if (current_step == 5) {
    tryRunButtonStep();
  } else if (current_step == 6) {
    speakAloudStep();
  } else if (current_step == 7) {
    runSpeakAloudStep();
  } else if (current_step == 8) {
    nextLevelStep();
  } else if (current_step == 9) {
    levelDefaultStep();
  } else if (current_step == 10) {
    adventureTabsStep();
  } else if (current_step == 11) {
    parsonsTabStep();
  } else if (current_step == 12) {
    quizTabStep();
  } else if (current_step == 13) {
    saveShareStep();
  } else if (current_step == 14) {
    cheatsheetStep();
  } else if (current_step == 15) {
    pushAchievement("well_begun_is_half_done");
    $('#achievement_pop-up').removeClass('z-10');
    $('#achievement_pop-up').addClass('z-50');
    // If the achievement pop-up is visible -> wait with the next function call
    setTimeout(function(){
      if ($('#achievement_pop-up').is(':visible')) {
        setTimeout(function() {
          endTutorial();
          $('#achievement_pop-up').removeClass('z-50');
          $('#achievement_pop-up').addClass('z-10');
        }, 5000);
      } else {
        endTutorial();
        $('#achievement_pop-up').removeClass('z-50');
        $('#achievement_pop-up').addClass('z-10');
      }
    }, 500);
  } else {
    location.replace("/hedy");
  }
}

function codeEditorStep() {
  $('#editor').addClass("z-40");
  addHighlightBorder("editor");

  relocatePopup(65, 30);
  theGlobalEditor.contents = "print ___";  
  tutorialPopup("intro", current_step);
}

function codeOutputStep() {
  removeBorder("editor");
  $('#code_output').addClass("z-40");
  addHighlightBorder("code_output");

  runit (1, "en", false, "", "run",function () {
    $ ('#output').focus ();
  });

  relocatePopup(35, 30);
  tutorialPopup("intro", current_step);
}

function runButtonStep() {
  removeBorder("code_output");
  $('#code_related_buttons').show();
  $('#runButtonContainer').addClass("z-40");
  addHighlightBorder("runButtonContainer");

  relocatePopup(50, 30);
  tutorialPopup("intro", current_step);
}

function tryRunButtonStep() {
  $.ajax({
      type: 'GET',
      url: '/get_tutorial_step/intro/code_snippet/',
      dataType: 'json'
    }).done(function(response: any) {
       theGlobalEditor.contents = response.code;
    }).fail(function() {
       theGlobalEditor.contents = "print Hello world!\nprint I'm learning Hedy with the tutorial!";
    });

  relocatePopup(50, 70);
  tutorialPopup("intro", current_step);
}

function speakAloudStep() {
  removeBorder("runButtonContainer");
  $('#editor').removeClass('z-40');
  $('#code_output').removeClass('z-40');
  $('#runButtonContainer').removeClass('z-40');

  $('#speak_container').addClass('z-40 bg-white relative');

  addHighlightBorder("speak_container");

  relocatePopup(50, 30);
  tutorialPopup("intro", current_step);
}

function runSpeakAloudStep() {
  $('#editor').addClass('z-40');
  $('#code_output').addClass('z-40');
  $('#runButtonContainer').addClass('z-40');

  relocatePopup(50, 70);
  tutorialPopup("intro", current_step);
}

function nextLevelStep() {
  removeBorder("speak_container");
  $('#editor').removeClass('z-40');
  $('#code_output').removeClass('z-40');
  $('#runButtonContainer').removeClass('z-40');
  $('#speak_container').removeClass('z-40 bg-white relative');

  $('#next_level_button').addClass("z-40");
  $('#next_level_button').removeAttr('onclick');
  addHighlightBorder("next_level_button");

  relocatePopup(50, 30);
  tutorialPopup("intro", current_step);
}

function levelDefaultStep() {
  removeBorder("next_level_button");
  $('#next_level_button').removeClass('z-40');

  $('#code_content_container').addClass('z-40');
  $('#adventures').addClass('z-40 bg-gray-100');
  $('#adventures').show();

  // Set to false, prevent "are you sure you want to switch without saving" pop-up
  clearUnsavedChanges();

  addHighlightBorder("adventures");
  relocatePopup(50, 40);
  tutorialPopup("intro", current_step);
}

function adventureTabsStep() {
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "story") {
      // Set to false, prevent "are you sure you want to switch without saving" pop-up
      clearUnsavedChanges();
      $(this).click();
    }
  });

  tutorialPopup("intro", current_step);
}

function parsonsTabStep() {
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "parsons") {
      // Set to false, prevent "are you sure you want to switch without saving" pop-up
      clearUnsavedChanges();
      $(this).click();
    }
  });
  tutorialPopup("intro", current_step);
}

function quizTabStep() {
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "quiz") {
      // Set to false, prevent "are you sure you want to switch without saving" pop-up
      clearUnsavedChanges();
      $(this).click();
    }
  });
  tutorialPopup("intro", current_step);
}

function saveShareStep() {
  // We should go back to the intro tab to make sure the save/share option is shown
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "default") {
      clearUnsavedChanges();
      $(this).click();
    }
  });
  removeBorder("adventures");
  $('#code_content_container').removeClass('z-40');
  $('#level-header').addClass("z-40");
  $('#cheatsheet_container').hide();
  addHighlightBorder("level-header");

  $('#save_program_button').removeAttr('onclick');
  $('#share_program_button').removeAttr('onclick');

  relocatePopup(50, 30);
  tutorialPopup("intro", current_step);
}

function cheatsheetStep() {
  $('#cheatsheet_container').show();
  $('#code_output').removeClass('z-40');
  $('#adventures').removeClass('z-40');
  $('#cheatsheet_dropdown').addClass('z-40');
  $('#cheatsheet_dropdown').show();

  tutorialPopup("intro", current_step);
}

function endTutorial() {
  removeBorder("level-header");
  $('#level-header').removeClass('z-40');
  $('#cheatsheet_dropdown').removeClass('z-40');
  $('#cheatsheet_dropdown').hide();

  relocatePopup(50, 15);
  tutorialPopup("intro", current_step);
}

