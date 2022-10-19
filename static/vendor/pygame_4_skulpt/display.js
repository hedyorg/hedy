var $builtinmodule = function (name) {
    var mod = {};
    mod.init = new Sk.builtin.func(function () {
        mod.__is_initialized = true;
        return Sk.builtin.none.none$;
    });
    mod.quit = new Sk.builtin.func(function () {
        mod.__is_initialized = false;
        return Sk.builtin.none.none$;
    });
    mod.get_init = new Sk.builtin.func(function () {
        if (mod.__is_initialized) {
            return Sk.ffi.remapToPy(true);
        }
        return Sk.ffi.remapToPy(false);
    });
    mod.set_mode = new Sk.builtin.func(function (size, flags) {
        var f = 0;
        if (flags !== undefined) {
            f = Sk.ffi.remapToJs(flags);
        }
        if (f & PygameLib.constants.FULLSCREEN) {
            mod.surface = Sk.misceval.callsim(PygameLib.SurfaceType, size, true, true);
        } else {
            mod.surface = Sk.misceval.callsim(PygameLib.SurfaceType, size, false, true);
        }
        PygameLib.surface = mod.surface;
        return mod.surface;
    });
    mod.get_surface = new Sk.builtin.func(function () {
        return PygameLib.surface;
    });
    mod.update = new Sk.builtin.func(function () {
        Sk.misceval.callsim(mod.surface.update, mod.surface);
    });
    mod.flip = new Sk.builtin.func(function () {
        Sk.misceval.callsim(mod.surface.update, mod.surface);
    });
    mod.set_caption = new Sk.builtin.func(function (caption) {
        PygameLib.caption = Sk.ffi.remapToJs(caption);
        if (Sk.title_container) {
            Sk.title_container.innerText = PygameLib.caption;
        }
    });
    mod.get_caption = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(PygameLib.caption);
    });
    mod.get_active = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(document.hasFocus());
    });
    return mod;
};
