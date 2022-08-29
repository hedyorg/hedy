import {pushAchievement, theGlobalEditor} from ".././app";
import "./utils";
import "./intro";

/*
Todo: Completely re-structure the tutorial structure
Suggested code structure:
- Use the tutorial.ts file for the general code such as:
  - Highlighting code
  - Step retrieval code
  - Error handling
- For each step create a dedicated .ts file:
  - Intro
  - Teacher
  - Each level
- Dynamically check if there is a corresponding file
- If not, don't show any tutorial -> redirect to /hedy/<level>
 */

let current_step = 0;
let current_level = "";

// We call this function on load -> customize click event of the tutorial button
(function() {
  $('#tutorial_next_button').off('click').on('click', () => {
    $('#tutorial-pop-up').hide();
    // If we are a student -> call the next student tutorial step, otherwise call the teacher step
    current_step += 1;
    if (current_level == "intro") {
      return callNextIntroStep();
    } else if (current_level == "teacher") {
      return callTeacherNextStep();
    } //return callNextLevelStep(current_level);
  });
})();

function classStep() {
  $('#auth_main_container').addClass('z-40');
  $('#teacher_classes').addClass('z-40 bg-gray-100');
  addHighlightBorder("teacher_classes");

  relocatePopup(50, 40);
  tutorialPopup(current_step);
}

function customizeClassStep() {
  tutorialPopup(current_step);
}

function adventureStep() {
  $('#teacher_adventures').addClass('z-40 bg-gray-100');
  removeBorder("teacher_classes");
  addHighlightBorder("teacher_adventures");

  relocatePopup(50, 70);
  tutorialPopup(current_step);
}

function multipleAccountsStep() {
  $('#teacher_accounts').addClass('z-40 bg-gray-100');
  removeBorder("teacher_adventures");
  addHighlightBorder("teacher_accounts");

  relocatePopup(50, 20);
  tutorialPopup(current_step);
}

function documentationStep() {
  $('#teacher_documentation').addClass('z-40 bg-gray-100');
  removeBorder("teacher_accounts");
  addHighlightBorder("teacher_documentation")

  tutorialPopup(current_step);
}

function teacherEndStep() {
  removeBorder("teacher_documentation");
  tutorialPopup(current_step);
}

function callTeacherNextStep() {
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

export function startIntroTutorial() {
  $('#tutorial-mask').show();
  $('#adventures').hide();
  $('#variables_container').hide();
  theGlobalEditor?.setValue("");

  current_step = 1;
  current_level = "intro";
  tutorialPopup(current_step);
}

export function startLevelTutorial(level: string) {
  $('#tutorial-mask').show();

  current_step = 1;
  current_level = level;
  tutorialPopup(current_step);
}

export function startTeacherTutorial() {
  $('#tutorial-mask').show();

  current_step = 1;
  current_level = "teacher";
  tutorialPopup(current_step);
}

