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
    var name_js = Sk.ffi.remapToJs(name);
    button.classList.add("blue-btn");
    button.innerText = name;
    button.onclick = function () {
        button_click(name);
    };
    document.getElementById("dynamic-buttons").appendChild(button);

    document.getElementById("dynamic-buttons").style.display = "";
}

var button_click = function (name) {
    var name_js = Sk.ffi.remapToJs(name);

    // For this to work the first element of e needs to be a constant indicating
    // this event is from a button, to make sure it is unique we use USEREVENT
    // the dictionary can then be filled with whatever data we need.
    var e = [PygameLib.constants.USEREVENT, { key: name }];
    PygameLib.eventQueue.unshift(e);
}
