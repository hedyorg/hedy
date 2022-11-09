// Queue interface for the frontend
Sk.insertPyGameEvent = function (eventName) {
    var e = [];
    switch (eventName) {
        case "left":
            e = [PygameLib.constants.KEYDOWN, { key: PygameLib.constants.K_LEFT }];
            break;
        case "right":
            e = [PygameLib.constants.KEYDOWN, { key: PygameLib.constants.K_RIGHT }];
            break;
        case "up":
            e = [PygameLib.constants.KEYDOWN, { key: PygameLib.constants.K_UP }];
            break;
        case "down":
            e = [PygameLib.constants.KEYDOWN, { key: PygameLib.constants.K_DOWN }];
            break;
        case "quit":
            e = [PygameLib.constants.QUIT, { key: PygameLib.constants.K_ESCAPE }];
            break;
    }
    PygameLib.eventQueue.unshift(e);
};

var PygameLib = {},
    rPyStr = new Sk.builtin.str("r"),
    gPyStr = new Sk.builtin.str("g"),
    bPyStr = new Sk.builtin.str("b"),
    aPyStr = new Sk.builtin.str("a"),
    leftPyStr = new Sk.builtin.str("left"),
    topPyStr = new Sk.builtin.str("top"),
    widthPyStr = new Sk.builtin.str("width"),
    heightPyStr = new Sk.builtin.str("height"),
    lenPyStr = new Sk.builtin.str("len");

PygameLib.running = false;


PygameLib.extract_color = function (color) {
    var color_js = [0, 0, 0, 0];
    if (Sk.abstr.typeName(color) === "Color") {
        color_js[0] = Sk.ffi.remapToJs(Sk.abstr.gattr(color, rPyStr, false));
        color_js[1] = Sk.ffi.remapToJs(Sk.abstr.gattr(color, gPyStr, false));
        color_js[2] = Sk.ffi.remapToJs(Sk.abstr.gattr(color, bPyStr, false));
        color_js[3] = Sk.ffi.remapToJs(Sk.abstr.gattr(color, aPyStr, false));
    } else {
        color_js = Sk.ffi.remapToJs(color);
        if (color_js.length === 3) color_js.push(1);
    }
    return color_js;
};

PygameLib.extract_rect = function (rect) {
    var rect_js = [0, 0, 0, 0];
    if (Sk.abstr.typeName(rect) === "Rect") {
        rect_js[0] = Sk.ffi.remapToJs(Sk.abstr.gattr(rect, leftPyStr, false));
        rect_js[1] = Sk.ffi.remapToJs(Sk.abstr.gattr(rect, topPyStr, false));
        rect_js[2] = Sk.ffi.remapToJs(Sk.abstr.gattr(rect, widthPyStr, false));
        rect_js[3] = Sk.ffi.remapToJs(Sk.abstr.gattr(rect, heightPyStr, false));
    } else {
        rect_js = Sk.ffi.remapToJs(rect);
    }
    return rect_js;
};

var createKeyboardEvent = function (event) {
    var e;
    var keyPGConstant;
    if (event.type === "keyup") {
        keyPGConstant = PygameLib.constants.KEYUP;
    } else if (event.type === "keydown") {
        keyPGConstant = PygameLib.constants.KEYDOWN;
    }
    var keyId = event.which;


    switch (keyId) {
        case 27:
            return [PygameLib.constants.QUIT, {key: PygameLib.constants.K_ESCAPE}];
        case 37:
            return [keyPGConstant, {key: PygameLib.constants.K_LEFT}];
        case 38:
            return [keyPGConstant, {key: PygameLib.constants.K_UP}];
        case 39:
            return [keyPGConstant, {key: PygameLib.constants.K_RIGHT}];
        case 40:
            return [keyPGConstant, {key: PygameLib.constants.K_DOWN}];
        default:
            var difference = 0;
            if ((event.which <= 90) && (event.which >= 65))
                difference = 32;
            return [keyPGConstant, { key: (event.which + difference)}];
    }
};

function keyEventListener(event) {
    var e = createKeyboardEvent(event);

    if (e[0] === PygameLib.constants.KEYDOWN)
        PygameLib.pressedKeys[e[1].key] = true;
    else if ((e[0] === PygameLib.constants.KEYUP))
        delete PygameLib.pressedKeys[e[1].key];
    if (PygameLib.eventQueue) {
        if (PygameLib.repeatKeys) {
            PygameLib.eventQueue.unshift(e);
        } else {
            if (!('repeat' in event) || !event.repeat) { // Pygame considers autorepeat is turnd of by default
                PygameLib.eventQueue.unshift(e);
            }
        }

    }
    if (PygameLib.running) event.preventDefault();
    return false;
}


// constants
PygameLib.constants = {
    'ACTIVEEVENT': 1,
    'ANYFORMAT': 268435456,
    'ASYNCBLIT': 4,
    'AUDIO_S16': 32784,
    'AUDIO_S16LSB': 32784,
    'AUDIO_S16MSB': 36880,
    'AUDIO_S16SYS': 32784,
    'AUDIO_S8': 32776,
    'AUDIO_U16': 16,
    'AUDIO_U16LSB': 16,
    'AUDIO_U16MSB': 4112,
    'AUDIO_U16SYS': 16,
    'AUDIO_U8': 8,
    'BIG_ENDIAN': 4321,
    'BLEND_ADD': 1,
    'BLEND_MAX': 5,
    'BLEND_MIN': 4,
    'BLEND_MULT': 3,
    'BLEND_PREMULTIPLIED': 17,
    'BLEND_RGBA_ADD': 6,
    'BLEND_RGBA_MAX': 16,
    'BLEND_RGBA_MIN': 9,
    'BLEND_RGBA_MULT': 8,
    'BLEND_RGBA_SUB': 7,
    'BLEND_RGB_ADD': 1,
    'BLEND_RGB_MAX': 5,
    'BLEND_RGB_MIN': 4,
    'BLEND_RGB_MULT': 3,
    'BLEND_RGB_SUB': 2,
    'BLEND_SUB': 2,
    'BUTTON_X1': 6,
    'BUTTON_X2': 7,
    'DOUBLEBUF': 1073741824,
    'FULLSCREEN': -2147483648,
    'GL_ACCELERATED_VISUAL': 15,
    'GL_ACCUM_ALPHA_SIZE': 11,
    'GL_ACCUM_BLUE_SIZE': 10,
    'GL_ACCUM_GREEN_SIZE': 9,
    'GL_ACCUM_RED_SIZE': 8,
    'GL_ALPHA_SIZE': 3,
    'GL_BLUE_SIZE': 2,
    'GL_BUFFER_SIZE': 4,
    'GL_DEPTH_SIZE': 6,
    'GL_DOUBLEBUFFER': 5,
    'GL_GREEN_SIZE': 1,
    'GL_MULTISAMPLEBUFFERS': 13,
    'GL_MULTISAMPLESAMPLES': 14,
    'GL_RED_SIZE': 0,
    'GL_STENCIL_SIZE': 7,
    'GL_STEREO': 12,
    'GL_SWAP_CONTROL': 16,
    'HAT_CENTERED': 0,
    'HAT_DOWN': 4,
    'HAT_LEFT': 8,
    'HAT_LEFTDOWN': 12,
    'HAT_LEFTUP': 9,
    'HAT_RIGHT': 2,
    'HAT_RIGHTDOWN': 6,
    'HAT_RIGHTUP': 3,
    'HAT_UP': 1,
    'HAVE_NEWBUF': 1,
    'HWACCEL': 256,
    'HWPALETTE': 536870912,
    'HWSURFACE': 1,
    'IYUV_OVERLAY': 1448433993,
    'JOYAXISMOTION': 7,
    'JOYBALLMOTION': 8,
    'JOYBUTTONDOWN': 10,
    'JOYBUTTONUP': 11,
    'JOYHATMOTION': 9,
    'KEYDOWN': 2,
    'KEYUP': 3,
    'KMOD_ALT': 768,
    'KMOD_CAPS': 8192,
    'KMOD_CTRL': 192,
    'KMOD_LALT': 256,
    'KMOD_LCTRL': 64,
    'KMOD_LMETA': 1024,
    'KMOD_LSHIFT': 1,
    'KMOD_META': 3072,
    'KMOD_MODE': 16384,
    'KMOD_NONE': 0,
    'KMOD_NUM': 4096,
    'KMOD_RALT': 512,
    'KMOD_RCTRL': 128,
    'KMOD_RMETA': 2048,
    'KMOD_RSHIFT': 2,
    'KMOD_SHIFT': 3,
    'K_0': 48,
    'K_1': 49,
    'K_2': 50,
    'K_3': 51,
    'K_4': 52,
    'K_5': 53,
    'K_6': 54,
    'K_7': 55,
    'K_8': 56,
    'K_9': 57,
    'K_AMPERSAND': 38,
    'K_ASTERISK': 42,
    'K_AT': 64,
    'K_BACKQUOTE': 96,
    'K_BACKSLASH': 92,
    'K_BACKSPACE': 8,
    'K_BREAK': 318,
    'K_CAPSLOCK': 301,
    'K_CARET': 94,
    'K_CLEAR': 12,
    'K_COLON': 58,
    'K_COMMA': 44,
    'K_DELETE': 127,
    'K_DOLLAR': 36,
    'K_DOWN': 274,
    'K_END': 279,
    'K_EQUALS': 61,
    'K_ESCAPE': 27,
    'K_EURO': 321,
    'K_EXCLAIM': 33,
    'K_F1': 282,
    'K_F10': 291,
    'K_F11': 292,
    'K_F12': 293,
    'K_F13': 294,
    'K_F14': 295,
    'K_F15': 296,
    'K_F2': 283,
    'K_F3': 284,
    'K_F4': 285,
    'K_F5': 286,
    'K_F6': 287,
    'K_F7': 288,
    'K_F8': 289,
    'K_F9': 290,
    'K_FIRST': 0,
    'K_GREATER': 62,
    'K_HASH': 35,
    'K_HELP': 315,
    'K_HOME': 278,
    'K_INSERT': 277,
    'K_KP0': 256,
    'K_KP1': 257,
    'K_KP2': 258,
    'K_KP3': 259,
    'K_KP4': 260,
    'K_KP5': 261,
    'K_KP6': 262,
    'K_KP7': 263,
    'K_KP8': 264,
    'K_KP9': 265,
    'K_KP_DIVIDE': 267,
    'K_KP_ENTER': 271,
    'K_KP_EQUALS': 272,
    'K_KP_MINUS': 269,
    'K_KP_MULTIPLY': 268,
    'K_KP_PERIOD': 266,
    'K_KP_PLUS': 270,
    'K_LALT': 308,
    'K_LAST': 323,
    'K_LCTRL': 306,
    'K_LEFT': 276,
    'K_LEFTBRACKET': 91,
    'K_LEFTPAREN': 40,
    'K_LESS': 60,
    'K_LMETA': 310,
    'K_LSHIFT': 304,
    'K_LSUPER': 311,
    'K_MENU': 319,
    'K_MINUS': 45,
    'K_MODE': 313,
    'K_NUMLOCK': 300,
    'K_PAGEDOWN': 281,
    'K_PAGEUP': 280,
    'K_PAUSE': 19,
    'K_PERIOD': 46,
    'K_PLUS': 43,
    'K_POWER': 320,
    'K_PRINT': 316,
    'K_QUESTION': 63,
    'K_QUOTE': 39,
    'K_QUOTEDBL': 34,
    'K_RALT': 307,
    'K_RCTRL': 305,
    'K_RETURN': 13,
    'K_RIGHT': 275,
    'K_RIGHTBRACKET': 93,
    'K_RIGHTPAREN': 41,
    'K_RMETA': 309,
    'K_RSHIFT': 303,
    'K_RSUPER': 312,
    'K_SCROLLOCK': 302,
    'K_SEMICOLON': 59,
    'K_SLASH': 47,
    'K_SPACE': 32,
    'K_SYSREQ': 317,
    'K_TAB': 9,
    'K_UNDERSCORE': 95,
    'K_UNKNOWN': 0,
    'K_UP': 273,
    'K_a': 97,
    'K_b': 98,
    'K_c': 99,
    'K_d': 100,
    'K_e': 101,
    'K_f': 102,
    'K_g': 103,
    'K_h': 104,
    'K_i': 105,
    'K_j': 106,
    'K_k': 107,
    'K_l': 108,
    'K_m': 109,
    'K_n': 110,
    'K_o': 111,
    'K_p': 112,
    'K_q': 113,
    'K_r': 114,
    'K_s': 115,
    'K_t': 116,
    'K_u': 117,
    'K_v': 118,
    'K_w': 119,
    'K_x': 120,
    'K_y': 121,
    'K_z': 122,
    'LIL_ENDIAN': 1234,
    'MOUSEBUTTONDOWN': 5,
    'MOUSEBUTTONUP': 6,
    'MOUSEMOTION': 4,
    'NOEVENT': 0,
    'NOFRAME': 32,
    'NUMEVENTS': 32,
    'OPENGL': 2,
    'OPENGLBLIT': 10,
    'PREALLOC': 16777216,
    'QUIT': 12,
    'RESIZABLE': 16,
    'RLEACCEL': 16384,
    'RLEACCELOK': 8192,
    'SCRAP_BMP': 'image/bmp',
    'SCRAP_CLIPBOARD': 0,
    'SCRAP_PBM': 'image/pbm',
    'SCRAP_PPM': 'image/ppm',
    'SCRAP_SELECTION': 1,
    'SCRAP_TEXT': 'text/plain',
    'SRCALPHA': 65536,
    'SRCCOLORKEY': 4096,
    'SWSURFACE': 0,
    'SYSWMEVENT': 13,
    'TIMER_RESOLUTION': 10,
    'USEREVENT': 24,
    'USEREVENT_DROPFILE': 4096,
    'UYVY_OVERLAY': 1498831189,
    'VIDEOEXPOSE': 17,
    'VIDEORESIZE': 16,
    'YUY2_OVERLAY': 844715353,
    'YV12_OVERLAY': 842094169,
    'YVYU_OVERLAY': 1431918169
}

