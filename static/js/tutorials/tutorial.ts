import {callNextIntroStep, startIntro} from "./intro";
import {callTeacherNextStep, startTeacher} from "./teacher";

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
    //return callNextLevelStep(current_level);
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
  //startLevel(level);
}

export function startTeacherTutorial() {
  $('#tutorial-mask').show();
  current_level = "teacher";
  startTeacher();
}

