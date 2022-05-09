import {modal} from "./modal";
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
  tutorialPopup(1);
}

function codeOutputStep() {
  $('#code_output').addClass("z-30");
  $('#code_output').show();
  $('#variables_container').hide();

  relocatePopup(30, 20);
  tutorialPopup(2);
}

function runButtonStep() {
  $('#code_related_buttons').show();
  $('#runButtonContainer').addClass("z-30");

  relocatePopup(50, 20);
  tutorialPopup(3);
}

function tryRunButtonStep() {
  $('#editor').addClass("z-30");
  $('#code_output').addClass("z-30");

  theGlobalEditor?.setValue("print Hallo wereld!\nprint Ik volg de Hedy tutorial");
  theGlobalEditor?.setOptions({readOnly: true});

  relocatePopup(50, 60);
  tutorialPopup(4);
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
  tutorialPopup(5);
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

  tutorialPopup(6);
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
  tutorialPopup(7);
}

function saveShareStep() {
  $('#level-header').addClass("z-30");
  $('#cheatsheet_container').hide();

  relocatePopup(50, 20);
  tutorialPopup(8);
}

function cheatsheetStep() {
  $('#cheatsheet_container').addClass("z-30");
  $('#cheatsheet_container').show();
  $('#cheatsheet_dropdown').addClass("z-50");
  $('#cheatsheet_dropdown').show();

  relocatePopup(50, 20);
  tutorialPopup(9);
}

function endTutorial() {
  $('#cheatsheet_dropdown').removeClass("z-50");
  $('#cheatsheet_dropdown').hide();

  relocatePopup(50, 20);
  tutorialPopup(10);
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

function tutorialPopup(step: number) {
    $.ajax({
      type: 'GET',
      url: '/get_tutorial_step/' + step.toString(),
      dataType: 'json'
    }).done(function(response: any) {
        $('#tutorial_title').text(response[0]);
        $('#tutorial_text').text(response[1]);
        $('#tutorial-pop-up').fadeIn(1500);
    }).fail(function(response) {
      modal.alert(response.responseText, 3000, true);
    });
}

export function startTutorial() {
  $('#tutorial-mask').show();
  $('#adventures').hide();
  tutorialPopup(0);
}

