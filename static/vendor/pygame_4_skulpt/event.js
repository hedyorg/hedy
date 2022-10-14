var $builtinmodule = function (name) {
    var mod = {};
    mod.get = new Sk.builtin.func(get_event);
    mod.EventType = Sk.misceval.buildClass(mod, event_EventType_f, "EventType", []);
    PygameLib.EventType = mod.EventType;
    mod.Event = new Sk.builtin.func(function (type, dict) {
        return Sk.misceval.callsim(mod.EventType, type, dict)
    });

    mod.wait = new Sk.builtin.func(function () {
        return new Sk.misceval.promiseToSuspension(new Promise(function (resolve) {
            var f = function () {
                if (PygameLib.eventQueue.length) {
                    var event = PygameLib.eventQueue.splice(0, 1)[0];
                    var type = Sk.ffi.remapToPy(event[0]);
                    var dictjs = event[1];
                    kvs = [];
                    for (k in dictjs) {
                        kvs.push(Sk.ffi.remapToPy(k));
                        kvs.push(Sk.ffi.remapToPy(dictjs[k]));
                    }
                    var dict = new Sk.builtin.dict(kvs);
                    var e = Sk.misceval.callsim(PygameLib.EventType, type, dict);
                    resolve(e);
                }
                else
                    Sk.setTimeout(f, 10);
            };

            Sk.setTimeout(f, 10);
        }));
    });
    return mod;
};

//pygame.event module
//pygame.event.get()
//get() -> Eventlist
//get(type) -> Eventlist
//get(typelist) -> Eventlist
var get_event = function (types) {
    // if (types){
    Sk.builtin.pyCheckArgs('get_event', arguments, 0, 1, false, false);
    var list = [];
    var t, d;
    var types_js = types ? Sk.ffi.remapToJs(types) : [];
    var queue = types ? (Sk.abstr.typeName(types) === "list" ? PygameLib.eventQueue.filter(e => types_js.includes(e[0])) : PygameLib.eventQueue.filter(e => e[0] === types_js))
        : PygameLib.eventQueue;
    for (var i = 0; i < queue.length; i++) {
        var event = queue[i];
        var type = Sk.ffi.remapToPy(event[0]);
        var dictjs = event[1];
        kvs = [];
        for (k in dictjs) {
            kvs.push(Sk.ffi.remapToPy(k));
            kvs.push(Sk.ffi.remapToPy(dictjs[k]));
        }
        var dict = new Sk.builtin.dict(kvs);
        var e = Sk.misceval.callsim(PygameLib.EventType, type, dict);
        list.push(e);
    }
    queue.splice(0);
    return new Sk.builtin.list(list);
    // }
    // return new Sk.builtin.list([]);
};

function event_EventType_f($gbl, $loc) {
    var dictPyStr = new Sk.builtin.str('dict'),
        typePyStr = new Sk.builtin.str('type');
    $loc.__init__ = new Sk.builtin.func(function (self, type, dict) {
        Sk.builtin.pyCheckArgs('__init__', arguments, 2, 3, false, false);
        dict = dict || new Sk.builtin.dict();
        Sk.abstr.sattr(self, dictPyStr, dict, false);
        Sk.abstr.sattr(self, typePyStr, type, false);
        dictjs = Sk.ffi.remapToJs(dict);
        for (k in dictjs) {
            Sk.abstr.sattr(self, new Sk.builtin.str(k), Sk.ffi.remapToPy(dictjs[k]), false);
        }
        return Sk.builtin.none.none$;
    });
    $loc.__init__.co_name = new Sk.builtin.str('__init__');
    $loc.__init__.co_varnames = ['self', 'type', 'dict'];

    $loc.__repr__ = new Sk.builtin.func(function (self) {
        var dict = Sk.ffi.remapToJs(Sk.abstr.gattr(self, dictPyStr, false));
        var type = Sk.ffi.remapToJs(Sk.abstr.gattr(self, typePyStr, false));
        return Sk.ffi.remapToPy('<Event(' + type + ' ' + dict + ')>');
    });
    $loc.__repr__.co_name = new Sk.builtin.str('__repr__');
    $loc.__repr__.co_varnames = ['self'];

}