PygameLib.Colors = {
    'gray17': [43, 43, 43, 255],
    'gold': [255, 215, 0, 255],
    'gray10': [26, 26, 26, 255],
    'yellow': [255, 255, 0, 255],
    'gray11': [28, 28, 28, 255],
    'grey61': [156, 156, 156, 255],
    'grey60': [153, 153, 153, 255],
    'darkseagreen': [143, 188, 143, 255],
    'grey62': [158, 158, 158, 255],
    'grey65': [166, 166, 166, 255],
    'gray12': [31, 31, 31, 255],
    'grey67': [171, 171, 171, 255],
    'grey66': [168, 168, 168, 255],
    'grey69': [176, 176, 176, 255],
    'gray21': [54, 54, 54, 255],
    'lightsalmon4': [139, 87, 66, 255],
    'lightsalmon2': [238, 149, 114, 255],
    'lightsalmon3': [205, 129, 98, 255],
    'lightsalmon1': [255, 160, 122, 255],
    'gray32': [82, 82, 82, 255],
    'green4': [0, 139, 0, 255],
    'gray30': [77, 77, 77, 255],
    'gray31': [79, 79, 79, 255],
    'green1': [0, 255, 0, 255],
    'gray37': [94, 94, 94, 255],
    'green3': [0, 205, 0, 255],
    'green2': [0, 238, 0, 255],
    'darkslategray1': [151, 255, 255, 255],
    'darkslategray2': [141, 238, 238, 255],
    'darkslategray3': [121, 205, 205, 255],
    'aquamarine1': [127, 255, 212, 255],
    'aquamarine3': [102, 205, 170, 255],
    'aquamarine2': [118, 238, 198, 255],
    'papayawhip': [255, 239, 213, 255],
    'black': [0, 0, 0, 255],
    'darkorange3': [205, 102, 0, 255],
    'oldlace': [253, 245, 230, 255],
    'lightgoldenrod4': [139, 129, 76, 255],
    'gray90': [229, 229, 229, 255],
    'orchid1': [255, 131, 250, 255],
    'orchid2': [238, 122, 233, 255],
    'orchid3': [205, 105, 201, 255],
    'grey68': [173, 173, 173, 255],
    'brown': [165, 42, 42, 255],
    'purple2': [145, 44, 238, 255],
    'gray80': [204, 204, 204, 255],
    'antiquewhite3': [205, 192, 176, 255],
    'antiquewhite2': [238, 223, 204, 255],
    'antiquewhite1': [255, 239, 219, 255],
    'paleviovarred3': [205, 104, 137, 255],
    'hotpink': [255, 105, 180, 255],
    'lightcyan': [224, 255, 255, 255],
    'coral3': [205, 91, 69, 255],
    'gray8': [20, 20, 20, 255],
    'gray9': [23, 23, 23, 255],
    'grey32': [82, 82, 82, 255],
    'bisque4': [139, 125, 107, 255],
    'cyan': [0, 255, 255, 255],
    'gray0': [0, 0, 0, 255],
    'gray1': [3, 3, 3, 255],
    'gray6': [15, 15, 15, 255],
    'bisque1': [255, 228, 196, 255],
    'bisque2': [238, 213, 183, 255],
    'bisque3': [205, 183, 158, 255],
    'skyblue': [135, 206, 235, 255],
    'gray': [190, 190, 190, 255],
    'darkturquoise': [0, 206, 209, 255],
    'rosybrown4': [139, 105, 105, 255],
    'deepskyblue3': [0, 154, 205, 255],
    'grey63': [161, 161, 161, 255],
    'indianred1': [255, 106, 106, 255],
    'grey78': [199, 199, 199, 255],
    'lightpink': [255, 182, 193, 255],
    'gray88': [224, 224, 224, 255],
    'gray22': [56, 56, 56, 255],
    'red': [255, 0, 0, 255],
    'grey11': [28, 28, 28, 255],
    'lemonchiffon3': [205, 201, 165, 255],
    'lemonchiffon2': [238, 233, 191, 255],
    'lemonchiffon1': [255, 250, 205, 255],
    'indianred3': [205, 85, 85, 255],
    'viovarred1': [255, 62, 150, 255],
    'plum2': [238, 174, 238, 255],
    'plum1': [255, 187, 255, 255],
    'lemonchiffon4': [139, 137, 112, 255],
    'gray99': [252, 252, 252, 255],
    'grey13': [33, 33, 33, 255],
    'grey55': [140, 140, 140, 255],
    'darkcyan': [0, 139, 139, 255],
    'chocolate4': [139, 69, 19, 255],
    'lightgoldenrodyellow': [250, 250, 210, 255],
    'gray54': [138, 138, 138, 255],
    'lavender': [230, 230, 250, 255],
    'chartreuse3': [102, 205, 0, 255],
    'chartreuse2': [118, 238, 0, 255],
    'chartreuse1': [127, 255, 0, 255],
    'grey48': [122, 122, 122, 255],
    'grey16': [41, 41, 41, 255],
    'thistle': [216, 191, 216, 255],
    'chartreuse4': [69, 139, 0, 255],
    'darkorchid4': [104, 34, 139, 255],
    'grey42': [107, 107, 107, 255],
    'grey41': [105, 105, 105, 255],
    'grey17': [43, 43, 43, 255],
    'dimgrey': [105, 105, 105, 255],
    'dodgerblue4': [16, 78, 139, 255],
    'darkorchid2': [178, 58, 238, 255],
    'darkorchid3': [154, 50, 205, 255],
    'blue': [0, 0, 255, 255],
    'rosybrown2': [238, 180, 180, 255],
    'honeydew': [240, 255, 240, 255],
    'gray18': [46, 46, 46, 255],
    'cornflowerblue': [100, 149, 237, 255],
    'grey91': [232, 232, 232, 255],
    'gray14': [36, 36, 36, 255],
    'gray15': [38, 38, 38, 255],
    'gray16': [41, 41, 41, 255],
    'maroon4': [139, 28, 98, 255],
    'maroon3': [205, 41, 144, 255],
    'maroon2': [238, 48, 167, 255],
    'maroon1': [255, 52, 179, 255],
    'gray13': [33, 33, 33, 255],
    'gold3': [205, 173, 0, 255],
    'gold2': [238, 201, 0, 255],
    'gold1': [255, 215, 0, 255],
    'grey79': [201, 201, 201, 255],
    'paleviovarred1': [255, 130, 171, 255],
    'paleviovarred2': [238, 121, 159, 255],
    'gold4': [139, 117, 0, 255],
    'gray41': [105, 105, 105, 255],
    'gray84': [214, 214, 214, 255],
    'mediumpurple': [147, 112, 219, 255],
    'rosybrown1': [255, 193, 193, 255],
    'lightblue2': [178, 223, 238, 255],
    'lightblue3': [154, 192, 205, 255],
    'grey57': [145, 145, 145, 255],
    'lightblue1': [191, 239, 255, 255],
    'lightblue4': [104, 131, 139, 255],
    'gray33': [84, 84, 84, 255],
    'skyblue4': [74, 112, 139, 255],
    'grey97': [247, 247, 247, 255],
    'skyblue1': [135, 206, 255, 255],
    'gray27': [69, 69, 69, 255],
    'skyblue3': [108, 166, 205, 255],
    'skyblue2': [126, 192, 238, 255],
    'lavenderblush1': [255, 240, 245, 255],
    'darkgrey': [169, 169, 169, 255],
    'lavenderblush3': [205, 193, 197, 255],
    'darkslategrey': [47, 79, 79, 255],
    'lavenderblush4': [139, 131, 134, 255],
    'deeppink4': [139, 10, 80, 255],
    'grey99': [252, 252, 252, 255],
    'gray36': [92, 92, 92, 255],
    'coral4': [139, 62, 47, 255],
    'magenta3': [205, 0, 205, 255],
    'lightskyblue4': [96, 123, 139, 255],
    'mediumturquoise': [72, 209, 204, 255],
    'gray34': [87, 87, 87, 255],
    'floralwhite': [255, 250, 240, 255],
    'grey39': [99, 99, 99, 255],
    'grey36': [92, 92, 92, 255],
    'grey37': [94, 94, 94, 255],
    'grey34': [87, 87, 87, 255],
    'gray26': [66, 66, 66, 255],
    'royalblue2': [67, 110, 238, 255],
    'grey33': [84, 84, 84, 255],
    'turquoise1': [0, 245, 255, 255],
    'grey31': [79, 79, 79, 255],
    'steelblue1': [99, 184, 255, 255],
    'sienna4': [139, 71, 38, 255],
    'steelblue3': [79, 148, 205, 255],
    'lavenderblush2': [238, 224, 229, 255],
    'sienna1': [255, 130, 71, 255],
    'steelblue4': [54, 100, 139, 255],
    'sienna3': [205, 104, 57, 255],
    'aquamarine4': [69, 139, 116, 255],
    'lightyellow1': [255, 255, 224, 255],
    'lightyellow2': [238, 238, 209, 255],
    'lightsteelblue': [176, 196, 222, 255],
    'lightyellow4': [139, 139, 122, 255],
    'magenta2': [238, 0, 238, 255],
    'lightskyblue1': [176, 226, 255, 255],
    'lightgoldenrod': [238, 221, 130, 255],
    'magenta4': [139, 0, 139, 255],
    'gray87': [222, 222, 222, 255],
    'greenyellow': [173, 255, 47, 255],
    'navajowhite4': [139, 121, 94, 255],
    'darkslategray4': [82, 139, 139, 255],
    'olivedrab': [107, 142, 35, 255],
    'navajowhite1': [255, 222, 173, 255],
    'navajowhite2': [238, 207, 161, 255],
    'darkgoldenrod1': [255, 185, 15, 255],
    'sienna': [160, 82, 45, 255],
    'blue1': [0, 0, 255, 255],
    'yellow1': [255, 255, 0, 255],
    'gray61': [156, 156, 156, 255],
    'magenta1': [255, 0, 255, 255],
    'grey52': [133, 133, 133, 255],
    'orangered4': [139, 37, 0, 255],
    'palegreen': [152, 251, 152, 255],
    'gray86': [219, 219, 219, 255],
    'grey80': [204, 204, 204, 255],
    'seashell': [255, 245, 238, 255],
    'royalblue': [65, 105, 225, 255],
    'firebrick3': [205, 38, 38, 255],
    'blue4': [0, 0, 139, 255],
    'peru': [205, 133, 63, 255],
    'gray60': [153, 153, 153, 255],
    'aquamarine': [127, 255, 212, 255],
    'grey53': [135, 135, 135, 255],
    'tan4': [139, 90, 43, 255],
    'darkgoldenrod': [184, 134, 11, 255],
    'tan2': [238, 154, 73, 255],
    'tan1': [255, 165, 79, 255],
    'darkslategray': [47, 79, 79, 255],
    'royalblue3': [58, 95, 205, 255],
    'red2': [238, 0, 0, 255],
    'red1': [255, 0, 0, 255],
    'dodgerblue': [30, 144, 255, 255],
    'viovarred4': [139, 34, 82, 255],
    'lightyellow': [255, 255, 224, 255],
    'pavarurquoise1': [187, 255, 255, 255],
    'firebrick2': [238, 44, 44, 255],
    'mediumaquamarine': [102, 205, 170, 255],
    'lemonchiffon': [255, 250, 205, 255],
    'chocolate': [210, 105, 30, 255],
    'orchid4': [139, 71, 137, 255],
    'maroon': [176, 48, 96, 255],
    'gray38': [97, 97, 97, 255],
    'darkorange4': [139, 69, 0, 255],
    'mintcream': [245, 255, 250, 255],
    'darkorange1': [255, 127, 0, 255],
    'antiquewhite': [250, 235, 215, 255],
    'darkorange2': [238, 118, 0, 255],
    'grey18': [46, 46, 46, 255],
    'grey19': [48, 48, 48, 255],
    'grey38': [97, 97, 97, 255],
    'moccasin': [255, 228, 181, 255],
    'grey10': [26, 26, 26, 255],
    'chocolate1': [255, 127, 36, 255],
    'chocolate2': [238, 118, 33, 255],
    'chocolate3': [205, 102, 29, 255],
    'saddlebrown': [139, 69, 19, 255],
    'grey15': [38, 38, 38, 255],
    'darkslateblue': [72, 61, 139, 255],
    'lightskyblue': [135, 206, 250, 255],
    'gray69': [176, 176, 176, 255],
    'gray68': [173, 173, 173, 255],
    'deeppink': [255, 20, 147, 255],
    'gray65': [166, 166, 166, 255],
    'gray64': [163, 163, 163, 255],
    'gray67': [171, 171, 171, 255],
    'gray66': [168, 168, 168, 255],
    'gray25': [64, 64, 64, 255],
    'coral': [255, 127, 80, 255],
    'gray63': [161, 161, 161, 255],
    'gray62': [158, 158, 158, 255],
    'goldenrod4': [139, 105, 20, 255],
    'grey35': [89, 89, 89, 255],
    'gray89': [227, 227, 227, 255],
    'goldenrod1': [255, 193, 37, 255],
    'goldenrod2': [238, 180, 34, 255],
    'goldenrod3': [205, 155, 29, 255],
    'springgreen1': [0, 255, 127, 255],
    'springgreen2': [0, 238, 118, 255],
    'springgreen3': [0, 205, 102, 255],
    'springgreen4': [0, 139, 69, 255],
    'mistyrose1': [255, 228, 225, 255],
    'sandybrown': [244, 164, 96, 255],
    'grey30': [77, 77, 77, 255],
    'seashell2': [238, 229, 222, 255],
    'seashell3': [205, 197, 191, 255],
    'tan': [210, 180, 140, 255],
    'seashell1': [255, 245, 238, 255],
    'mistyrose3': [205, 183, 181, 255],
    'magenta': [255, 0, 255, 255],
    'pink': [255, 192, 203, 255],
    'ivory2': [238, 238, 224, 255],
    'ivory1': [255, 255, 240, 255],
    'lightcyan2': [209, 238, 238, 255],
    'mediumseagreen': [60, 179, 113, 255],
    'ivory4': [139, 139, 131, 255],
    'darkorange': [255, 140, 0, 255],
    'powderblue': [176, 224, 230, 255],
    'dodgerblue1': [30, 144, 255, 255],
    'gray95': [242, 242, 242, 255],
    'firebrick1': [255, 48, 48, 255],
    'gray7': [18, 18, 18, 255],
    'mistyrose4': [139, 125, 123, 255],
    'tomato': [255, 99, 71, 255],
    'indianred2': [238, 99, 99, 255],
    'steelblue2': [92, 172, 238, 255],
    'gray100': [255, 255, 255, 255],
    'seashell4': [139, 134, 130, 255],
    'grey89': [227, 227, 227, 255],
    'grey88': [224, 224, 224, 255],
    'grey87': [222, 222, 222, 255],
    'grey86': [219, 219, 219, 255],
    'grey85': [217, 217, 217, 255],
    'grey84': [214, 214, 214, 255],
    'midnightblue': [25, 25, 112, 255],
    'grey82': [209, 209, 209, 255],
    'grey81': [207, 207, 207, 255],
    'yellow3': [205, 205, 0, 255],
    'ivory3': [205, 205, 193, 255],
    'grey22': [56, 56, 56, 255],
    'gray85': [217, 217, 217, 255],
    'viovarred3': [205, 50, 120, 255],
    'dodgerblue2': [28, 134, 238, 255],
    'gray42': [107, 107, 107, 255],
    'sienna2': [238, 121, 66, 255],
    'grey72': [184, 184, 184, 255],
    'grey73': [186, 186, 186, 255],
    'grey70': [179, 179, 179, 255],
    'paleviovarred': [219, 112, 147, 255],
    'lightslategray': [119, 136, 153, 255],
    'grey77': [196, 196, 196, 255],
    'grey74': [189, 189, 189, 255],
    'slategray1': [198, 226, 255, 255],
    'pink1': [255, 181, 197, 255],
    'mediumpurple1': [171, 130, 255, 255],
    'pink3': [205, 145, 158, 255],
    'antiquewhite4': [139, 131, 120, 255],
    'lightpink1': [255, 174, 185, 255],
    'honeydew2': [224, 238, 224, 255],
    'khaki4': [139, 134, 78, 255],
    'darkolivegreen4': [110, 139, 61, 255],
    'gray45': [115, 115, 115, 255],
    'slategray3': [159, 182, 205, 255],
    'darkolivegreen1': [202, 255, 112, 255],
    'khaki1': [255, 246, 143, 255],
    'khaki2': [238, 230, 133, 255],
    'khaki3': [205, 198, 115, 255],
    'lavenderblush': [255, 240, 245, 255],
    'honeydew4': [131, 139, 131, 255],
    'salmon3': [205, 112, 84, 255],
    'salmon2': [238, 130, 98, 255],
    'gray92': [235, 235, 235, 255],
    'salmon4': [139, 76, 57, 255],
    'gray49': [125, 125, 125, 255],
    'gray48': [122, 122, 122, 255],
    'linen': [250, 240, 230, 255],
    'burlywood1': [255, 211, 155, 255],
    'green': [0, 255, 0, 255],
    'gray47': [120, 120, 120, 255],
    'blueviovar': [138, 43, 226, 255],
    'brown2': [238, 59, 59, 255],
    'brown3': [205, 51, 51, 255],
    'peachpuff': [255, 218, 185, 255],
    'brown4': [139, 35, 35, 255],
    'firebrick4': [139, 26, 26, 255],
    'azure1': [240, 255, 255, 255],
    'azure3': [193, 205, 205, 255],
    'azure2': [224, 238, 238, 255],
    'azure4': [131, 139, 139, 255],
    'tomato4': [139, 54, 38, 255],
    'orange4': [139, 90, 0, 255],
    'firebrick': [178, 34, 34, 255],
    'indianred': [205, 92, 92, 255],
    'orange1': [255, 165, 0, 255],
    'orange3': [205, 133, 0, 255],
    'orange2': [238, 154, 0, 255],
    'darkolivegreen': [85, 107, 47, 255],
    'gray2': [5, 5, 5, 255],
    'slategrey': [112, 128, 144, 255],
    'gray81': [207, 207, 207, 255],
    'darkred': [139, 0, 0, 255],
    'gray3': [8, 8, 8, 255],
    'lightsteelblue1': [202, 225, 255, 255],
    'lightsteelblue2': [188, 210, 238, 255],
    'lightsteelblue3': [162, 181, 205, 255],
    'lightsteelblue4': [110, 123, 139, 255],
    'tomato3': [205, 79, 57, 255],
    'gray43': [110, 110, 110, 255],
    'darkgoldenrod4': [139, 101, 8, 255],
    'grey50': [127, 127, 127, 255],
    'yellow4': [139, 139, 0, 255],
    'mediumorchid': [186, 85, 211, 255],
    'yellow2': [238, 238, 0, 255],
    'darkgoldenrod2': [238, 173, 14, 255],
    'darkgoldenrod3': [205, 149, 12, 255],
    'chartreuse': [127, 255, 0, 255],
    'mediumblue': [0, 0, 205, 255],
    'gray4': [10, 10, 10, 255],
    'springgreen': [0, 255, 127, 255],
    'orange': [255, 165, 0, 255],
    'gray5': [13, 13, 13, 255],
    'lightsalmon': [255, 160, 122, 255],
    'gray19': [48, 48, 48, 255],
    'turquoise': [64, 224, 208, 255],
    'lightseagreen': [32, 178, 170, 255],
    'grey8': [20, 20, 20, 255],
    'grey9': [23, 23, 23, 255],
    'grey6': [15, 15, 15, 255],
    'grey7': [18, 18, 18, 255],
    'grey4': [10, 10, 10, 255],
    'grey5': [13, 13, 13, 255],
    'grey2': [5, 5, 5, 255],
    'grey3': [8, 8, 8, 255],
    'grey0': [0, 0, 0, 255],
    'grey1': [3, 3, 3, 255],
    'gray50': [127, 127, 127, 255],
    'goldenrod': [218, 165, 32, 255],
    'grey58': [148, 148, 148, 255],
    'grey59': [150, 150, 150, 255],
    'gray51': [130, 130, 130, 255],
    'grey54': [138, 138, 138, 255],
    'mediumorchid4': [122, 55, 139, 255],
    'grey56': [143, 143, 143, 255],
    'navajowhite3': [205, 179, 139, 255],
    'mediumorchid1': [224, 102, 255, 255],
    'grey51': [130, 130, 130, 255],
    'mediumorchid3': [180, 82, 205, 255],
    'mediumorchid2': [209, 95, 238, 255],
    'cyan2': [0, 238, 238, 255],
    'cyan3': [0, 205, 205, 255],
    'gray23': [59, 59, 59, 255],
    'cyan1': [0, 255, 255, 255],
    'darkgreen': [0, 100, 0, 255],
    'gray24': [61, 61, 61, 255],
    'cyan4': [0, 139, 139, 255],
    'darkviovar': [148, 0, 211, 255],
    'peachpuff4': [139, 119, 101, 255],
    'gray28': [71, 71, 71, 255],
    'slateblue4': [71, 60, 139, 255],
    'slateblue3': [105, 89, 205, 255],
    'peachpuff1': [255, 218, 185, 255],
    'peachpuff2': [238, 203, 173, 255],
    'peachpuff3': [205, 175, 149, 255],
    'gray29': [74, 74, 74, 255],
    'pavarurquoise': [175, 238, 238, 255],
    'darkgray': [169, 169, 169, 255],
    'grey25': [64, 64, 64, 255],
    'darkmagenta': [139, 0, 139, 255],
    'palegoldenrod': [238, 232, 170, 255],
    'grey64': [163, 163, 163, 255],
    'grey12': [31, 31, 31, 255],
    'deeppink3': [205, 16, 118, 255],
    'gray79': [201, 201, 201, 255],
    'gray83': [212, 212, 212, 255],
    'deeppink2': [238, 18, 137, 255],
    'burlywood4': [139, 115, 85, 255],
    'paleviovarred4': [139, 71, 93, 255],
    'deeppink1': [255, 20, 147, 255],
    'slateblue2': [122, 103, 238, 255],
    'grey46': [117, 117, 117, 255],
    'royalblue4': [39, 64, 139, 255],
    'yellowgreen': [154, 205, 50, 255],
    'royalblue1': [72, 118, 255, 255],
    'slateblue1': [131, 111, 255, 255],
    'lightgoldenrod3': [205, 190, 112, 255],
    'lightgoldenrod2': [238, 220, 130, 255],
    'navy': [0, 0, 128, 255],
    'orchid': [218, 112, 214, 255],
    'ghostwhite': [248, 248, 255, 255],
    'purple': [160, 32, 240, 255],
    'darkkhaki': [189, 183, 107, 255],
    'grey45': [115, 115, 115, 255],
    'gray94': [240, 240, 240, 255],
    'wheat4': [139, 126, 102, 255],
    'gray96': [245, 245, 245, 255],
    'gray97': [247, 247, 247, 255],
    'wheat1': [255, 231, 186, 255],
    'gray91': [232, 232, 232, 255],
    'wheat3': [205, 186, 150, 255],
    'wheat2': [238, 216, 174, 255],
    'indianred4': [139, 58, 58, 255],
    'coral2': [238, 106, 80, 255],
    'coral1': [255, 114, 86, 255],
    'viovarred': [208, 32, 144, 255],
    'rosybrown3': [205, 155, 155, 255],
    'deepskyblue2': [0, 178, 238, 255],
    'deepskyblue1': [0, 191, 255, 255],
    'bisque': [255, 228, 196, 255],
    'grey49': [125, 125, 125, 255],
    'khaki': [240, 230, 140, 255],
    'wheat': [245, 222, 179, 255],
    'lightslateblue': [132, 112, 255, 255],
    'mediumpurple3': [137, 104, 205, 255],
    'gray55': [140, 140, 140, 255],
    'deepskyblue': [0, 191, 255, 255],
    'gray98': [250, 250, 250, 255],
    'steelblue': [70, 130, 180, 255],
    'aliceblue': [240, 248, 255, 255],
    'lightskyblue2': [164, 211, 238, 255],
    'lightskyblue3': [141, 182, 205, 255],
    'lightslategrey': [119, 136, 153, 255],
    'blue3': [0, 0, 205, 255],
    'blue2': [0, 0, 238, 255],
    'gainsboro': [220, 220, 220, 255],
    'grey76': [194, 194, 194, 255],
    'purple3': [125, 38, 205, 255],
    'plum4': [139, 102, 139, 255],
    'gray56': [143, 143, 143, 255],
    'plum3': [205, 150, 205, 255],
    'plum': [221, 160, 221, 255],
    'lightgrey': [211, 211, 211, 255],
    'mediumslateblue': [123, 104, 238, 255],
    'mistyrose': [255, 228, 225, 255],
    'lightcyan1': [224, 255, 255, 255],
    'grey71': [181, 181, 181, 255],
    'darksalmon': [233, 150, 122, 255],
    'beige': [245, 245, 220, 255],
    'grey24': [61, 61, 61, 255],
    'azure': [240, 255, 255, 255],
    'honeydew1': [240, 255, 240, 255],
    'slategray2': [185, 211, 238, 255],
    'dodgerblue3': [24, 116, 205, 255],
    'slategray4': [108, 123, 139, 255],
    'grey27': [69, 69, 69, 255],
    'lightcyan3': [180, 205, 205, 255],
    'cornsilk': [255, 248, 220, 255],
    'tomato1': [255, 99, 71, 255],
    'gray57': [145, 145, 145, 255],
    'mediumviovarred': [199, 21, 133, 255],
    'tomato2': [238, 92, 66, 255],
    'snow4': [139, 137, 137, 255],
    'grey75': [191, 191, 191, 255],
    'snow2': [238, 233, 233, 255],
    'snow3': [205, 201, 201, 255],
    'snow1': [255, 250, 250, 255],
    'grey23': [59, 59, 59, 255],
    'cornsilk3': [205, 200, 177, 255],
    'lightcoral': [240, 128, 128, 255],
    'orangered': [255, 69, 0, 255],
    'navajowhite': [255, 222, 173, 255],
    'mediumpurple2': [159, 121, 238, 255],
    'slategray': [112, 128, 144, 255],
    'pink2': [238, 169, 184, 255],
    'grey29': [74, 74, 74, 255],
    'grey28': [71, 71, 71, 255],
    'gray82': [209, 209, 209, 255],
    'burlywood': [222, 184, 135, 255],
    'mediumpurple4': [93, 71, 139, 255],
    'mediumspringgreen': [0, 250, 154, 255],
    'grey26': [66, 66, 66, 255],
    'grey21': [54, 54, 54, 255],
    'grey20': [51, 51, 51, 255],
    'blanchedalmond': [255, 235, 205, 255],
    'pink4': [139, 99, 108, 255],
    'gray78': [199, 199, 199, 255],
    'tan3': [205, 133, 63, 255],
    'gray76': [194, 194, 194, 255],
    'gray77': [196, 196, 196, 255],
    'white': [255, 255, 255, 255],
    'gray75': [191, 191, 191, 255],
    'gray72': [184, 184, 184, 255],
    'gray73': [186, 186, 186, 255],
    'gray70': [179, 179, 179, 255],
    'gray71': [181, 181, 181, 255],
    'lightgray': [211, 211, 211, 255],
    'ivory': [255, 255, 240, 255],
    'gray46': [117, 117, 117, 255],
    'gray74': [189, 189, 189, 255],
    'lightyellow3': [205, 205, 180, 255],
    'lightpink2': [238, 162, 173, 255],
    'lightpink3': [205, 140, 149, 255],
    'pavarurquoise4': [102, 139, 139, 255],
    'lightpink4': [139, 95, 101, 255],
    'pavarurquoise3': [150, 205, 205, 255],
    'seagreen4': [46, 139, 87, 255],
    'seagreen3': [67, 205, 128, 255],
    'seagreen2': [78, 238, 148, 255],
    'seagreen1': [84, 255, 159, 255],
    'pavarurquoise2': [174, 238, 238, 255],
    'gray52': [133, 133, 133, 255],
    'cornsilk4': [139, 136, 120, 255],
    'cornsilk2': [238, 232, 205, 255],
    'darkolivegreen3': [162, 205, 90, 255],
    'cornsilk1': [255, 248, 220, 255],
    'limegreen': [50, 205, 50, 255],
    'darkolivegreen2': [188, 238, 104, 255],
    'grey': [190, 190, 190, 255],
    'viovarred2': [238, 58, 140, 255],
    'salmon1': [255, 140, 105, 255],
    'grey92': [235, 235, 235, 255],
    'grey93': [237, 237, 237, 255],
    'grey94': [240, 240, 240, 255],
    'grey95': [242, 242, 242, 255],
    'grey96': [245, 245, 245, 255],
    'grey83': [212, 212, 212, 255],
    'grey98': [250, 250, 250, 255],
    'lightgoldenrod1': [255, 236, 139, 255],
    'palegreen1': [154, 255, 154, 255],
    'red3': [205, 0, 0, 255],
    'palegreen3': [124, 205, 124, 255],
    'palegreen2': [144, 238, 144, 255],
    'palegreen4': [84, 139, 84, 255],
    'cadetblue': [95, 158, 160, 255],
    'viovar': [238, 130, 238, 255],
    'mistyrose2': [238, 213, 210, 255],
    'slateblue': [106, 90, 205, 255],
    'grey43': [110, 110, 110, 255],
    'grey90': [229, 229, 229, 255],
    'gray35': [89, 89, 89, 255],
    'turquoise3': [0, 197, 205, 255],
    'turquoise2': [0, 229, 238, 255],
    'burlywood3': [205, 170, 125, 255],
    'burlywood2': [238, 197, 145, 255],
    'lightcyan4': [122, 139, 139, 255],
    'rosybrown': [188, 143, 143, 255],
    'turquoise4': [0, 134, 139, 255],
    'whitesmoke': [245, 245, 245, 255],
    'lightblue': [173, 216, 230, 255],
    'grey40': [102, 102, 102, 255],
    'gray40': [102, 102, 102, 255],
    'honeydew3': [193, 205, 193, 255],
    'dimgray': [105, 105, 105, 255],
    'grey47': [120, 120, 120, 255],
    'seagreen': [46, 139, 87, 255],
    'red4': [139, 0, 0, 255],
    'grey14': [36, 36, 36, 255],
    'snow': [255, 250, 250, 255],
    'darkorchid1': [191, 62, 255, 255],
    'gray58': [148, 148, 148, 255],
    'gray59': [150, 150, 150, 255],
    'cadetblue4': [83, 134, 139, 255],
    'cadetblue3': [122, 197, 205, 255],
    'cadetblue2': [142, 229, 238, 255],
    'cadetblue1': [152, 245, 255, 255],
    'olivedrab4': [105, 139, 34, 255],
    'purple4': [85, 26, 139, 255],
    'gray20': [51, 51, 51, 255],
    'grey44': [112, 112, 112, 255],
    'purple1': [155, 48, 255, 255],
    'olivedrab1': [192, 255, 62, 255],
    'olivedrab2': [179, 238, 58, 255],
    'olivedrab3': [154, 205, 50, 255],
    'orangered3': [205, 55, 0, 255],
    'orangered2': [238, 64, 0, 255],
    'orangered1': [255, 69, 0, 255],
    'darkorchid': [153, 50, 204, 255],
    'thistle3': [205, 181, 205, 255],
    'thistle2': [238, 210, 238, 255],
    'thistle1': [255, 225, 255, 255],
    'salmon': [250, 128, 114, 255],
    'gray93': [237, 237, 237, 255],
    'thistle4': [139, 123, 139, 255],
    'gray39': [99, 99, 99, 255],
    'lawngreen': [124, 252, 0, 255],
    'hotpink3': [205, 96, 144, 255],
    'hotpink2': [238, 106, 167, 255],
    'hotpink1': [255, 110, 180, 255],
    'lightgreen': [144, 238, 144, 255],
    'hotpink4': [139, 58, 98, 255],
    'darkseagreen4': [105, 139, 105, 255],
    'darkseagreen3': [155, 205, 155, 255],
    'darkseagreen2': [180, 238, 180, 255],
    'darkseagreen1': [193, 255, 193, 255],
    'deepskyblue4': [0, 104, 139, 255],
    'gray44': [112, 112, 112, 255],
    'navyblue': [0, 0, 128, 255],
    'darkblue': [0, 0, 139, 255],
    'forestgreen': [34, 139, 34, 255],
    'gray53': [135, 135, 135, 255],
    'grey100': [255, 255, 255, 255],
    'brown1': [255, 64, 64, 255],
};

