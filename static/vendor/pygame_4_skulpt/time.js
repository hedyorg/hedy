var $builtinmodule = function (name) {
    mod = {};
    mod.wait = new Sk.builtin.func(function (amount) {
        var t_m = Sk.importModule("time", false, true);
        var sec = Sk.ffi.remapToJs(amount) / 1000;
        return Sk.misceval.callsimOrSuspend(t_m.$d['sleep'], Sk.ffi.remapToPy(sec));
    });

    mod.get_ticks = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(new Date() - PygameLib.initial_time);
    });
    mod.delay = new Sk.builtin.func(function (amount) {
        var t_m = Sk.importModule("time", false, false);
        var sec = Sk.ffi.remapToJs(amount) / 1000;
        return Sk.misceval.callsimOrSuspend(t_m.$d['sleep'], Sk.ffi.remapToPy(sec));
    });
    mod.set_timer = new Sk.builtin.func(function (eventid, milliseconds) {
        var event = Sk.ffi.remapToJs(eventid);
        var ms = Sk.ffi.remapToJs(milliseconds);
        if (PygameLib.eventTimer[event]) {
            clearInterval(PygameLib.eventTimer[event].timer);
        }
        else {
            PygameLib.eventTimer[event] = {};
            PygameLib.eventTimer[event].f = function () {
                var e = [event, {}];
                PygameLib.eventQueue.unshift(e);
            }
        }
        if (ms) {
            PygameLib.eventTimer[event].timer = setInterval(PygameLib.eventTimer[event].f, ms);
        }
        return mod;
    });

    mod.Clock = Sk.misceval.buildClass(mod, time_Clock, 'Clock', []);
    PygameLib.ClockType = mod.Clock;
    return mod;
};

function time_Clock($gbl, $loc) {
    var prevTimePyStr = new Sk.builtin.str('prevTime'),
        getTimePyStr = new Sk.builtin.str('getTime'),
        rawTimePyStr = new Sk.builtin.str('rawTime'),
        fpsArrayPyStr = new Sk.builtin.str('fpsArray'),
        fpsIdxPyStr = new Sk.builtin.str('fpsIdx');
    $loc.__init__ = new Sk.builtin.func(function (self) {

        Sk.abstr.sattr(self, prevTimePyStr, Sk.ffi.remapToPy(Date.now()), false);
        Sk.abstr.sattr(self, getTimePyStr, Sk.builtin.none.none$, false);
        Sk.abstr.sattr(self, rawTimePyStr, Sk.ffi.remapToPy(0), false);
        Sk.abstr.sattr(self, fpsArrayPyStr, Sk.ffi.remapToPy([]), false);
        Sk.abstr.sattr(self, fpsIdxPyStr, Sk.ffi.remapToPy(0));
        return Sk.builtin.none.none$;
    }, $gbl);
    $loc.__init__.co_name = new Sk.builtin.str('__init__');

    $loc.tick = new Sk.builtin.func(function (self, framerate) {

        var currTime = Date.now();
        var mills = 0;
        if (Sk.ffi.remapToJs(Sk.abstr.gattr(self, prevTimePyStr) !== null)) {
            var prevTime = Sk.ffi.remapToJs(Sk.abstr.gattr(self, prevTimePyStr, false));
            mills = (currTime - prevTime);
        }
        Sk.abstr.sattr(self, prevTimePyStr, Sk.ffi.remapToPy(currTime), false);
        Sk.abstr.sattr(self, getTimePyStr, Sk.ffi.remapToPy(mills), false);
        var arr = Sk.ffi.remapToJs(Sk.abstr.gattr(self, fpsArrayPyStr, false));
        var idx = Sk.ffi.remapToJs(Sk.abstr.gattr(self, fpsIdxPyStr, false));
        if (arr.length < 10) {
            arr.push(mills);
        } else {
            arr[idx] = mills;
        }
        idx = (idx + 1) % 10;
        Sk.abstr.sattr(self, fpsArrayPyStr, Sk.ffi.remapToPy(arr), false);
        Sk.abstr.sattr(self, fpsIdxPyStr, Sk.ffi.remapToPy(idx), false);
        if (framerate !== undefined) {
            var timeout = 1000 / Sk.ffi.remapToJs(framerate);
            return new Sk.misceval.promiseToSuspension(
                new Promise(function (resolve) {
                    var f = function () {
                        Sk.abstr.sattr(self, rawTimePyStr, Sk.ffi.remapToPy(Date.now() - currTime), false);
                        resolve(mills);
                    };

                    if (PygameLib.running) {
                        Sk.setTimeout(f, timeout);
                    }
                }));
        }
        Sk.abstr.sattr(self, rawTimePyStr, Sk.ffi.remapToPy(Date.now() - currTime), false);
        return Sk.ffi.remapToPy(mills);
    }, $gbl);
    $loc.tick.co_name = new Sk.builtin.str('tick');
    $loc.tick.co_varnames = ['framerate'];
    $loc.tick.$defaults = [Sk.ffi.remapToPy(0)];

    $loc.tick_busy_loop = new Sk.builtin.func(function (self, framerate) {
        var currTime = Date.now();
        var mills = 0;
        if (Sk.ffi.remapToJs(Sk.abstr.gattr(self, prevTimePyStr, false)) !== null) {
            var prevTime = Sk.ffi.remapToJs(Sk.abstr.gattr(self, prevTimePyStr, false));
            mills = (currTime - prevTime);
        }
        Sk.abstr.sattr(self, prevTimePyStr, Sk.ffi.remapToPy(currTime), false);
        Sk.abstr.sattr(self, getTimePyStr, Sk.ffi.remapToPy(mills), false);

        if (framerate !== undefined) {
            var timeout = 1000 / Sk.ffi.remapToJs(framerate);
            return new Sk.misceval.promiseToSuspension(
                new Promise(function (resolve) {
                    var f = function () {
                        Sk.abstr.sattr(self, rawTimePyStr, Sk.ffi.remapToPy(Date.now() - currTime), false);
                        resolve(mills);
                    };
                    if (PygameLib.running) {
                        Sk.setTimeout(f, timeout);
                    }
                }));
        }
        Sk.abstr.sattr(self, rawTimePyStr, Sk.ffi.remapToPy(Date.now() - currTime), false);
        return Sk.ffi.remapToPy(mills);
    }, $gbl);
    $loc.tick_busy_loop.co_name = new Sk.builtin.str('tick_busy_loop');
    $loc.tick_busy_loop.co_varnames = ['framerate'];
    $loc.tick_busy_loop.$defaults = [Sk.ffi.remapToPy(0)];

    $loc.get_time = new Sk.builtin.func(function (self) {
        return Sk.abstr.gattr(self, getTimePyStr, false);
    });
    $loc.get_time.co_name = new Sk.builtin.str('get_time');

    $loc.get_rawtime = new Sk.builtin.func(function (self) {
        return Sk.abstr.gattr(self, rawTimePyStr, false);
    });
    $loc.get_rawtime.co_name = new Sk.builtin.str('get_rawtime');

    $loc.get_fps = new Sk.builtin.func(function (self) {
        var arr = Sk.ffi.remapToJs(Sk.abstr.gattr(self, fpsArrayPyStr, false));
        if (arr.length < 10 || arr[0] === 0) {
            return Sk.ffi.remapToPy(0);
        }
        var sum = 0;
        for (var i = 0; i < 10; i++) {
            sum += arr[i];
        }
        return Sk.ffi.remapToPy(sum / 10);
    });
}

time_Clock.co_name = new Sk.builtin.str('Clock');

