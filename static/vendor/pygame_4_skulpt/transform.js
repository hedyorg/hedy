let $builtinmodule = function (name) {
    let mod = {};
    mod.flip = new Sk.builtin.func(function (surf, xbool, ybool) {
        if (Sk.abstr.typeName(surf) !== "Surface") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        if (Sk.abstr.typeName(xbool) !== "bool" || Sk.abstr.typeName(ybool) !== "bool") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        let t = Sk.builtin.tuple([surf.width, surf.height]);
        let ret = Sk.misceval.callsim(PygameLib.SurfaceType, t);
        ret.context2d.save();
        let xb = Sk.ffi.remapToJs(xbool);
        let xflip = xb ? -1 : 1;
        let yb = Sk.ffi.remapToJs(ybool);
        let yflip = yb ? -1 : 1;
        ret.context2d.scale(xflip, yflip);
        ret.context2d.drawImage(surf.offscreen_canvas, -surf.width, 0, surf.width, surf.height);
        ret.context2d.restore();
        return ret;
    });

    function scale(surf, size, dest) {
        if (Sk.abstr.typeName(surf) !== "Surface") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        if (Sk.abstr.typeName(size) !== "tuple") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        let sz = Sk.ffi.remapToJs(size);
        let w = Math.round(sz[0]);
        let h = Math.round(sz[1]);
        if (w === 0 || h === 0) {
            if (dest !== undefined && dest !== Sk.builtins.none.none$) {
                dest.context2d.drawImage(surf.offscreen_canvas, 0, 0);
            }
            return surf;
        }
        let t = Sk.builtin.tuple([w, h]);
        let xs = w / surf.width;
        let ys = h / surf.height;
        let ret = Sk.misceval.callsim(PygameLib.SurfaceType, t);
        ret.context2d.save();
        ret.context2d.scale(xs, ys);
        ret.context2d.drawImage(surf.offscreen_canvas, 0, 0);
        ret.context2d.restore();
        if (dest !== undefined && dest !== Sk.builtins.none.none$) {
            dest.context2d.drawImage(ret.offscreen_canvas, 0, 0);
        }
        return ret;
    }

    mod.scale = new Sk.builtin.func(scale);
    mod.smoothscale = new Sk.builtin.func(scale);
    mod.rotate = new Sk.builtin.func(function (surf, angle) {
        if (Sk.abstr.typeName(surf) !== "Surface") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        let a = Sk.ffi.remapToJs(angle);
        let w = surf.width;
        let h = surf.height;
        let t = Sk.builtin.tuple([1.5 * w, 1.5 * h]);
        let ret = Sk.misceval.callsim(PygameLib.SurfaceType, t);
        ret.context2d.save();
        ret.context2d.translate(w / 2, h / 2);
        ret.context2d.rotate(-a * Math.PI / 180);
        ret.context2d.translate(-w / 2, -h / 2);
        ret.context2d.drawImage(surf.offscreen_canvas, 0, 0);
        ret.context2d.restore();
        return ret;
    });
    mod.rotozoom = new Sk.builtin.func(function (surf, angle, sc) {
        if (Sk.abstr.typeName(surf) !== "Surface") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        let scale = Sk.ffi.remapToJs(sc);
        let a = Sk.ffi.remapToJs(angle);
        let w = surf.width;
        let h = surf.height;
        let t = Sk.builtin.tuple([2 * scale * w, 2 * scale * h]);
        let ret = Sk.misceval.callsim(PygameLib.SurfaceType, t);
        ret.context2d.save();
        ret.context2d.scale(scale, scale);
        w *= scale;
        h *= scale;
        ret.context2d.translate(w / 2, h / 2);
        ret.context2d.rotate(-a * Math.PI / 180);
        ret.context2d.translate(-w / 2, -h / 2);
        ret.context2d.drawImage(surf.offscreen_canvas, 0, 0);
        ret.context2d.restore();
        return ret;
    });
    mod.scale2x = new Sk.builtin.func(function (surf, dest) {
        if (Sk.abstr.typeName(surf) !== "Surface") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        let w = surf.width;
        let h = surf.height;
        let t = Sk.builtin.tuple([2 * w, 2 * h]);
        let ret = Sk.misceval.callsim(PygameLib.SurfaceType, t);
        ret.context2d.save();
        ret.context2d.scale(2, 2);
        ret.context2d.drawImage(surf.offscreen_canvas, 0, 0);
        ret.context2d.restore();
        if (dest !== undefined && dest !== Sk.builtins.none.none$) {
            dest.context2d.drawImage(ret.offscreen_canvas, 0, 0);
        }
        return ret;
    });
    mod.chop = new Sk.builtin.func(function (surf, rect) {
        if (Sk.abstr.typeName(surf) !== "Surface") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        if (Sk.abstr.typeName(rect) !== "Rect") {
            throw new Sk.builtin.TypeError("Wrong arguments");
        }
        let rr = PygameLib.extract_rect(rect);
        let x1 = rr[0];
        let y1 = rr[1];
        let x2 = rr[0] + rr[2];
        let y2 = rr[1] + rr[3];
        let w = surf.width;
        let h = surf.height;
        let rw = w - x2;
        let rh = h - y2;
        let t = Sk.builtin.tuple([w, h]);
        let ret = Sk.misceval.callsim(PygameLib.SurfaceType, t);
        ret.context2d.drawImage(surf.offscreen_canvas, 0, 0, x1, y1, 0, 0, x1, y1);
        ret.context2d.drawImage(surf.offscreen_canvas, 0, y2, x1, rh, 0, y1, x1, rh);
        ret.context2d.drawImage(surf.offscreen_canvas, x2, 0, rw, y1, x1, 0, rw, y1);
        ret.context2d.drawImage(surf.offscreen_canvas, x2, y2, rw, rh, x1, y1, rw, rh);
        return ret;
    });
    return mod;
};
