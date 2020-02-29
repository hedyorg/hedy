var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
// editor.session.setMode("ace/mode/javascript");

// Here's everything you need to run a python program in skulpt
// grab the code from your textarea
// get a reference to your pre element for output
// configure the output function
// call Sk.importMainWithBody()

function print_demo() {
  var editor = ace.edit("editor");
  editor.setValue("print Hallo welkom bij Hedy");
}

function ask_demo() {
  var editor = ace.edit("editor");
  editor.setValue("ask Wat is je lievelingskleur");
}

function echo_demo() {
  var editor = ace.edit("editor");
  editor.setValue("ask Wat is je lievelingskleur\necho je lievelingskleur is ");
}

function runit(level) {
  error.hide();
  try {
    // var prog = document.getElementById("editor").value;

    var editor = ace.edit("editor");
    var prog = editor.getValue();

    console.log('Origineel programma:\n', prog);

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
    inputfun: inputFromModal,
    inputfunTakesPrompt: true,
  });

  Sk.misceval.asyncToPromise(function () {
    return Sk.importMainWithBody("<stdin>", false, code, true);
  }).then(function(mod) {
    console.log('Programma klaar');
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
