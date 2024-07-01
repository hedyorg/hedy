import {addHighlightBorder, relocatePopup, removeBorder, tutorialPopup} from "./utils";

let current_step = 0;

export function startTeacher() {
  current_step = 1;

  tutorialPopup("teacher", current_step);
}

export function callTeacherNextStep() {
  current_step += 1;
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
    teacherEndStep();    
  } else {
    location.replace("/for-teachers");
  }
}

function classStep() {
  $('#auth_main_container').addClass('z-40');
  $('#teacher_classes').addClass('z-40 bg-gray-100');
  addHighlightBorder("teacher_classes");

  relocatePopup(50, 40);
  tutorialPopup("teacher", current_step);
}

function customizeClassStep() {
  tutorialPopup("teacher", current_step);
}

function adventureStep() {
  $('#teacher_adventures').addClass('z-40 bg-gray-100');
  removeBorder("teacher_classes");
  addHighlightBorder("teacher_adventures");

  relocatePopup(50, 70);
  tutorialPopup("teacher", current_step);
}

function multipleAccountsStep() {
  $('#teacher_accounts').addClass('z-40 bg-gray-100');
  removeBorder("teacher_adventures");
  addHighlightBorder("teacher_accounts");

  relocatePopup(50, 20);
  tutorialPopup("teacher", current_step);
}

function documentationStep() {
  $('#teacher_documentation').addClass('z-40 bg-gray-100');
  removeBorder("teacher_accounts");
  addHighlightBorder("teacher_documentation")

  tutorialPopup("teacher", current_step);
}

function teacherEndStep() {
  removeBorder("teacher_documentation");
  tutorialPopup("teacher", current_step);
}