var $builtinmodule = function (name) {
    var mod = {};
    for (var k in PygameLib.constants) {
        mod[k] = Sk.ffi.remapToPy(PygameLib.constants[k]);
    }
    mod.__path__ = Sk.builtin.list([{"pygame": "pygame", "v": "pygame", "__class__": "pygame"}]);
    mod.init = new Sk.builtin.func(pygame_init);
    mod.Surface = Sk.misceval.buildClass(mod, surface$1, 'Surface', []);
    PygameLib.SurfaceType = mod.Surface;
    mod.Color = Sk.misceval.buildClass(mod, color_type_f, 'Color', []);
    PygameLib.ColorType = mod.Color;
    mod.Rect = Sk.misceval.buildClass(mod, rect_type_f, 'Rect', []);
    PygameLib.RectType = mod.Rect;
    mod.quit = new Sk.builtin.func(function () {
        PygameLib.running = false;
        if (Sk.quitHandler) {
            Sk.quitHandler();
        }
        Sk.hardInterrupt = true;

    });
    mod.error = new Sk.builtin.func(function (description) {
        if (Sk.abstr.typeName(description) !== "str") {
            throw new Sk.builtin.TypeError("Error description should be a string");
        }
        mod.lastError = description;
        return Sk.builtin.RuntimeError(description);
    });
    mod.get_error = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    mod.set_error = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    mod.get_sdl_version = new Sk.builtin.func(function () {
        return Sk.builtin.tuple([1, 2, 15])
    });
    mod.get_sdl_byteorder = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(PygameLib.constants.LIL_ENDIAN);
    });
    mod.register_quit = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    mod.encode_string = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    mod.encode_file_path = new Sk.builtin.func(function () {
        throw new Sk.builtin.NotImplementedError("Not yet implemented");
    });
    return mod;
};

