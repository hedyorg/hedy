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
        document.onkeydown = animateKeys;
        return new Sk.misceval.promiseToSuspension(keyBoardInputPromise(
            if_pressed_mapping
        ).then(() => {document.onkeydown = null; return Sk.builtin.none.none$}));
    });

    return mod;
};
