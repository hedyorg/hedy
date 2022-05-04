import {theGlobalEditor} from "./app";

let current_step = 0;

// We call this function on load -> fix relevant stuff
(function() {
  $('#tutorial_next_button').off('click').on('click', () => {
    $('#tutorial-pop-up').hide();
    callNextStep();
  });
})();

function hideFunctionality() {
  $('#level-header').hide();
  $('#adventures').hide();
  $('#editor-area').hide();
  $('#developers_toggle_container').hide();
  $('#tutorial-mask').show();
}

function callNextStep() {
  current_step += 1;
  console.log(current_step);
  $('#tutorial-mask').hide();

  // Step 1: Show the code editor
  if (current_step == 1) {
    $('#tutorial-mask').show();

    $('#editor').addClass("z-40");
    $('#editor-area').show();
    $('#code_output').hide();
    $('#code_related_buttons').hide();
    relocatePopup("right");
    tutorialPopup("De code editor", "In dit venster schrijf je alle code, probeer maar wat in te vullen!");
  } else if (current_step == 2) {
    // Reset highlight from previous step
    $('#editor').removeClass("z-40");
    $('#tutorial-mask').show();

    $('#code_output').addClass("z-40");
    $('#code_output').show();

    relocatePopup("left");
    tutorialPopup("Het output venster", "De code die je uitvoert wordt hier weergegeven.");
  } else if (current_step == 3) {
    // Reset highlight from previous step
    $('#code_output').removeClass("z-40");
    $('#tutorial-mask').show();

    $('#code_related_buttons').show();
    $('#debug_container').hide();
    $('#speak_container').hide();

    $('#runButtonContainer').addClass("z-50");
    relocatePopup("middle");
    tutorialPopup("De uitvoer knop", "Met deze knop kun je een programma uitvoeren, zullen we het proberen?");
  } else if (current_step == 4) {
    $('#runButtonContainer').removeClass("z-50");
    theGlobalEditor?.setValue("print hallo wereld!");

    relocatePopup("bottom");
    tutorialPopup("Probeer het uit!", "Probeer het uit, klik op volgende stap als je klaar bent");
  }

  // Step 4: Show the adventures

  // Step 5: Show the cheatsheet
}

function relocatePopup(direction: string) {
  $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  if (direction == "left") {
      $('#tutorial-pop-up').css({'left': '35%'});
  } else if (direction === "right") {
      $('#tutorial-pop-up').css({'left': '65%'});
  } else if (direction == "buttom") {
      $('#tutorial-pop-up').css({'top': '60%'});
  } else {
    $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  }
}

function tutorialPopup(title: string, message: string) {
  $('#tutorial_title').text(title);
  $('#tutorial_text').text(message);
  $('#tutorial-pop-up').fadeIn(1500);
}

export function startTutorial() {
  hideFunctionality();
  tutorialPopup("Welkom bij Hedy!", "In deze uitleg leggen we stap voor stap uit wat je allemaal kunt doen");
}

