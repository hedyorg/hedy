var $builtinmodule = function (name) {
    mod = {};
    mod.rect = new Sk.builtin.func(draw_rect);
    mod.polygon = new Sk.builtin.func(draw_polygon);
    mod.circle = new Sk.builtin.func(draw_circle);
    mod.ellipse = new Sk.builtin.func(draw_ellipse);
    mod.arc = new Sk.builtin.func(draw_arc);
    mod.line = new Sk.builtin.func(draw_line);
    mod.lines = new Sk.builtin.func(draw_lines);
    mod.aaline = new Sk.builtin.func(draw_aaline);
    mod.aalines = new Sk.builtin.func(draw_aalines);
    return mod;
};

//returns Rect object used as bounding box for drawing functions
var bbox = function (min_h, max_h, min_w, max_w) {
    var width = max_w - min_w;
    var height = max_h - min_h;
    var top = min_h;
    var left = min_w;
    t = Sk.builtin.tuple([left, top]);
    return Sk.misceval.callsim(PygameLib.RectType, Sk.builtin.tuple([left, top]), Sk.builtin.tuple([width, height]));
};

//pygame.draw.rect()
//rect(Surface, color, Rect, width=0) -> Rect
var draw_rect = function (surface, color, rect, width = 0) {
    var ctx = surface.context2d;
    var color_js = PygameLib.extract_color(color);
    var width_js = Sk.ffi.remapToJs(width);
    var rect_js = PygameLib.extract_rect(rect);

    var left = rect_js[0];
    var top = rect_js[1];
    var width = rect_js[2];
    var height = rect_js[3];

    if (width_js) {
        ctx.lineWidth = width_js;
        ctx.strokeStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.strokeRect(left, top, width, height);
    } else {
        ctx.fillStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.fillRect(left, top, width, height);
    }

    return Sk.misceval.callsim(PygameLib.RectType, Sk.builtin.tuple([left, top]), Sk.builtin.tuple([width, height]));
};

//pygame.draw.polygon()
//polygon(Surface, color, pointlist, width=0) -> Rect
var draw_polygon = function (surface, color, pointlist, width = 0) {
    return draw_lines(surface, color, true, pointlist, width);
};

//pygame.draw.circle()
//circle(Surface, color, pos, radius, width=0) -> Rect
var draw_circle = function (surface, color, pos, radius, width = 0) {
    var ctx = surface.context2d;
    var width_js = Sk.ffi.remapToJs(width);
    var center = Sk.ffi.remapToJs(pos);
    var rad = Sk.ffi.remapToJs(radius);
    var color_js = PygameLib.extract_color(color);
    ctx.beginPath();
    ctx.arc(center[0], center[1], rad, 0, 2 * Math.PI);
    if (width_js) {
        ctx.lineWidth = width_js;
        ctx.strokeStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.stroke();
    } else {
        ctx.fillStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.fill();
    }

    return bbox(center[1] - rad, center[1] + rad, center[0] - rad, center[0] + rad);
};

//pygame.draw.arc()
//arc(Surface, color, Rect, start_angle, stop_angle, width=1) -> Rect
var draw_arc = function (surface, color, rect, start_angle, stop_angle, width = 0) {
    return draw_oval(surface, color, rect, start_angle, stop_angle, width, false);
};

//pygame.draw.arg()
//ellipse(Surface, color, Rect, width=0) -> Rect
var draw_ellipse = function (surface, color, rect, width = 0) {
    return draw_oval(surface, color, rect, 0, 2 * Math.PI, width, true);
};

//help function
var draw_oval = function (surface, color, rect, start_angle, stop_angle, width, ellipse = false) {
    var ctx = surface.context2d;
    var width_js = Sk.ffi.remapToJs(width);
    var color_js = PygameLib.extract_color(color);
    var rect_js = PygameLib.extract_rect(rect);
    var angles = [0, 0];
    angles[0] = Sk.ffi.remapToJs(start_angle);
    angles[1] = Sk.ffi.remapToJs(stop_angle);
    var center = [0, 0];
    center[0] = rect_js[0] + rect_js[2] / 2;
    center[1] = rect_js[1] + rect_js[3] / 2;

    ctx.beginPath();

    ctx.ellipse(center[0], center[1], rect_js[2] / 2, rect_js[3] / 2, 0, -angles[0], -angles[1], true);

    if (width_js) {
        ctx.lineWidth = width_js;
        ctx.strokeStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.stroke();
    } else if (ellipse) {
        ctx.fillStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.fill();
    }

    return Sk.misceval.callsim(PygameLib.RectType, Sk.builtin.tuple([rect_js[0], rect_js[1]]), Sk.builtin.tuple([rect_js[2], rect_js[3]]));
};