// pygame module
function pygame_init() {
    // ovo je mi ne izgleda najelegantnije, ali još nisam našao lepši način
    var display_m = Sk.importModule("pygame.display", false, false);
    var event_m = Sk.importModule("pygame.event", false, false);
    var draw_m = Sk.importModule("pygame.draw", false, false);
    var pygame_m = Sk.importModule("pygame", false, false);
    var time_m = Sk.importModule("pygame.time", false, false);
    var image_m = Sk.importModule("pygame.image", false, false);
    var font_m = Sk.importModule("pygame.font", false, false);
    var key_m = Sk.importModule("pygame.key", false, false);
    var version_m = Sk.importModule("pygame.version", false, false);
    var mouse_m = Sk.importModule("pygame.mouse", false, false);
    var transform_m = Sk.importModule("pygame.transform", false, false);
    var locals_m = Sk.importModule("pygame.locals", false, false);

    PygameLib.initial_time = new Date();
    pygame_m.$d['display'] = display_m.$d['display'];
    pygame_m.$d['event'] = display_m.$d['event'];
    pygame_m.$d['draw'] = display_m.$d['draw'];
    pygame_m.$d['image'] = display_m.$d['image'];
    delete PygameLib.eventQueue;
    delete PygameLib.eventTimer;
    PygameLib.eventQueue = [];
    PygameLib.pressedKeys = {};
    PygameLib.eventTimer = {};
    PygameLib.running = true;
    PygameLib.repeatKeys = false;
    PygameLib.mouseData = {"button": [0, 0, 0], "pos": [0, 0], "rel": [0, 0]};
    // }
}

