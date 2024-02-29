var $builtinmodule = function (name) {
    var mod = {};

    mod.clear = new Sk.builtin.func(function () {
        $('#output').text('');
    });

    function keyBoardInputPromise(if_pressed_mapping) {
      $('#keybinding-modal').show();
      return new Promise((resolve, reject) => {
        window.addEventListener("keydown", (event) => {
          let pressed_mapped_key = false;

          for (const [key, value] of Object.entries(if_pressed_mapping.entries)) {
            // If mapped key is a variable (not char), we retrieve variable value and use that
            // otherwise if char, use that.
            const charOrVar = value[0].v;
            let mapLetterKey = Object.hasOwn(Sk.globals, charOrVar) ? Sk.globals[charOrVar].v : charOrVar;

            if (event.key === `${mapLetterKey}`){
              pressed_mapped_key = true;
              Sk.misceval.callOrSuspend(Sk.globals[value[1].v]);
            }
          }

          if (!pressed_mapped_key){
            Sk.misceval.callOrSuspend(Sk.globals[if_pressed_mapping.entries['else'][1].v]);
          }

          $('#keybinding-modal').hide();
          resolve();
        }, { once: true });
      })
    }

    mod.if_pressed = new Sk.builtin.func(function (if_pressed_mapping) {
        return new Sk.misceval.promiseToSuspension(keyBoardInputPromise(
            if_pressed_mapping
        ).then(() => Sk.builtin.none.none$));
    });

    return mod;
};
