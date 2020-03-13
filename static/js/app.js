var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
// editor.session.setMode("ace/mode/javascript");

// Here's everything you need to run a python program in skulpt
// grab the code from your textarea
// get a reference to your pre element for output
// configure the output function
// call Sk.importMainWithBody()

function print_demo(level) {

  if (level == 1 || level == 2){
    var editor = ace.edit("editor");
    editor.setValue("print Hallo welkom bij Hedy!");
  }

}

function is_demo(level) {
  if (level == 1){
    console.log('A demo is tried for is at a level where it is not yet available');
  }
  if (level == 2){
      var editor = ace.edit("editor");
      editor.setValue("naam is Hedy");
  }
}

function echo_demo(level) {
  if (level == 1 || level == 2){
    var editor = ace.edit("editor");
    editor.setValue("ask Wat is je lievelingskleur?\necho je lievelingskleur is");
  }
}

function ask_demo(level) {
  if (level == 1 || level == 2){
    var editor = ace.edit("editor");
    editor.setValue("ask Wat is je lievelingskleur?");
  }
}

function goto(level, lang) {
    var url = '/?level=' + level.toString();
    if (lang){
      url += '&lang=' + lang;
    }
    window.location.href = url;
}

function runit(level, lang) {
  error.hide();
  try {
    x = $.getJSON('/error_messages.js', {
      lang: lang,
    }).done(function(response) {
      console.log('Response', response);
      error_messages = response;
    });

    var editor = ace.edit("editor");
    var prog = editor.getValue();

    console.log('Original program:\n', prog);

    $.getJSON('/parse/', {
      level: level.toString(),
      code: prog,
    }).done(function(response) {
      console.log('Response', response);
      if (response.Error) {
        error.show('De server kon het programma niet vertalen', response.Error);
      } else {
        runPythonProgram(response.Code);
      }
    }).fail(function(err) {
      console.error(err);
      error.show('We konden niet goed met de server praten', JSON.stringify(err));
    });

  } catch (e) {
    console.error(e);
    error.show('Misschien hebben wij een klein programmeerfoutje gemaakt', e.message);
  }
}

function runPythonProgram(code) {
  const outputDiv = $('#output');
  outputDiv.empty();

  Sk.pre = "output";
  Sk.configure({
    output: outf,
    read: builtinRead,
    inputfun: inputFromInlineModal,
    inputfunTakesPrompt: true,
  });

  Sk.misceval.asyncToPromise(function () {
    return Sk.importMainWithBody("<stdin>", false, code, true);
  }).then(function(mod) {
    console.log('Program executed');
  }).catch(function(err) {
    console.log(err);
    addToOutput(JSON.stringify(err), 'red');
  });

  function addToOutput(text, color) {
    $('<span>').text(text).css({ color }).appendTo(outputDiv);
  }

  // output functions are configurable.  This one just appends some text
  // to a pre element.
  function outf(text) {
    addToOutput(text, 'white');
  }

  function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
  }

  /**
   * Get the input inline in the terminal
   *
   * Render the prompt to the terminal, add an inputbox where the user can
   * type, and replace the inputbox with static text after they hit enter.
   */
  function inputFromTerminal(prompt) {
    return new Promise(function(ok) {
      addToOutput(prompt + '\n', 'white');
      const input = $('<input>').attr('placeholder', 'Typ hier je antwoord').appendTo(outputDiv).focus();

      // When enter is pressed, turn the input box into a regular
      // span and resolve the promise
      input.on('keypress', function(e) {
        if (e.which == 13 /* ENTER */) {
          const text = input.val();

          input.remove();
          addToOutput(text + '\n', 'yellow');
          ok(text);
        }
      });
    });
  }

  function inputFromModal(prompt) {
    return new Promise(function(ok) {
      const input = $('#ask-modal input[type="text"]');
      $('#ask-modal .caption').text(prompt);
      input.val('');
      setTimeout(function() {
        input.focus();
      }, 0);
      $('#ask-modal form').one('submit', function(event) {
        event.preventDefault();
        $('#ask-modal').hide();
        ok(input.val());
        return false;
      });
      $('#ask-modal').show();
    });
  }

  function inputFromInlineModal(prompt) {
    return new Promise(function(ok) {
      const input = $('#inline-modal input[type="text"]');
      $('#inline-modal .caption').text(prompt);
      input.val('');
      setTimeout(function() {
        input.focus();
      }, 0);
      $('#inline-modal form').one('submit', function(event) {
        event.preventDefault();
        $('#inline-modal').hide();
        ok(input.val());
        return false;
      });
      $('#inline-modal').show();
    });
  }
}

var error = {
  hide() {
    $('#errorbox').hide();
  },

  show(caption, message) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').text(message);
    $('#errorbox').show();
  }
};