var mouseEventListener = function (event) {

    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var canvasX = 0;
    var canvasY = 0;
    var currentElement = this;
    do {
        totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
        totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
    }
    while (currentElement === currentElement.offsetParent);

    canvasX = event.clientX - totalOffsetX;
    canvasY = event.clientY - totalOffsetY;

    var button = event.button;
    if (event.type === "mousedown") {
        var e = [PygameLib.constants.MOUSEBUTTONDOWN,
            {
                key: PygameLib.constants.MOUSEBUTTONDOWN,
                pos: [canvasX, canvasY],
                button: button + 1
            }];
        PygameLib.mouseData["button"][button] = 1;
    } else if (event.type === "mouseup") {
        var e = [PygameLib.constants.MOUSEBUTTONUP,
            {
                key: PygameLib.constants.MOUSEBUTTONUP,
                pos: [canvasX, canvasY],
                button: button + 1
            }];
        PygameLib.mouseData["button"][button] = 0;
    } else if (event.type === "mousemove") {
        var leftButton = 0;
        var rightButton = 0;
        var middleButton = 0;
        if (event.buttons && (1 << 0)) {
            leftButton = 1;
        }
        if (event.buttons && (1 << 1)) {
            rightButton = 1;
        }
        if (event.buttons && (1 << 2)) {
            middleButton = 1;
        }
        var e = [PygameLib.constants.MOUSEMOTION,
        {
            key: PygameLib.constants.MOUSEMOTION,
            pos: [canvasX, canvasY],
            rel: [event.movementX, event.movementY],
            buttons: [leftButton, middleButton, rightButton]
        }];
        PygameLib.mouseData["pos"] = [canvasX, canvasY];
        PygameLib.mouseData["rel"] = [event.movementX, event.movementY];
    }
    PygameLib.eventQueue.unshift(e);
};

// Surface((width, height))
var init$1 = function $__init__123$(self, size, fullscreen = false, main = true) {
    Sk.builtin.pyCheckArgs('__init__', arguments, 2, 5, false, false);
    var tuple_js = Sk.ffi.remapToJs(size);
    self.width = Math.round(tuple_js[0]);
    self.height = Math.round(tuple_js[1]);
    self.main_canvas = document.createElement("canvas");
    main = Sk.ffi.remapToJs(main);
    if (main) {
        self.main_canvas = Sk.main_canvas;

        Sk.bindPygameListeners = function () {
            self.main_canvas.addEventListener('mousedown', mouseEventListener);
            self.main_canvas.addEventListener('mouseup', mouseEventListener);
            self.main_canvas.addEventListener('mousemove', mouseEventListener);
            window.addEventListener("keydown", keyEventListener);
            window.addEventListener("keyup", keyEventListener);
        }

        Sk.unbindPygameListeners = function () {
            self.main_canvas.removeEventListener('mousedown', mouseEventListener);
            self.main_canvas.removeEventListener('mouseup', mouseEventListener);
            self.main_canvas.removeEventListener('mousemove', mouseEventListener);
            window.removeEventListener("keydown", keyEventListener);
            window.removeEventListener("keyup", keyEventListener);
        }

        Sk.bindPygameListeners();
    }
    self.main_canvas.width = self.width;
    self.main_canvas.height = self.height;
    self.main_context = self.main_canvas.getContext("2d");

    self.offscreen_canvas = document.createElement('canvas');
    self.context2d = self.offscreen_canvas.getContext("2d");
    self.offscreen_canvas.width = self.width;
    self.offscreen_canvas.height = self.height;
    self.main_canvas.setAttribute('width', self.width);
    self.main_canvas.setAttribute('height', self.height);
    fillBlack(self.main_context, self.main_canvas.width, self.main_canvas.height, main);
    fillBlack(self.context2d, self.width, self.height, main);

    return Sk.builtin.none.none$;

};

function fillBlack(ctx, w, h, main = false) {
    ctx.beginPath();
    ctx.rect(0, 0, w, h);
    if (main){
        ctx.fillStyle = "black";
    } else {
        ctx.fillStyle = "rgba(100, 100, 100, 0.0)";
    }
    ctx.fill();
}

init$1.co_name = new Sk.builtins['str']('__init__');
init$1.co_varnames = ['self', 'size', 'flags', 'depth', 'masks'];
init$1.$defaults = [new Sk.builtin.int_(0), new Sk.builtin.int_(0), Sk.builtin.none.none$];

var repr$1 = function $__repr__123$(self) {
    var width = Sk.ffi.remapToJs(self.width);
    var height = Sk.ffi.remapToJs(self.height);

    return Sk.ffi.remapToPy('<Surface(' + width + 'x' + height + 'x32 SW)>');
};
repr$1.co_name = new Sk.builtin.str('__repr__');
repr$1.co_varnames = ['self'];

function get_height(self) {
    Sk.builtin.pyCheckArgs('get_height', arguments, 1, 1, false, false);
    return Sk.ffi.remapToPy(self.height);
}

get_height.co_name = new Sk.builtin.str('get_height');
get_height.co_varnames = ['self'];

function get_width(self) {
    Sk.builtin.pyCheckArgs('get_width', arguments, 1, 1, false, false);
    return Sk.ffi.remapToPy(self.width);
}

get_width.co_name = new Sk.builtin.str('get_width');
get_width.co_varnames = ['self'];

function get_size(self) {
    Sk.builtin.pyCheckArgs('get_size', arguments, 1, 1, false, false);
    return Sk.builtin.tuple([self.width, self.height]);
}

get_size.co_name = new Sk.builtin.str('get_size');
get_size.co_varnames = ['self'];

function get_flags() {
    Sk.builtin.pyCheckArgs('get_flags', arguments, 1, 1, false, false);
    return new Sk.builtin.int_(0);
}

get_flags.co_name = new Sk.builtin.str('get_flags');
get_flags.co_varnames = ['self'];

function update(self) {
    self.main_canvas.width = self.offscreen_canvas.width;
    self.main_canvas.height = self.offscreen_canvas.height;
    self.main_context.drawImage(self.offscreen_canvas, 0, 0);
}

update.co_name = new Sk.builtin.str('update');
update.co_varnames = ['self'];

function blit(self, other, pos) {
    // other, pos;
    let target_pos_js;
    if (Sk.misceval.isTrue(Sk.builtin.isinstance(pos, Sk.builtin.tuple)) ||
        Sk.misceval.isTrue(Sk.builtin.isinstance(pos, Sk.builtin.list))
    ) {
        target_pos_js = Sk.ffi.remapToJs(pos);
    } else if (Sk.misceval.isTrue(Sk.builtin.isinstance(pos, PygameLib.RectType))) {
        // debugger;
        const tmpName = Sk.builtin.str("topleft");
        target_pos_js = Sk.ffi.remapToJs(Sk.builtin.getattr(pos, tmpName))
    } else {
        target_pos_js = [0, 0]
    }
    self.context2d.drawImage(other.offscreen_canvas, target_pos_js[0], target_pos_js[1]);
    return Sk.misceval.callsim(PygameLib.RectType,
        Sk.builtin.tuple([0, 0]), Sk.builtin.tuple([other.offscreen_canvas.width, other.offscreen_canvas.height]))

}

function convert(self) {
    return self;
}

var surface$1 = function $Surface$class_outer(gbl, loc) {
    loc.__init__ = new Sk.builtin.func(init$1, gbl);
    loc.__repr__ = new Sk.builtin.func(repr$1, gbl);
    loc.fill = new Sk.builtin.func(function (self, color) {
        var ctx = self.context2d;
        var color_js = PygameLib.extract_color(color);
        ctx.fillStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.fillRect(0, 0, self.width, self.height);
    });
    loc.blit = new Sk.builtin.func(blit, gbl);
    loc.convert = new Sk.builtin.func(convert, gbl);
    loc.convert_alpha = new Sk.builtin.func(convert, gbl);
    loc.update = new Sk.builtin.func(update, gbl);
    loc.get_width = new Sk.builtin.func(get_width, gbl);
    loc.get_height = new Sk.builtin.func(get_height, gbl);
    loc.get_size = new Sk.builtin.func(get_size, gbl);
    loc.get_flags = new Sk.builtin.func(get_flags, gbl);
    loc.copy = new Sk.builtin.func(function (self) {
        var size = Sk.builtin.tuple([self.offscreen_canvas.width, self.offscreen_canvas.width]);
        var ret = Sk.misceval.callsim(PygameLib.SurfaceType, size);
        ret.offscreen_canvas.width = self.offscreen_canvas.width;
        ret.offscreen_canvas.height = self.offscreen_canvas.height;
        ret.context2d.drawImage(self.offscreen_canvas, 0, 0);
        return ret;
    });
    loc.scroll = new Sk.builtin.func(function (self, dx, dy) {
        var x = Sk.ffi.remapToJs(dx);
        var y = Sk.ffi.remapToJs(dy);
        self.context2d.drawImage(self.offscreen_canvas, x, y);
        return Sk.builtin.none.none$;
    });
    loc.get_at = new Sk.builtin.func(function (self, coordinates) {
        if (Sk.abstr.typeName(coordinates) !== "tuple") {
            throw new Sk.builtin.TypeError("argument must be a pair");
        }
        var x = Sk.ffi.remapToJs(coordinates.v[0]);
        var y = Sk.ffi.remapToJs(coordinates.v[1]);
        var data = self.context2d.getImageData(x, y, 1, 1).data;
        return Sk.builtin.tuple([data[0], data[1], data[2], data[3]]);
    });
    loc.set_at = new Sk.builtin.func(function (self, coordinates, clr) {
        if (Sk.abstr.typeName(coordinates) !== "tuple") {
            throw new Sk.builtin.TypeError("the first argument must be a pair");
        }
        if (Sk.abstr.typeName(clr) !== "Color") {
            throw new Sk.builtin.TypeError("the second argument must be a Pygame color");
        }
        var rgba = PygameLib.extract_color(clr);
        self.context2d.fillStyle = "rgba(" + rgba[0] + "," + rgba[1] + "," + rgba[2] + "," + (rgba[3] / 255) + ")";
        var x = Sk.ffi.remapToJs(coordinates.v[0]);
        var y = Sk.ffi.remapToJs(coordinates.v[1]);
        self.context2d.fillRect(x, y, 1, 1);
    });
    loc.get_rect = new Sk.builtin.func(function (self) {
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([0, 0]), Sk.builtin.tuple([self.offscreen_canvas.width, self.offscreen_canvas.height]))
    });
    loc.get_bounding_rect = new Sk.builtin.func(function (self) {
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([0, 0]), Sk.builtin.tuple([self.offscreen_canvas.width, self.offscreen_canvas.height]))
    })
};

