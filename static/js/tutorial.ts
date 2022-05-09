import {theGlobalEditor} from "./app";

let current_step = 0;

// We call this function on load -> customize click event of the tutorial button
(function() {
  $('#tutorial_next_button').off('click').on('click', () => {
    $('#tutorial-pop-up').hide();
    callNextStep();
  });
})();

function codeEditorStep() {
  $('#editor').addClass("z-30");
  $('#editor-area').show();
  relocatePopup(70, 20);
  tutorialPopup("De code editor", "In dit venster schrijf je alle code, probeer maar wat in te vullen!");
}

function codeOutputStep() {
  $('#code_output').addClass("z-30");
  $('#code_output').show();
  $('#variables_container').hide();

  relocatePopup(30, 20);
  tutorialPopup("Het output venster", "De code die je uitvoert wordt hier weergegeven.");
}

function runButtonStep() {
  $('#code_related_buttons').show();
  $('#runButtonContainer').addClass("z-30");

  relocatePopup(50, 20);
  tutorialPopup("De uitvoer knop", "Met deze knop kun je een programma uitvoeren, zullen we het proberen?");
}

function tryRunButtonStep() {
  $('#editor').addClass("z-30");
  $('#code_output').addClass("z-30");

  theGlobalEditor?.setValue("print Hallo wereld!\nprint Ik volg de Hedy tutorial");
  theGlobalEditor?.setOptions({readOnly: true});

  relocatePopup(50, 60);
  tutorialPopup("Probeer het uit!", "Voer het programma uit, klik op 'volgende stap' als je klaar bent.");
}

function levelDefaultStep() {
  $('#adventures').show();
  // Hide all tabs except the default level one
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') != "default") {
      $(this).hide();
    } else {
      $(this).addClass("z-30");
    }
  });

  relocatePopup(50, 60);
  tutorialPopup("Level uitleg", "In het eerste tabje vind je altijd de level uitleg. Hier worden in elk level de nieuwe commando's uitgelegd.");
}

function adventureTabsStep() {
  // Show all tabs except the quiz one
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') != "quiz") {
      $(this).addClass("z-30");
      $(this).show();
      if ($(this).attr('data-tab') == "story") {
        // Set to false, prevent "are you sure you want to switch without saving" pop-up
        window.State.unsaved_changes = false;
        $(this).click();
      }
    }
    if ($(this).attr('data-tab') == "default") {
      $(this).removeClass("z-30");
    }
  });

  tutorialPopup("Avonturen", "De andere tabjes bevatten avonturen, deze kun je per level maken. Ze gaan van makkelijk naar moeilijk!");
}

function quizTabStep() {
  // Show all tabs (including the quiz one) -> only highlight the quiz tab
  $('.tab').show();
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "quiz") {
      $(this).addClass("z-30");
    } else {
      $(this).removeClass("z-30");
    }
  });

  relocatePopup(50, 10);
  tutorialPopup("Quiz", "Aan het einde van elk level kun je een quiz maken, zo kun je goed testen of je alles snapt!");
}

function saveShareStep() {
  $('#level-header').addClass("z-30");
  $('#cheatsheet_container').hide();

  relocatePopup(50, 20);
  tutorialPopup("Opslaan en delen", "Je kunt al jouw gemaakt programma's opslaan en delen met andere Hedy gebruikers.");
}

function cheatsheetStep() {
  $('#cheatsheet_container').addClass("z-30");
  $('#cheatsheet_container').show();
  $('#cheatsheet_dropdown').addClass("z-50");
  $('#cheatsheet_dropdown').show();

  relocatePopup(50, 20);
  tutorialPopup("Spiekbriefje", "Als je iets bent vergeten kun je het spiekbriefje gebruiken om te kijken welke commando's je mag gebruiken.");
}

function endTutorial() {
  $('#cheatsheet_dropdown').removeClass("z-50");
  $('#cheatsheet_dropdown').hide();

  relocatePopup(50, 20);
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

function relocatePopup(x: number, y: number) {
  $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  if (x && y) {
    let left = x.toString() + "%"
    let top = y.toString() + "%"
    $('#tutorial-pop-up').css({'top': top, 'left': left});
  }

}

function tutorialPopup(title: string, message: string) {
  $('#tutorial_title').text(title);
  $('#tutorial_text').text(message);
  //$('#tutorial-pop-up').fadeIn(1500);
  $('#tutorial-pop-up').show(); //Use show() for debugging purposes
}

export function startTutorial() {
  $('#tutorial-mask').show();
  $('#adventures').hide();
  tutorialPopup("Welkom bij Hedy!", "In deze uitleg leggen we stap voor stap uit wat je allemaal kunt doen");
}

