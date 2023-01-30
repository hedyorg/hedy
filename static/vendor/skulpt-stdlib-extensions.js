var $builtinmodule = function (name) {
    var mod = {};
    mod.clear = new Sk.builtin.func(function () {
        $('#output').text('');
    });
    return mod;
};
