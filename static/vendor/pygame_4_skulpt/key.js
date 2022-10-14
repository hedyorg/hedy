var $builtinmodule = function (name) {
    mod = {};
    mod.set_repeat = new Sk.builtin.func(function (delay, interval) {
        if (delay !== undefined) {
            PygameLib.repeatKeys = true;
        } else {
            PygameLib.repeatKeys = false;
        }
    });
    mod.get_repeat = new Sk.builtin.func(function () {
        if (PygameLib.repeatKeys) {
            return Sk.builtin.tuple([1, 1]);
        } else {
            return Sk.builtin.tuple([0, 0]);
        }
    });
    mod.get_focused = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(document.hasFocus());
    });
    mod.get_pressed = new Sk.builtin.func(function () {
        var pressed = new Array(PygameLib.constants.K_LAST + 1).fill(false);
        for (var key = 0; key < pressed.length; key++) {
            if (PygameLib.pressedKeys[key])
                pressed[key] = true;
        }
        return Sk.ffi.remapToPy(pressed);
    });
    mod.get_mods = new Sk.builtin.func(function () {
        var mask = 0;
        for (var i = 0; i < PygameLib.eventQueue.length; i++) {
            for (var j = 0; j < keyboardModifierKeys.length; j++) {
                if (PygameLib.eventQueue[i][1].key === keyboardModifierKeys[j]) {
                    mask &= 1 << j;
                }
            }
        }
        return Sk.ffi.remapToPy(mask);
    });
    mod.set_mods = new Sk.builtin.func(function (m) {
        var mask = Sk.ffi.remapToJs(m);
        for (var i = 0; i < keyboardModifierKeys.length; i++) {
            if (mask & (1 << i)) {
                PygameLib.eventQueue.unshift([PygameLib.constants.KEYDOWN, {key: keyboardModifierKeys[i]}]);
            }
        }

    });
    mod.name = new Sk.builtin.func(function (idx) {
        var i = Sk.ffi.remapToJs(idx);
        if (i < 0 || i >= 323) {
            return Sk.ffi.remapToPy("unknown key");
        }
        return Sk.ffi.remapToPy(keyToName[i]);
    });
    return mod;
};

keyToName = ['unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'backspace', 'tab', 'unknown key', 'unknown key', 'clear', 'return', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'pause', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'escape', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'space', '!', '"', '#', '$', 'unknown key', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'delete', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key', 'unknown key',
    'world 0', 'world 1', 'world 2', 'world 3', 'world 4', 'world 5', 'world 6', 'world 7', 'world 8', 'world 9',
    'world 10', 'world 11', 'world 12', 'world 13', 'world 14', 'world 15', 'world 16', 'world 17', 'world 18',
    'world 19', 'world 20', 'world 21', 'world 22', 'world 23', 'world 24', 'world 25', 'world 26', 'world 27',
    'world 28', 'world 29', 'world 30', 'world 31', 'world 32', 'world 33', 'world 34', 'world 35', 'world 36',
    'world 37', 'world 38', 'world 39', 'world 40', 'world 41', 'world 42', 'world 43', 'world 44', 'world 45',
    'world 46', 'world 47', 'world 48', 'world 49', 'world 50', 'world 51', 'world 52', 'world 53', 'world 54',
    'world 55', 'world 56', 'world 57', 'world 58', 'world 59', 'world 60', 'world 61', 'world 62', 'world 63',
    'world 64', 'world 65', 'world 66', 'world 67', 'world 68', 'world 69', 'world 70', 'world 71', 'world 72',
    'world 73', 'world 74', 'world 75', 'world 76', 'world 77', 'world 78', 'world 79', 'world 80', 'world 81',
    'world 82', 'world 83', 'world 84', 'world 85', 'world 86', 'world 87', 'world 88', 'world 89', 'world 90',
    'world 91', 'world 92', 'world 93', 'world 94', 'world 95', '[0]', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]',
    '[7]', '[8]', '[9]', '[.]', '[/]', '[*]', '[-]', '[+]', 'enter', 'equals', 'up', 'down', 'right', 'left', 'insert',
    'home', 'end', 'page up', 'page down', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'f13', 'f14', 'f15', 'unknown key', 'unknown key', 'unknown key', 'numlock', 'caps lock', 'scroll lock',
    'right shift', 'left shift', 'right ctrl', 'left ctrl', 'right alt', 'left alt', 'right meta', 'left meta',
    'left super', 'right super', 'alt gr', 'compose', 'help', 'print screen', 'sys req', 'break', 'menu', 'power',
    'euro', 'undo', 'unknown key'];
var keyboardModifierKeys = [PygameLib.constants.K_LSHIFT, PygameLib.constants.K_RSHIFT, 0, 0, 0, 0,
    PygameLib.constants.K_LCTRL, PygameLib.constants.K_RCTRL, PygameLib.constants.K_LALT, PygameLib.constants.K_RALT,
    PygameLib.constants.K_LMETA, PygameLib.constants.K_RMETA, 0, PygameLib.constants.K_CAPSLOCK,
    PygameLib.constants.K_NUMLOCK, PygameLib.constants.K_MODE];