surface$1.co_name = new Sk.builtin.str('Surface');

//pygame.Color
function color_type_f($gbl, $loc) {
    // https://gist.github.com/mjackson/5311256
    $loc.__init__ = new Sk.builtin.func(function (self, r, g, b, a) {
        Sk.builtin.pyCheckArgs('__init__', arguments, 2, 5, false, false);
        var r_js = Sk.ffi.remapToJs(r);
        if (typeof (r_js) == 'string') {
            var color_name = r_js;
            r = Sk.ffi.remapToPy(PygameLib.Colors[color_name][0]);
            g = Sk.ffi.remapToPy(PygameLib.Colors[color_name][1]);
            b = Sk.ffi.remapToPy(PygameLib.Colors[color_name][2]);
            a = Sk.ffi.remapToPy(PygameLib.Colors[color_name][3]);
        }
        Sk.abstr.sattr(self, rPyStr, r, false);
        Sk.abstr.sattr(self, gPyStr, g, false);
        Sk.abstr.sattr(self, bPyStr, b, false);
        Sk.abstr.sattr(self, aPyStr, a, false);
        Sk.abstr.sattr(self, lenPyStr, Sk.ffi.remapToPy(4), false);
        return Sk.builtin.none.none$;
    });
    $loc.__init__.co_name = new Sk.builtin.str('__init__');
    $loc.__init__.co_varnames = ['self', 'r', 'g', 'b', 'a'];

    $loc.__repr__ = new Sk.builtin.func(function (self) {
        var r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false));
        var g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false));
        var b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false));
        var a = Sk.ffi.remapToJs(Sk.abstr.gattr(self, aPyStr, false));
        return Sk.ffi.remapToPy('<Color(' + r + ', ' + g + ', ' + b + ', ' + a + ')>');
    });
    $loc.__repr__.co_name = new Sk.builtin.str('__repr__');
    $loc.__repr__.co_varnames = ['self'];

    var cmy_getter = new Sk.builtin.func(function (self) {
        var r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false));
        var g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false));
        var b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false));
        return Sk.builtin.tuple([1.0 - r / 255, 1.0 - g / 255, 1.0 - b / 255]);
    });
    var cmy_setter = new Sk.builtin.func(function (self, val) {
        var cmy = Sk.ffi.remapToJs(val);
        Sk.abstr.sattr(self, rPyStr, Sk.ffi.remapToPy(255 - cmy[0] * 255), false);
        Sk.abstr.sattr(self, gPyStr, Sk.ffi.remapToPy(255 - cmy[1] * 255), false);
        Sk.abstr.sattr(self, bPyStr, Sk.ffi.remapToPy(255 - cmy[2] * 255), false);
    });
    // this is a way of creating an equivalent of property()
    $loc.cmy = Sk.misceval.callsimOrSuspend(Sk.builtins.property, cmy_getter, cmy_setter);

    var hsva_getter = new Sk.builtin.func(function (self) {
        // https://stackoverflow.com/a/8023734
        var rr, gg, bb,
            r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false)) / 255,
            g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false)) / 255,
            b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false)) / 255,
            h, s,
            v = Math.max(r, g, b),
            diff = v - Math.min(r, g, b),
            diffc = function (c) {
                return (v - c) / 6 / diff + 1 / 2;
            };

        if (diff === 0) {
            h = s = 0;
        } else {
            s = diff / v;
            rr = diffc(r);
            gg = diffc(g);
            bb = diffc(b);

            if (r === v) {
                h = bb - gg;
            } else if (g === v) {
                h = (1 / 3) + rr - bb;
            } else if (b === v) {
                h = (2 / 3) + gg - rr;
            }
            if (h < 0) {
                h += 1;
            } else if (h > 1) {
                h -= 1;
            }
        }
        var a = Sk.ffi.remapToJs(Sk.abstr.gattr(self, aPyStr, false));
        a = Math.round(a / 255 * 100);
        return Sk.builtin.tuple([Math.round(h * 360), Math.round(s * 100), Math.round(v * 100), a]);
    });
    var hsva_setter = new Sk.builtin.func(function (self, val) {
        // https://stackoverflow.com/a/17243070
        var r, g, b, i, f, p, q, t;
        var hsva = Sk.ffi.remapToJs(val);
        var h = hsva[0] / 360;
        var s = hsva[1] / 100;
        var v = hsva[2] / 100;
        i = Math.floor(h * 6);
        f = h * 6 - i;
        p = v * (1 - s);
        q = v * (1 - f * s);
        t = v * (1 - (1 - f) * s);
        switch (i % 6) {
            case 0:
                r = v, g = t, b = p;
                break;
            case 1:
                r = q, g = v, b = p;
                break;
            case 2:
                r = p, g = v, b = t;
                break;
            case 3:
                r = p, g = q, b = v;
                break;
            case 4:
                r = t, g = p, b = v;
                break;
            case 5:
                r = v, g = p, b = q;
                break;
        }
        Sk.abstr.sattr(self, rPyStr, Sk.ffi.remapToPy(Math.round(r * 255)), false);
        Sk.abstr.sattr(self, gPyStr, Sk.ffi.remapToPy(Math.round(g * 255)), false);
        Sk.abstr.sattr(self, bPyStr, Sk.ffi.remapToPy(Math.round(b * 255)), false);
        Sk.abstr.sattr(self, aPyStr, Sk.ffi.remapToPy(Math.round(hsva[3] / 100 * 255)), false);
    });
    $loc.hsva = Sk.misceval.callsimOrSuspend(Sk.builtins.property, hsva_getter, hsva_setter);

    var hsla_getter = new Sk.builtin.func(function (self) {
        var r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false));
        var g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false));
        var b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false));
        var a = Sk.ffi.remapToJs(Sk.abstr.gattr(self, aPyStr, false));
        r /= 255;
        g /= 255;
        b /= 255;
        a /= 255;

        var max = Math.max(r, g, b), min = Math.min(r, g, b);
        var h, s, l = (max + min) / 2;

        if (max === min) {
            h = s = 0; // achromatic
        } else {
            var d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

            switch (max) {
                case r:
                    h = (g - b) / d + (g < b ? 6 : 0);
                    break;
                case g:
                    h = (b - r) / d + 2;
                    break;
                case b:
                    h = (r - g) / d + 4;
                    break;
            }

            h /= 6;
        }
        h *= 360;
        s *= 100;
        l *= 100;
        a *= 100;
        return Sk.builtin.tuple([h, s, l, a]);
    });
    var hsla_setter = new Sk.builtin.func(function (self, val) {
        var hsla = Sk.ffi.remapToJs(val);
        var h = hsla[0] / 360;
        var s = hsla[1] / 100;
        var l = hsla[2] / 100;
        var a = hsla[3] / 100;
        var r, g, b;

        if (s === 0) {
            r = g = b = l; // achromatic
        } else {
            function hue2rgb(p, q, t) {
                if (t < 0) t += 1;
                if (t > 1) t -= 1;
                if (t < 1 / 6) return p + (q - p) * 6 * t;
                if (t < 1 / 2) return q;
                if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
                return p;
            }

            var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            var p = 2 * l - q;

            r = hue2rgb(p, q, h + 1 / 3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1 / 3);
        }
        Sk.abstr.sattr(self, rPyStr, Sk.ffi.remapToPy(Math.round(r * 255)), false);
        Sk.abstr.sattr(self, gPyStr, Sk.ffi.remapToPy(Math.round(g * 255)), false);
        Sk.abstr.sattr(self, bPyStr, Sk.ffi.remapToPy(Math.round(b * 255)), false);
        Sk.abstr.sattr(self, aPyStr, Sk.ffi.remapToPy(Math.round(a * 255)), false);
    });
    $loc.hsla = Sk.misceval.callsimOrSuspend(Sk.builtins.property, hsla_getter, hsla_setter);

    var i1i2i3_getter = new Sk.builtin.func(function (self) {
        var r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false));
        var g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false));
        var b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false));
        r /= 255;
        g /= 255;
        b /= 255;
        var i1 = (r + g + b) / 3;
        var i2 = (r - b) / 2;
        var i3 = (2 * g - r - b) / 4;
        return Sk.builtin.tuple([i1, i2, i3]);
    });
    var i1i2i3_setter = new Sk.builtin.func(function (self, val) {
        var i1i2i3 = Sk.ffi.remapToJs(val);
        var i1 = i1i2i3[0];
        var i2 = i1i2i3[1];
        var i3 = i1i2i3[2];
        var r = i1 + i2 - 2 * i3 / 3;
        var g = i1 + 4 * i3 / 3;
        var b = i1 - i2 - 2 * i3 / 3;
        Sk.abstr.sattr(self, rPyStr, Sk.ffi.remapToPy(Math.round(r * 255)), false);
        Sk.abstr.sattr(self, gPyStr, Sk.ffi.remapToPy(Math.round(g * 255)), false);
        Sk.abstr.sattr(self, bPyStr, Sk.ffi.remapToPy(Math.round(b * 255)), false);
    });
    $loc.i1i2i3 = Sk.misceval.callsimOrSuspend(Sk.builtins.property, i1i2i3_getter, i1i2i3_setter);

    $loc.normalize = new Sk.builtin.func(function (self) {
        var r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false));
        var g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false));
        var b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false));
        var a = Sk.ffi.remapToJs(Sk.abstr.gattr(self, aPyStr, false));
        return Sk.builtin.tuple([r / 255, g / 255, b / 255, a / 255]);
    });

    $loc.correct_gamma = new Sk.builtin.func(function (self, val) {
        var gamma = Sk.ffi.remapToJs(val);
        var r = Sk.ffi.remapToJs(Sk.abstr.gattr(self, rPyStr, false));
        var g = Sk.ffi.remapToJs(Sk.abstr.gattr(self, gPyStr, false));
        var b = Sk.ffi.remapToJs(Sk.abstr.gattr(self, bPyStr, false));
        var a = Sk.ffi.remapToJs(Sk.abstr.gattr(self, aPyStr, false));
        r = Math.round(Math.pow(r / 255, gamma) * 255);
        g = Math.round(Math.pow(g / 255, gamma) * 255);
        b = Math.round(Math.pow(b / 255, gamma) * 255);
        a = Math.round(Math.pow(a / 255, gamma) * 255);
        Sk.abstr.sattr(self, rPyStr, Sk.ffi.remapToPy(r), false);
        Sk.abstr.sattr(self, gPyStr, Sk.ffi.remapToPy(g), false);
        Sk.abstr.sattr(self, bPyStr, Sk.ffi.remapToPy(b), false);
        Sk.abstr.sattr(self, aPyStr, Sk.ffi.remapToPy(a), false);
        return Sk.builtin.tuple([r, g, b, a])
    });

    $loc.set_length = new Sk.builtin.func(function (self, val) {
        Sk.abstr.sattr(self, lenPyStr, val, false);
    });

    $loc.__len__ = new Sk.builtin.func(function (self) {
        return Sk.abstr.gattr(self, lenPyStr, false);
    })
};

