import {callNextIntroStep, startIntro } from "./intro";
import {callTeacherNextStep, startTeacher} from "./teacher";

// We should add this import for every level we add to the tutorial
import {callNextStepLevel1, startLevel1} from "./level1";

let current_level = "";

// We call this function on load -> customize click event of the tutorial button
(function() {
  $('#tutorial_next_button').off('click').on('click', () => {
    $('#tutorial-pop-up').hide();
    // If we are a student -> call the next student tutorial step, otherwise call the teacher step
    if (current_level == "intro") {
      return callNextIntroStep();
    } else if (current_level == "teacher") {
      return callTeacherNextStep();
    }
    return callNextLevelStep(current_level);
  });
})();

export function startIntroTutorial() {
  $('#tutorial-mask').show();
  current_level = "intro";
  startIntro();
}

export function startLevelTutorial(level: string) {
  $('#tutorial-mask').show();
  current_level = level;
  startLevel(level);
}

export function startTeacherTutorial() {
  $('#tutorial-mask').show();
  current_level = "teacher";
  startTeacher();
}

function startLevel(current_level: string) {
  if (current_level == "1") {
    startLevel1();
  }
  /*
    else if (current_level == "2") {
      startLevel2();
    }
  */
}

function callNextLevelStep(current_level: string) {
  if (current_level == "1") {
    callNextStepLevel1();
  }
  /*
    else if (current_level == "2") {
      callNextStepLevel2();
    }
  */
}

