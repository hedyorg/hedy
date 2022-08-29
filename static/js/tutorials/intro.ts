import {runit, theGlobalEditor} from "../app";
import "./utils";

    function codeEditorStep() {
      $('#editor').addClass("z-40");
      addHighlightBorder("editor");

      relocatePopup(65, 30);
      theGlobalEditor?.setValue("print ___");
      tutorialPopup(current_step);
    }

    function codeOutputStep() {
      removeBorder("editor");
      $('#code_output').addClass("z-40");
      addHighlightBorder("code_output");

      runit ("1", "en", "", function () {
        $ ('#output').focus ();
      });

      relocatePopup(35, 30);
      tutorialPopup(current_step);
    }

    function runButtonStep() {
      removeBorder("code_output");
      $('#code_related_buttons').show();
      $('#runButtonContainer').addClass("z-40");
      addHighlightBorder("runButtonContainer");

      relocatePopup(50, 30);
      tutorialPopup(current_step);
    }

    function tryRunButtonStep() {
      $.ajax({
          type: 'GET',
          url: '/get_tutorial_step/intro/code_snippet/',
          dataType: 'json'
        }).done(function(response: any) {
           theGlobalEditor?.setValue(response.code);
        }).fail(function() {
           theGlobalEditor?.setValue("print Hello world!\nprint I'm learning Hedy with the tutorial!");
        });

      relocatePopup(50, 70);
      tutorialPopup(current_step);
    }

    function speakAloudStep() {
      removeBorder("runButtonContainer");
      $('#editor').removeClass('z-40');
      $('#code_output').removeClass('z-40');
      $('#runButtonContainer').removeClass('z-40');

      $('#speak_container').addClass('z-40 bg-white relative');

      addHighlightBorder("speak_container");

      relocatePopup(50, 30);
      tutorialPopup(current_step);
    }

    function runSpeakAloudStep() {
      $('#editor').addClass('z-40');
      $('#code_output').addClass('z-40');
      $('#runButtonContainer').addClass('z-40');

      relocatePopup(50, 70);
      tutorialPopup(current_step);
    }

    function nextLevelStep() {
      removeBorder("speak_container");
      $('#editor').removeClass('z-40');
      $('#code_output').removeClass('z-40');
      $('#runButtonContainer').removeClass('z-40');
      $('#speak_container').removeClass('z-40 bg-white relative');

      $('#next_level_button').addClass("z-40");
      $('#next_level_button').removeAttr('onclick');
      addHighlightBorder("next_level_button");

      relocatePopup(50, 30);
      tutorialPopup(current_step);
    }

    function levelDefaultStep() {
      removeBorder("next_level_button");
      $('#next_level_button').removeClass('z-40');

      $('#code_content_container').addClass('z-40');
      $('#adventures').addClass('z-40 bg-gray-100');
      $('#adventures').show();

      // Set to false, prevent "are you sure you want to switch without saving" pop-up
      window.State.unsaved_changes = false;

      addHighlightBorder("adventures");
      relocatePopup(50, 40);
      tutorialPopup(current_step);
    }

    function adventureTabsStep() {
      $('#adventures-buttons').children().each(function() {
        if ($(this).attr('data-tab') == "story") {
          // Set to false, prevent "are you sure you want to switch without saving" pop-up
          window.State.unsaved_changes = false;
          $(this).click();
        }
      });

      tutorialPopup(current_step);
    }

    function quizTabStep() {
      tutorialPopup(current_step);
    }

    function saveShareStep() {
      removeBorder("adventures");
      $('#code_content_container').removeClass('z-40');
      $('#level-header').addClass("z-40");
      $('#cheatsheet_container').hide();
      addHighlightBorder("level-header");

      $('#save_program_button').removeAttr('onclick');
      $('#share_program_button').removeAttr('onclick');

      relocatePopup(50, 30);
      tutorialPopup(current_step);
    }

    function cheatsheetStep() {
      $('#cheatsheet_container').show();
      $('#code_output').removeClass('z-40');
      $('#adventures').removeClass('z-40');
      $('#cheatsheet_dropdown').addClass('z-40');
      $('#cheatsheet_dropdown').show();

      tutorialPopup(current_step);
    }

    function endTutorial() {
      removeBorder("level-header");
      $('#level-header').removeClass('z-40');
      $('#cheatsheet_dropdown').removeClass('z-40');
      $('#cheatsheet_dropdown').hide();

      relocatePopup(50, 15);
      tutorialPopup(current_step);
    }
