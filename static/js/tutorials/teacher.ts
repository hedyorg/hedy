import {pushAchievement} from "../app";
import {addHighlightBorder, relocatePopup, removeBorder, tutorialPopup} from "./utils";

function classStep() {
  $('#auth_main_container').addClass('z-40');
  $('#teacher_classes').addClass('z-40 bg-gray-100');
  addHighlightBorder("teacher_classes");

  relocatePopup(50, 40);
  tutorialPopup();
}

function customizeClassStep() {
  tutorialPopup();
}

function adventureStep() {
  $('#teacher_adventures').addClass('z-40 bg-gray-100');
  removeBorder("teacher_classes");
  addHighlightBorder("teacher_adventures");

  relocatePopup(50, 70);
  tutorialPopup();
}

function multipleAccountsStep() {
  $('#teacher_accounts').addClass('z-40 bg-gray-100');
  removeBorder("teacher_adventures");
  addHighlightBorder("teacher_accounts");

  relocatePopup(50, 20);
  tutorialPopup();
}

function documentationStep() {
  $('#teacher_documentation').addClass('z-40 bg-gray-100');
  removeBorder("teacher_accounts");
  addHighlightBorder("teacher_documentation")

  tutorialPopup();
}

function teacherEndStep() {
  removeBorder("teacher_documentation");
  tutorialPopup();
}

export function callTeacherNextStep() {
  if (current_step == 2) {
    classStep();
  } else if (current_step == 3) {
    customizeClassStep();
  } else if (current_step == 4) {
    adventureStep();
  } else if (current_step == 5) {
    multipleAccountsStep();
  } else if (current_step == 6) {
    documentationStep();
  } else if (current_step == 7) {
    pushAchievement("ring_the_bell");
    $('#achievement_pop-up').removeClass('z-10');
    $('#achievement_pop-up').addClass('z-50');
    // If the achievement pop-up is visible -> wait with the next function call
    setTimeout(function(){
      if ($('#achievement_pop-up').is(':visible')) {
        setTimeout(function() {
          teacherEndStep();
          $('#achievement_pop-up').removeClass('z-50');
          $('#achievement_pop-up').addClass('z-10');
        }, 5000);
      } else {
        teacherEndStep();
        $('#achievement_pop-up').removeClass('z-50');
        $('#achievement_pop-up').addClass('z-10');
      }
    }, 500);
  } else {
    location.replace("/for-teachers");
  }
}