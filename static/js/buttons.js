// This file defines a module that can be imported as an external module
// in Python through Skulpt.
//
// The module is defined in a variable called $builtinmodule (that is a
// function for some reason) in which a variable mod is created containing all
// the member functions and classes of that module.

var $builtinmodule = function (name) {
    var mod = {};

    mod.add = new Sk.builtin.func(buttons_add);

    return mod;
};

function buttons_add(name) {
  let button = document.createElement("button");
  button.innerText = name;
  button.classList.add("blue-btn");
  button.onclick = function () {
    console.log(name, "ingedrukt!");
  };
  document.getElementById("dynamic-buttons").appendChild(button);

  document.getElementById("dynamic-buttons").style.display = "";
}
