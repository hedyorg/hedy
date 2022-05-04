import {theGlobalEditor} from "./app";

let current_step = 0;

// We call this function on load -> customize click event of the tutorial button
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
}

function codeEditorStep() {
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

  $('#code_output').addClass("z-40");
  $('#code_output').show();
  $('#variables_container').hide();

  relocatePopup("left");
  tutorialPopup("Het output venster", "De code die je uitvoert wordt hier weergegeven.");
}

function runButtonStep() {
  // Reset highlight from previous step
  $('#code_output').removeClass("z-40");

  $('#code_related_buttons').show();
  $('#debug_container').hide();
  $('#speak_container').hide();

  $('#runButtonContainer').addClass("z-40");
  // Disable the button as we only want to show where it is -> not use it yet
  $('#runit').prop("disabled",true);

  relocatePopup("middle");
  tutorialPopup("De uitvoer knop", "Met deze knop kun je een programma uitvoeren, zullen we het proberen?");
}

function tryRunButtonStep() {
  $('#editor').addClass("z-40");
  $('#code_output').addClass("z-40");

  theGlobalEditor?.setValue("print Hallo wereld!\nprint Ik volg de Hedy tutorial");
  theGlobalEditor?.setOptions({readOnly: true});
  $('#runit').prop("disabled",false);

  relocatePopup("bottom");
  tutorialPopup("Probeer het uit!", "Voer het programma uit, klik op 'volgende stap' als je klaar bent.");
}

function levelDefaultStep() {
  $('#code_output').removeClass("z-40");
  $('#editor').removeClass("z-40");
  $('#runButtonContainer').removeClass("z-40");

  $('#adventures').show();
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
  // Show all tabs except the quiz one
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') != "quiz") {
      $(this).addClass("z-40");
      $(this).show();
      if ($(this).attr('data-tab') == "story") {
        // Set to false, prevent "are you sure you want to switch without saving" pop-up
        window.State.unsaved_changes = false;
        $(this).click();
      }
    }
    if ($(this).attr('data-tab') == "default") {
      $(this).removeClass("z-40");
    }
  });

  tutorialPopup("Avonturen", "De andere tabjes bevatten avonturen, deze kun je per level maken. Ze gaan van makkelijk naar moeilijk!");
}

function quizTabStep() {
  // Show all tabs (including the quiz one) -> only highlight the quiz tab
  $('.tab').show();
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "quiz") {
      $(this).addClass("z-40");
    } else {
      $(this).removeClass("z-40");
    }
  });

  relocatePopup("top");
  tutorialPopup("Quiz", "Aan het einde van elk level kun je een quiz maken, zo kun je goed testen of je alles snapt!");
}

function saveShareStep() {
  $('#adventures-buttons').children().each(function() {
    $(this).removeClass("z-40");
  });

  $('#level-header').addClass("z-40");
  $('#level-header').show();
  $('#cheatsheet_container').hide();

  relocatePopup("middle");
  tutorialPopup("Opslaan en delen", "Je kunt al jouw gemaakt programma's opslaan en delen met andere Hedy gebruikers.");
}

function cheatsheetStep() {
  $('#level-header').removeClass("z-40");
  $('#cheatsheet_container').addClass("z-40");
  $('#cheatsheet_container').show();

  relocatePopup("middle");
  tutorialPopup("Spiekbriefje", "Als je iets bent vergeten kun je het spiekbriefje gebruiken om te kijken welke commando's je mag gebruiken.");
}

function endTutorial() {
  $('#cheatsheet_container').removeClass("z-40");
  relocatePopup("middle");
  tutorialPopup("Einde!", "Klik op 'Volgende stap' om te echt aan de slag te gaan met Hedy!");
}

function callNextStep() {
  current_step += 1;
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
    saveShareStep();
  } else if (current_step == 9) {
    cheatsheetStep();
  } else if (current_step == 10) {
    endTutorial();
  } else {
    location.replace("/hedy");
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
    $('#tutorial-pop-up').css({'top': '70%'});
  } else if (direction == "middle") {
    $('#tutorial-pop-up').css({'top': '50%'});
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

