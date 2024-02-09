var $builtinmodule = function (name) {
    var mod = {};

    mod.clear = new Sk.builtin.func(function () {
        $('#output').text('');
    });

    function keyBoardInputPromise(key, if_body, else_body) {
      $('#keybinding-modal').show();
      return new Promise((resolve, reject) => {
        window.addEventListener("keydown", (event) => {
          if (event.key === key.v){
            Sk.misceval.callOrSuspend(if_body);
          } else {
            Sk.misceval.callOrSuspend(else_body);
          }

          $('#keybinding-modal').hide();
          resolve();
        }, { once: true });
      })
    }

    mod.if_pressed = new Sk.builtin.func(function (key, if_body, else_body) {
        return new Sk.misceval.promiseToSuspension(keyBoardInputPromise(
            key, if_body, else_body
        ).then(() => Sk.builtin.none.none$));
    });

    return mod;
};
