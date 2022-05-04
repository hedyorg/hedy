
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
    $('#editor-area').show();
    $('#code_output').hide();
    $('#code_related_buttons').hide();
    relocatePopup("right");
    tutorialPopup("De code editor", "In dit venster schrijf je alle code, probeer maar wat in te vullen!");
  }
  // Step 2: Show the output window

  // Step 3: Show the run button

  // Step 4: Show the adventures

  // Step 5: Show the cheatsheet
}

function relocatePopup(direction: string) {
  $('tutorial-pop-up').removeAttr('style');
  if (direction == "left") {
      $('tutorial-pop-up').attr('style', 'width: 500px; top: 20%; left: 20%; transform: translate(-50%, -50%);');
  } else if (direction == "right") {
      $('tutorial-pop-up').attr('style', 'width: 500px; top: 20%; left: 80%; transform: translate(-50%, -50%);');
  } else if (direction == "button") {
      $('tutorial-pop-up').attr('style', 'width: 500px; top: 80%; left: 50%; transform: translate(-50%, -50%);');
  } else {
      $('tutorial-pop-up').attr('style', 'width: 500px; top: 20%; left: 50%; transform: translate(-50%, -50%);');
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

