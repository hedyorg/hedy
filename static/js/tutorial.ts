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

function codeEditorStep() {
  $('#tutorial-mask').show();
  $('#editor').addClass("z-40");
  $('#editor-area').show();
  $('#code_output').hide();
  $('#code_related_buttons').hide();
  relocatePopup("right");
  tutorialPopup("De code editor", "In dit venster schrijf je alle code, probeer maar wat in te vullen!");
}

function codeOutputStep() {
  // Reset highlight from previous step
  $('#editor').removeClass("z-40");
  $('#tutorial-mask').show();

  $('#code_output').addClass("z-40");
  $('#code_output').show();
  $('#variables').hide();

  relocatePopup("left");
  tutorialPopup("Het output venster", "De code die je uitvoert wordt hier weergegeven.");
}

function runButtonStep() {
  // Reset highlight from previous step
  $('#code_output').removeClass("z-40");
  $('#tutorial-mask').show();

  $('#code_related_buttons').show();
  $('#debug_container').hide();
  $('#speak_container').hide();

  $('#runButtonContainer').addClass("z-40");
  relocatePopup("middle");
  tutorialPopup("De uitvoer knop", "Met deze knop kun je een programma uitvoeren, zullen we het proberen?");
}

function tryRunButtonStep() {
  $('#editor').addClass("z-40");
  $('#code_output').addClass("z-40");
  $('#tutorial-mask').show();
  theGlobalEditor?.setValue("print Hallo wereld!\nprint Ik volg de Hedy tutorial");
  theGlobalEditor?.setOptions({readOnly: true});

  relocatePopup("bottom");
  tutorialPopup("Probeer het uit!", "Voer het programma uit, klik op 'volgende stap' als je klaar bent.");
}

function levelDefaultStep() {
  $('#code_output').removeClass("z-40");
  $('#editor').removeClass("z-40");
  $('#code_output').removeClass("z-40");

  $('#adventures').addClass("z-40");
  $('#adventures').show();
  $('#tutorial-mask').show();

  // Hide all tabs except the default level one
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') != "default") {
      $(this).hide();
    } else {
      $(this).addClass("z-40");
    }
  });

  relocatePopup("bottom");
  tutorialPopup("Level uitleg", "In het eerste tabje vind je altijd de level uitleg. Hier worden in elk level de nieuwe commando's uitgelegd.");
}

function adventureTabsStep() {
  $('#tutorial-mask').show();

  // Show all tabs except the quiz one
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') != "quiz") {
      $(this).addClass("z-40");
      $(this).show();
    }
    if ($(this).attr('data-tab') == "default") {
      $(this).removeClass("z-40");
    }
  });

  tutorialPopup("Avonturen", "De andere tabjes bevatten avonturen, deze kun je per level maken. Ze gaan van makkelijk naar moeilijk!");
}

function quizTabStep() {
  // Show all tabs (including the quiz one
  $('.tab').show();
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "quiz") {
      $(this).addClass("z-40");
    } else {
      $(this).removeClass("z-40");
    }
  });

  tutorialPopup("Quiz", "Aan het einde van elk level kun je een quiz maken, zo kun je goed testen of je alles snapt!");
}


function callNextStep() {
  current_step += 1;
  console.log(current_step);
  $('#tutorial-mask').hide();

  // Step 1: Show the code editor
  if (current_step == 1) {
    codeEditorStep();
  } else if (current_step == 2) {
    codeOutputStep();
  } else if (current_step == 3) {
    runButtonStep();
  } else if (current_step == 4) {
    tryRunButtonStep();
  } else if (current_step == 5) {
    levelDefaultStep();
  } else if (current_step == 6) {
    adventureTabsStep();
  } else if (current_step == 7) {
    quizTabStep();
  } else if (current_step == 8) {
    // Show the cheatsheet
  } else if (current_step == 9) {
    // Show the speak aloud option
  } else if (current_step == 10) {
    // Show the saving / sharing bar
  }
}

function relocatePopup(direction: string) {
  // Todo TB -> Might be nice to re-write this to an x/y coordinate function
  // So we can call it like relocatePopup(30, 70) to better align with what we want

  $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  if (direction == "left") {
      $('#tutorial-pop-up').css({'left': '35%'});
  } else if (direction === "right") {
      $('#tutorial-pop-up').css({'left': '65%'});
  } else if (direction == "bottom") {
      $('#tutorial-pop-up').css({'top': '60%'});
  } else {
    $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  }
}

function tutorialPopup(title: string, message: string) {
  $('#tutorial_title').text(title);
  $('#tutorial_text').text(message);
  //$('#tutorial-pop-up').fadeIn(1500);
  $('#tutorial-pop-up').show(); //Use show() for debugging purposes
}

export function startTutorial() {
  hideFunctionality();
  tutorialPopup("Welkom bij Hedy!", "In deze uitleg leggen we stap voor stap uit wat je allemaal kunt doen");
}