//pygame.draw.line()
//line(Surface, color, start_pos, end_pos, width=1) -> Rect
var draw_line = function (surface, color, start_pos, end_pos, width = 1) {
    var width_js = Sk.ffi.remapToJs(width);
    var start_pos_js = Sk.ffi.remapToJs(start_pos);
    var end_pos_js = Sk.ffi.remapToJs(end_pos);
    var color_js = PygameLib.extract_color(color);
    var ctx = surface.context2d;
    var ax = start_pos_js[0];
    var ay = start_pos_js[1];
    var bx = end_pos_js[0];
    var by = end_pos_js[1];
    var points;
    if (Math.abs(ax - bx) <= Math.abs(ay - by)) {
        points = [Sk.builtin.tuple([ax - width_js / 2, ay]), Sk.builtin.tuple([ax + width_js / 2, ay]),
            Sk.builtin.tuple([bx + width_js / 2, by]), Sk.builtin.tuple([bx - width_js / 2, by])];
        points = Sk.builtin.list(points);
    }
    else {
        points = [Sk.builtin.tuple([ax, ay - width_js / 2]), Sk.builtin.tuple([ax, ay + width_js / 2]),
            Sk.builtin.tuple([bx, by + width_js / 2]), Sk.builtin.tuple([bx, by - width_js / 2])];
        points = Sk.builtin.list(points);
    }
    draw_polygon(surface, color, points);
    var left = Math.min(start_pos_js[0], end_pos_js[0]);
    var right = Math.max(start_pos_js[0], end_pos_js[0]);
    var top = Math.min(start_pos_js[1], end_pos_js[1]);
    var bot = Math.max(start_pos_js[1], end_pos_js[1]);
    return bbox(top, bot, left, right);
};

//pygame.draw.lines()
//lines(Surface, color, closed, pointlist, width=1) -> Rect
var draw_lines = function (surface, color, closed, pointlist, width = 1) {
    var width_js = Sk.ffi.remapToJs(width);
    var closed_js = Sk.ffi.remapToJs(closed);
    var pointlist_js = Sk.ffi.remapToJs(pointlist);
    var color_js = PygameLib.extract_color(color);
    var ctx = surface.context2d;
    if (!width_js) {
        ctx.beginPath();
        ctx.lineWidth = width_js;
        var first_point = pointlist_js[0];
        var max_h = first_point[1], max_w = first_point[0];
        var min_h = first_point[1], min_w = first_point[0];
        ctx.moveTo(first_point[0], first_point[1]);
        for (var i = 0; i < pointlist_js.length; i++) {
            ctx.lineTo(pointlist_js[i][0], pointlist_js[i][1]);
            max_w = Math.max(max_w, pointlist_js[i][0]);
            min_w = Math.min(min_w, pointlist_js[i][0]);
            max_h = Math.max(max_h, pointlist_js[i][1]);
            min_h = Math.min(min_h, pointlist_js[i][1]);
        }
        if (closed_js) {
            ctx.closePath();
        }
    }
    else {
        for (var i = 0; i < pointlist_js.length - 1; i++) {
            draw_line(surface, color, Sk.builtin.tuple([pointlist_js[i][0], pointlist_js[i][1]]), Sk.builtin.tuple([pointlist_js[i + 1][0], pointlist_js[i + 1][1]]), width);
        }
        return bbox(0, 0, 0, 0);
    }

    if (width_js) {
        ctx.strokeStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.stroke();
    } else {
        ctx.fillStyle = 'rgba(' + color_js[0] + ', ' + color_js[1] + ', ' + color_js[2] + ', ' + color_js[3] + ')';
        ctx.fill();
    }
    return bbox(min_h, max_h, min_w, max_w);
};

//pygame.draw.aaline()
//aaline(Surface, color, startpos, endpos, blend=1) -> Rect
var draw_aaline = function (surface, color, startpos, endpos, blend = 1) {
    return draw_line(surface, color, startpos, endpos);
};

//pygame.draw.aalines()
//aalines(Surface, color, closed, pointlist, blend=1) -> Rect
var draw_aalines = function (surface, color, closed, pointlist, blend = 1) {
    return draw_lines(surface, color, closed, pointlist);
};
