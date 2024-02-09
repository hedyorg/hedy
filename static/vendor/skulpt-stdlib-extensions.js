var $builtinmodule = function (name) {
    var mod = {};

    mod.clear = new Sk.builtin.func(function () {
        $('#output').text('');
    });

    mod.if_pressed = new Sk.builtin.func(function (key, if_body, else_body) {
        window.addEventListener("keydown", (event) => {
          if (event.key === key){
            sk.misceval.callOrSuspend(if_body);
          } else {
            sk.misceval.callOrSuspend(else_body);
          }
        }, { once: true });
    });

    return mod;
};