//pygame.Rect
function rect_type_f($gbl, $loc) {
    //Rect(Surface, color, Rect, width=0) -> Rect
    //Rect((left, top), (width, height)) -> Rect
    $loc.__init__ = new Sk.builtin.func(function (self, a, b, c, d) {
        Sk.builtin.pyCheckArgs('__init__', arguments, 3, 5, false, false);

        if (Sk.abstr.typeName(a) === "tuple" && Sk.abstr.typeName(b) === "tuple") {
            if (c !== undefined || d !== undefined) {
                throw new Sk.builtin.RuntimeError("Expected 2 tuples or 4 ints as input");
            }
            var a_js = Sk.ffi.remapToJs(a);
            var b_js = Sk.ffi.remapToJs(b);
            Sk.abstr.sattr(self, leftPyStr, Sk.ffi.remapToPy(a_js[0]), false);
            Sk.abstr.sattr(self, topPyStr, Sk.ffi.remapToPy(a_js[1]), false);
            Sk.abstr.sattr(self, widthPyStr, Sk.ffi.remapToPy(b_js[0]), false);
            Sk.abstr.sattr(self, heightPyStr, Sk.ffi.remapToPy(b_js[1]), false);
        } else if ((Sk.abstr.typeName(a) === "int" || Sk.abstr.typeName(a) === "float") &&
            (Sk.abstr.typeName(b) === "int" || Sk.abstr.typeName(b) === "float") &&
            (Sk.abstr.typeName(c) === "int" || Sk.abstr.typeName(c) === "float") &&
            (Sk.abstr.typeName(d) === "int" || Sk.abstr.typeName(d) === "float")) {
            Sk.abstr.sattr(self, leftPyStr, a, false);
            Sk.abstr.sattr(self, topPyStr, b, false);
            Sk.abstr.sattr(self, widthPyStr, c, false);
            Sk.abstr.sattr(self, heightPyStr, d, false);

        }
        return Sk.builtin.none.none$;
    });
    $loc.__init__.co_name = new Sk.builtin.str('__init__');
    $loc.__init__.co_varnames = ['self', 'left', 'top', 'width', 'heght'];

    $loc.__repr__ = new Sk.builtin.func(function (self) {
        var left = Sk.ffi.remapToJs(Sk.abstr.gattr(self, leftPyStr, false));
        var top = Sk.ffi.remapToJs(Sk.abstr.gattr(self, topPyStr, false));
        var width = Sk.ffi.remapToJs(Sk.abstr.gattr(self, widthPyStr, false));
        var height = Sk.ffi.remapToJs(Sk.abstr.gattr(self, heightPyStr, false));
        return Sk.ffi.remapToPy('<Rect(' + left + ', ' + top + ', ' + width + ', ' + height + ')>');
    });
    $loc.__repr__.co_name = new Sk.builtin.str('__repr__');
    $loc.__repr__.co_varnames = ['self'];

    $loc.copy = new Sk.builtin.func(function (self) {
        var left = Sk.ffi.remapToJs(Sk.abstr.gattr(self, leftPyStr, false));
        var top = Sk.ffi.remapToJs(Sk.abstr.gattr(self, topPyStr, false));
        var width = Sk.ffi.remapToJs(Sk.abstr.gattr(self, widthPyStr, false));
        var height = Sk.ffi.remapToJs(Sk.abstr.gattr(self, heightPyStr, false));
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([left, top]), Sk.builtin.tuple([width, height]))
    }, $gbl);
    // https://github.com/pygame/pygame/blob/master/src_c/rect.c
    var x_getter = new Sk.builtin.func(function (self) {
        return Sk.abstr.gattr(self, leftPyStr, false);
    });
    var x_setter = new Sk.builtin.func(function (self, val) {
        Sk.abstr.sattr(self, leftPyStr, val, false);
    });
    $loc.x = Sk.misceval.callsimOrSuspend(Sk.builtins.property, x_getter, x_setter);

    var y_getter = new Sk.builtin.func(function (self) {
        return Sk.abstr.gattr(self, topPyStr, false);
    });
    var y_setter = new Sk.builtin.func(function (self, val) {
        Sk.abstr.sattr(self, topPyStr, val, false);
    });
    $loc.y = Sk.misceval.callsimOrSuspend(Sk.builtins.property, y_getter, y_setter);

    function get_top(self) {
        return Sk.ffi.remapToJs(Sk.abstr.gattr(self, topPyStr, false));
    }

    function get_height(self) {
        return Sk.ffi.remapToJs(Sk.abstr.gattr(self, heightPyStr, false));
    }

    function get_bottom(self) {
        return get_top(self) + get_height(self);
    }

    function get_left(self) {
        return Sk.ffi.remapToJs(Sk.abstr.gattr(self, leftPyStr, false));
    }

    function get_width(self) {
        return Sk.ffi.remapToJs(Sk.abstr.gattr(self, widthPyStr, false));
    }

    function get_right(self) {
        return get_left(self) + get_width(self);
    }

    function get_centerx(self) {
        return get_left(self) + Math.floor(get_width(self) / 2);
    }

    function get_centery(self) {
        return get_top(self) + Math.floor(get_height(self) / 2);
    }

    function set_top(self, t) {
        Sk.abstr.sattr(self, topPyStr, Sk.ffi.remapToPy(t), false);
    }

    function set_height(self, h) {
        Sk.abstr.sattr(self, heightPyStr, Sk.ffi.remapToPy(h), false);
    }

    function set_bottom(self, b) {
        set_top(self, b - get_height(self));
    }

    function set_left(self, l) {
        Sk.abstr.sattr(self, leftPyStr, Sk.ffi.remapToPy(l), false);
    }

    function set_width(self, w) {
        Sk.abstr.sattr(self, widthPyStr, Sk.ffi.remapToPy(w), false);
    }

    function set_right(self, r) {
        set_left(self, r - get_width(self));
    }

    function set_centerx(self, cx) {
        set_left(self, cx - Math.floor(get_width(self) / 2));
    }

    function set_centery(self, cy) {
        set_top(self, cy - Math.floor(get_height(self) / 2));
    }

    var bottom_getter = new Sk.builtin.func(function (self) {
        return Sk.ffi.remapToPy(get_bottom(self));
    });
    var bottom_setter = new Sk.builtin.func(function (self, val) {
        set_bottom(self, Sk.ffi.remapToJs(val));
    });
    $loc.bottom = Sk.misceval.callsimOrSuspend(Sk.builtins.property, bottom_getter, bottom_setter);

    var right_getter = new Sk.builtin.func(function (self) {
        return Sk.ffi.remapToPy(get_right(self));
    });
    var right_setter = new Sk.builtin.func(function (self, val) {
        set_right(self, Sk.ffi.remapToJs(val));
    });
    $loc.right = Sk.misceval.callsimOrSuspend(Sk.builtins.property, right_getter, right_setter);

    var topleft_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_left(self), get_top(self)]);
    });
    var topleft_setter = new Sk.builtin.func(function (self, val) {
        var tl = Sk.ffi.remapToJs(val);
        set_top(self, tl[1]);
        set_left(self, tl[0]);
    });
    $loc.topleft = Sk.misceval.callsimOrSuspend(Sk.builtins.property, topleft_getter, topleft_setter);

    var bottomleft_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([Sk.ffi.remapToPy(get_bottom(self)), Sk.ffi.remapToPy(get_left(self))]);
    });
    var bottomleft_setter = new Sk.builtin.func(function (self, val) {
        var bl = Sk.ffi.remapToJs(val);
        set_bottom(self, bl[0]);
        set_left(self, bl[1]);
    });
    $loc.bottomleft = Sk.misceval.callsimOrSuspend(Sk.builtins.property, bottomleft_getter, bottomleft_setter);

    var topright_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_top(self), get_right(self)]);
    });
    var topright_setter = new Sk.builtin.func(function (self, val) {
        var tr = Sk.ffi.remapToJs(val);
        set_top(self, tr[0]);
        set_right(self, tr[1]);
    });
    $loc.topright = Sk.misceval.callsimOrSuspend(Sk.builtins.property, topright_getter, topright_setter);

    var bottomright_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([Sk.ffi.remapToPy(get_bottom(self)), Sk.ffi.remapToPy(get_right(self))]);
    });
    var bottomright_setter = new Sk.builtin.func(function (self, val) {
        var br = Sk.ffi.remapToJs(val);
        set_bottom(self, br[0]);
        set_right(self, br[1]);
    });
    $loc.bottomright = Sk.misceval.callsimOrSuspend(Sk.builtins.property, bottomright_getter, bottomright_setter);

    var midtop_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_left(self) + Math.floor(get_width(self) / 2), get_top(self)]);
    });
    var midtop_setter = new Sk.builtin.func(function (self, val) {
        var mt = Sk.ffi.remapToJs(val);
        set_left(self, mt[0] - Math.floor(get_width(self) / 2));
        set_top(self, mt[1]);
    });
    $loc.midtop = Sk.misceval.callsimOrSuspend(Sk.builtins.property, midtop_getter, midtop_setter);

    var midbottom_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_centerx(self), get_bottom(self)])
    });
    var midbottom_setter = new Sk.builtin.func(function (self, val) {
        var mb = Sk.ffi.remapToJs(val);
        set_centerx(self, mb[0]);
        set_bottom(self, mb[1]);
    });
    $loc.midbottom = Sk.misceval.callsimOrSuspend(Sk.builtins.property, midbottom_getter, midbottom_setter);

    var midleft_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_left(self), get_centery(self)]);
    });
    var midleft_setter = new Sk.builtin.func(function (self, val) {
        var lm = Sk.ffi.remapToJs(val);
        set_left(self, lm[0]);
        set_centery(self, lm[1]);
    });
    $loc.midleft = Sk.misceval.callsimOrSuspend(Sk.builtins.property, midleft_getter, midleft_setter);

    var midright_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_right(self), get_centery(self)]);
    });
    var midright_setter = new Sk.builtin.func(function (self, val) {
        var rm = Sk.ffi.remapToJs(val);
        set_right(self, rm[0]);
        set_centery(self, rm[1]);
    });
    $loc.midright = Sk.misceval.callsimOrSuspend(Sk.builtins.property, midright_getter, midright_setter);

    var center_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_centerx(self), get_centery(self)]);
    });
    var center_setter = new Sk.builtin.func(function (self, val) {
        var c = Sk.ffi.remapToJs(val);
        set_centerx(self, c[0]);
        set_centery(self, c[1]);
    });
    $loc.center = Sk.misceval.callsimOrSuspend(Sk.builtins.property, center_getter, center_setter);

    var centerx_getter = new Sk.builtin.func(function (self) {
        return Sk.ffi.remapToPy(get_centerx(self));
    });
    var centerx_setter = new Sk.builtin.func(function (self, val) {
        set_centerx(self, Sk.ffi.remapToJs(val));
    });
    $loc.centerx = Sk.misceval.callsimOrSuspend(Sk.builtins.property, centerx_getter, centerx_setter);

    var centery_getter = new Sk.builtin.func(function (self) {
        return Sk.ffi.remapToPy(get_centery(self));
    });
    var centery_setter = new Sk.builtin.func(function (self) {
        set_centery(self, Sk.ffi.remapToPy(val));
    });
    $loc.centery = Sk.misceval.callsimOrSuspend(Sk.builtins.property, centery_getter, centery_setter);

    var size_getter = new Sk.builtin.func(function (self) {
        return Sk.builtin.tuple([get_width(self), get_height(self)]);
    });
    var size_setter = new Sk.builtin.func(function (self, val) {
        var s = Sk.ffi.remapToJs(val);
        set_width(self, s[0]);
        set_height(self, s[1]);
    });
    $loc.size = Sk.misceval.callsimOrSuspend(Sk.builtins.property, size_getter, size_setter);

    var w_getter = new Sk.builtin.func(function (self) {
        return Sk.ffi.remapToPy(get_width(self));
    });
    var w_setter = new Sk.builtin.func(function (self, val) {
        set_width(self, Sk.ffi.remapToJs(val));
    });
    $loc.w = Sk.misceval.callsimOrSuspend(Sk.builtins.property, w_getter, w_setter);

    var h_getter = new Sk.builtin.func(function (self) {
        return Sk.ffi.remapToPy(get_height(self));
    });
    var h_setter = new Sk.builtin.func(function (self, val) {
        set_height(self, Sk.ffi.remapToJs(val));
    });
    $loc.h = Sk.misceval.callsimOrSuspend(Sk.builtins.property, h_getter, h_setter);

    $loc.move = new Sk.builtin.func(function (self, x, y) {
        var newLeft = get_left(self) + Sk.ffi.remapToJs(x);
        var newTop = get_top(self) + Sk.ffi.remapToJs(y);
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([newLeft, newTop]), Sk.builtin.tuple([get_width(self), get_height(self)]))
    });
    $loc.move_ip = new Sk.builtin.func(function (self, x, y) {
        set_left(self, get_left(self) + Sk.ffi.remapToJs(x));
        set_top(self, get_top(self) + Sk.ffi.remapToJs(y));
        return Sk.builtin.none.none$;
    });
    $loc.inflate = new Sk.builtin.func(function (self, x, y) {
        x = Sk.ffi.remapToJs(x);
        y = Sk.ffi.remapToJs(y);
        var newLeft = get_left(self) - Math.floor(x / 2);
        var newTop = get_top(self) - Math.floor(y / 2);
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([newLeft, newTop]), Sk.builtin.tuple([get_width(self) + x, get_height(self) + y]));
    });
    $loc.inflate_ip = new Sk.builtin.func(function (self, x, y) {
        x = Sk.ffi.remapToJs(x);
        y = Sk.ffi.remapToJs(y);
        var newLeft = get_left(self) - Math.floor(x / 2);
        var newTop = get_top(self) - Math.floor(y / 2);
        set_left(self, newLeft);
        set_top(self, newTop);
        set_width(self, get_width(self) + x);
        set_height(self, get_height(self) + y);
    });
    $loc.clamp = new Sk.builtin.func(function (self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var x, y;
        if (selfw >= argw) {
            x = argx + argw / 2 - selfw / 2;
        } else if (selfx < argx) {

            x = argx;
        } else if (selfx + selfw > argx + argw) {
            x = argx + argw - selfw;
        } else {
            x = selfx;
        }

        if (selfh >= argh) {
            y = argy + argh / 2 - selfh / 2;
        } else if (selfy < argy) {
            y = argy;
        } else if (selfy + selfh > argy + argh) {
            y = argy + argh - selfh;
        } else {
            y = selfy;
        }
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([x, y]), Sk.builtin.tuple([selfw, selfh]));
    });
    $loc.clamp_ip = new Sk.builtin.func(function (self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var x, y;
        if (selfw >= argw) {
            x = argx + argw / 2 - selfw / 2;
        } else if (selfx < argx) {

            x = argx;
        } else if (selfx + selfw > argx + argw) {
            x = argx + argw - selfw;
        } else {
            x = selfx;
        }

        if (selfh >= argh) {
            y = argy + argh / 2 - selfh / 2;
        } else if (selfy < argy) {
            y = argy;
        } else if (selfy + selfh > argy + argh) {
            y = argy + argh - selfh;
        } else {
            y = selfy;
        }
        set_left(self, x);
        set_top(self, y);
    });
    $loc.clip = new Sk.builtin.func(function (self, argrect) {
        if (Sk.abstr.typeName(argrect) !== "Rect") {
            throw new Sk.builtin.TypeError("Argument must be rect style object");
        }
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var x, y, w, h;
        /* Left */
        if ((selfx >= argx) && (selfx < (argx + argw))) {
            x = selfx;
        } else if ((argx >= selfx) && (argx < (selfx + selfw))) {
            x = argx;
        } else {
            return Sk.misceval.callsim(PygameLib.RectType,
                Sk.builtin.tuple([selfx, selfy]), Sk.builtin.tuple([0, 0]));
        }
        /* Right */
        if (((selfx + selfw) > argx) && ((selfx + selfw) <= (argx + argw))) {
            w = (selfx + selfw) - x;
        } else if (((argx + argw) > selfx) && ((argx + argw) <= (selfx + selfw))) {
            w = (argx + argw) - x;
        } else {
            return Sk.misceval.callsim(PygameLib.RectType,
                Sk.builtin.tuple([selfx, selfy]), Sk.builtin.tuple([0, 0]));
        }
        /* Top */
        if ((selfy >= argy) && (selfy < (argy + argh))) {
            y = selfy;
        } else if ((argy >= selfy) && (argy < (selfy + selfh))) {
            y = argy;
        } else {
            return Sk.misceval.callsim(PygameLib.RectType,
                Sk.builtin.tuple([selfx, selfy]), Sk.builtin.tuple([0, 0]));
        }
        /* Bottom */
        if (((selfy + selfh) > argy) && ((selfy + selfh) <= (argy + argh))) {
            h = (selfy + selfh) - y;
        } else if (((argy + argh) > selfy) && ((argy + argh) <= (selfy + selfh))) {
            h = (argy + argh) - y;
        } else {
            return Sk.misceval.callsim(PygameLib.RectType,
                Sk.builtin.tuple([selfx, selfy]), Sk.builtin.tuple([0, 0]));
        }
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([x, y]), Sk.builtin.tuple([w, h]));
    });
    $loc.union = new Sk.builtin.func(function (self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var x, y, w, h;
        x = Math.min(argx, selfx);
        y = Math.min(argy, selfy);
        w = Math.max(selfx + selfw, argx + argw) - x;
        h = Math.max(selfy + selfh, argy + argh) - y;
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([x, y]), Sk.builtin.tuple([w, h]));
    });
    $loc.union_ip = new Sk.builtin.func(function (self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var x, y, w, h;
        x = Math.min(argx, selfx);
        y = Math.min(argy, selfy);
        w = Math.max(selfx + selfw, argx + argw) - x;
        h = Math.max(selfy + selfh, argy + argh) - y;
        set_left(self, x);
        set_top(self, y);
        set_width(self, w);
        set_height(self, h);
    });
    $loc.unionall = new Sk.builtin.func(function (self, list) {
        var l = get_left(self);
        var t = get_top(self);
        var r = l + get_width(self);
        var b = t + get_height(self);
        for (var i = 0; i < list.v.length; i++) {
            l = Math.min(l, get_left(list.v[i]));
            t = Math.min(t, get_top(list.v[i]));
            r = Math.max(r, get_right(list.v[i]));
            b = Math.max(b, get_bottom(list.v[i]));
        }
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([l, t]), Sk.builtin.tuple([r - l, b - t]));
    });
    $loc.unionall_ip = new Sk.builtin.func(function (self, list) {
        var l = get_left(self);
        var t = get_top(self);
        var r = l + get_width(self);
        var b = t + get_height(self);
        for (var i = 0; i < list.v.length; i++) {
            l = Math.min(l, get_left(list.v[i]));
            t = Math.min(t, get_top(list.v[i]));
            r = Math.max(r, get_right(list.v[i]));
            b = Math.max(b, get_bottom(list.v[i]));
        }
        set_left(self, l);
        set_top(self, t);
        set_width(self, r - l);
        set_height(self, b - t);
    });
    $loc.fit = new Sk.builtin.func(function (self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var x, y, w, h;
        var xratio, yratio, maxratio;
        xratio = selfw / argw;
        yratio = selfh / argh;
        maxratio = (xratio > yratio) ? xratio : yratio;

        w = Math.round(selfw / maxratio);
        h = Math.round(selfh / maxratio);

        x = argx + Math.floor((argw - w) / 2);
        y = argy + Math.floor((argh - h) / 2);
        return Sk.misceval.callsim(PygameLib.RectType,
            Sk.builtin.tuple([x, y]), Sk.builtin.tuple([w, h]));
    });
    $loc.normalize = new Sk.builtin.func(function (self) {
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        if (selfw < 0) {
            selfx += selfw;
            selfw = -selfw;
        }
        if (selfh < 0) {
            selfy += selfh;
            selfh = -selfh;
        }
        set_left(self, selfx);
        set_width(self, selfw);
        set_top(self, selfy);
        set_height(self, selfh);
    });
    $loc.contains = new Sk.builtin.func(function (self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var contained = (selfx <= argx) && (selfy <= argy) &&
            (selfx + selfw >= argx + argw) &&
            (selfy + selfh >= argy + argh) &&
            (selfx + selfw > argx) &&
            (selfy + selfh > argy);
        return Sk.ffi.remapToPy(contained);
    });
    $loc.collidepoint = new Sk.builtin.func(function (self, x, y) {
        if (Sk.abstr.typeName(x) === "tuple" && y === undefined) {
            var xy = Sk.ffi.remapToJs(x);
            x = xy[0];
            y = xy[1];
        } else if (Sk.abstr.typeName(x) === "int" && Sk.abstr.typeName(y) === "int") {
            x = Sk.ffi.remapToJs(x);
            y = Sk.ffi.remapToJs(y);
        } else {
            throw new Sk.builtin.TypeError("argument must contain two numbers");
        }
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        var inside = x >= selfx && x < selfx + selfw &&
            y >= selfy && y < selfy + selfh;
        return Sk.ffi.remapToPy(inside);
    });

    function do_rects_intersect(self, argrect) {
        var argx = get_left(argrect);
        var argy = get_top(argrect);
        var argw = get_width(argrect);
        var argh = get_height(argrect);
        var selfx = get_left(self);
        var selfy = get_top(self);
        var selfw = get_width(self);
        var selfh = get_height(self);
        return (selfx < argx + argw && selfy < argy + argh &&
            selfx + selfw > argx && selfy + selfh > argy);
    }

    $loc.colliderect = new Sk.builtin.func(function (self, argrect) {
        if (Sk.abstr.typeName(argrect) !== "Rect") {
            throw new Sk.builtin.TypeError("Argument must be rect style object");
        }
        return Sk.ffi.remapToPy(do_rects_intersect(self, argrect))
    });
    $loc.collidelist = new Sk.builtin.func(function (self, list) {
        if (Sk.abstr.typeName(list) !== "list") {
            throw new Sk.builtin.TypeError("Argument must be a sequence of rectstyle objects.");
        }
        var ret = -1;
        for (var i = 0; i < list.v.length; i++) {
            if (Sk.abstr.typeName(list.v[i]) !== "Rect") {
                throw new Sk.builtin.TypeError("Argument must be a sequence of rectstyle objects.");
            }
            if (do_rects_intersect(self, list.v[i])) {
                ret = i;
                break;
            }
        }
        return Sk.ffi.remapToPy(ret);
    });
    $loc.collidelistall = new Sk.builtin.func(function (self, list) {
        if (Sk.abstr.typeName(list) !== "list") {
            throw new Sk.builtin.TypeError("Argument must be a sequence of rectstyle objects.");
        }
        var ret = [];
        for (var i = 0; i < list.v.length; i++) {
            if (Sk.abstr.typeName(list.v[i]) !== "Rect") {
                throw new Sk.builtin.TypeError("Argument must be a sequence of rectstyle objects.");
            }
            if (do_rects_intersect(self, list.v[i])) {
                ret.push(i);
            }
        }
        return Sk.ffi.remapToPy(ret);
    });
};
