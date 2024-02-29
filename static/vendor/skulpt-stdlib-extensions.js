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
            if (event.key === key){
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
