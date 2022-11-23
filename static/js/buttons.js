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
