var $builtinmodule = function (name) {
    mod = {};
    mod.get_pressed = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(PygameLib.mouseData["button"]);
    });
    mod.get_pos = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(PygameLib.mouseData["pos"]);
    });
    mod.get_rel = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(PygameLib.mouseData["rel"]);
    });
    mod.set_pos = new Sk.builtin.func(function (x, y) {
        if (Sk.abstr.typeName(x) === "tuple" && y === undefined) {
            var xy = Sk.ffi.remapToJs(x);
            x = xy[0];
            y = xy[1];
        } else if (Sk.abstr.typeName(x) === "int" && Sk.abstr.typeName(y) === "int") {
            x = Sk.ffi.remapToJs(x);
            y = Sk.ffi.remapToJs(y);
        } else {
            throw new Sk.builtin.TypeError("invalid position argument for set_pos");
        }
        PygameLib.mouseData["pos"] = [x, y];
    });
    mod.set_visible = new Sk.builtin.func(function (b) {
        if (Sk.ffi.remapToJs(b)) {
            document.body.style.cursor = '';
        } else {
            document.body.style.cursor = 'none';
        }
    });
    mod.get_focused = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(document.hasFocus());
    });
    mod.set_cursor = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    mod.get_cursor = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    return mod;
};
