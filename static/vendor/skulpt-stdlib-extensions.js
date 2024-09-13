var $builtinmodule = function (name) {
    var mod = {};

    mod.clear = new Sk.builtin.func(function () {
        $('#output').text('');
    });

    function animateKeys(event) {
      const keyColors = ['#cbd5e0', '#bee3f8', '#4299e1', '#ff617b', '#ae81ea', '#68d391'];
      const output = $("#output");
  
      if (output !== null) {
        let keyElement = $("<div></div>");
        output.append(keyElement);
  
        keyElement.text(event.key);
        keyElement.css('color', keyColors[Math.floor(Math.random() * keyColors.length)]);
        keyElement.addClass('animate-keys')
  
        setTimeout(function () {
          keyElement.remove()
        }, 1500);
      }
    }

    var ongoingIfPressedCall = false;

    function callIfPressedFunc(name, resolve, reject) {
      var f = Sk.misceval.loadname(name, Sk.globals);
      var currentProgram = window.sessionStorage.getItem("currentProgram");

      Sk.misceval.asyncToPromise(() =>
        Sk.misceval.callOrSuspend(f), {}, currentProgram).then(() => {
          resolve();
        }).catch((e) => {
          reject(e);
        }).finally(() => {
          ongoingIfPressedCall = false;
        });
    }

    function keyBoardInputPromise(if_pressed_mapping) {
      ongoingIfPressedCall = true;
      $('#keybinding_modal').show();
      return new Promise((resolve, reject) => {
        window.addEventListener("keydown", (event) => {
          try {
            let pressed_mapped_key = false;

            for (const [key, value] of Object.entries(if_pressed_mapping.entries)) {
              // if the mapped key is a variable, we retrieve variable value and use that
              // if the mapped key is not a variable, use it as a char
              const charOrVar = value[0].v;
              let mapLetterKey = charOrVar;
              if (Object.hasOwn(Sk.globals, charOrVar)) {
                if (Sk.globals[charOrVar].hasOwnProperty('v')) {
                  mapLetterKey = Sk.globals[charOrVar].v;
                } else {
                  mapLetterKey = Sk.globals[charOrVar].$d.entries['data'][1].v;
                }
              }

              if (event.key === `${mapLetterKey}`) {
                pressed_mapped_key = true;
                callIfPressedFunc(value[1].v, resolve, reject);
              }
            }

            if (!pressed_mapped_key) {
              callIfPressedFunc(if_pressed_mapping.entries['else'][1].v, resolve, reject);
            }
          } catch (err) {
            ongoingIfPressedCall = false;
            reject(err);
          } finally {
            $('#keybinding_modal').hide();
          }
        }, { once: true });
      })
    }

    mod.if_pressed = new Sk.builtin.func(function (if_pressed_mapping) {
        document.onkeydown = animateKeys;
        return new Sk.misceval.promiseToSuspension(
          keyBoardInputPromise(if_pressed_mapping)
          .then(() => { return Sk.builtin.none.none$ })
          .finally(() => { document.onkeydown = null;})
        );
    });

    return mod;
};
