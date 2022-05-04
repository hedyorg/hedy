
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
  // Step 1: show the code editor
  if (current_step == 1) {
    console.log("We komen in stap 1!");
    $('#editor-area').show();
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

