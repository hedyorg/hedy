/**
 * Debugger support for skulpt module
 */

var Sk = Sk || {}; //jshint ignore:line

// function hasOwnProperty(obj, prop) {
//     var proto = obj.constructor.prototype;
//     return (prop in obj) &&
//         (!(prop in proto) || proto[prop] !== obj[prop]);
// }

Sk.Breakpoint = function(filename, lineno, colno) {
    this.filename = filename;
    this.lineno = lineno;
    this.colno = colno;
    this.enabled = true;
    this.ignore_count = 0;
};

Sk.Debugger = function(filename, output_callback, editor_ref) {
    this.dbg_breakpoints = {};
    this.tmp_breakpoints = {};
    this.suspension_stack = [];
    this.current_suspension = -1;
    this.eval_callback = null;
    this.suspension = null;
    this.output_callback = output_callback;
    this.step_mode = false;
    this.filename = filename;
    this.editor_ref = editor_ref;
    this.code = "";
};

Sk.Debugger.prototype.set_code = function(code) {
    this.code = code;
}

Sk.Debugger.prototype.print = function(txt) {
    console.log(txt);
};

Sk.Debugger.prototype.get_source_line = function(lineno) {
    if (this.code.length > 0) {
        return this.code[lineno];
    }
    
    return "";
};

Sk.Debugger.prototype.move_up_the_stack = function() {
    this.current_suspension = Math.min(this.current_suspension + 1, this.suspension_stack.length - 1);
};

Sk.Debugger.prototype.move_down_the_stack = function() {
    this.current_suspension = Math.max(this.current_suspension - 1, 0);
};

Sk.Debugger.prototype.enable_step_mode = function() {
    this.step_mode = true;
};

Sk.Debugger.prototype.disable_step_mode = function() {
    this.step_mode = false;
};

Sk.Debugger.prototype.get_suspension_stack = function() {
    return this.suspension_stack;
};

Sk.Debugger.prototype.get_active_suspension = function() {
    if (this.suspension_stack.length === 0) {
        return null;
    }

    return this.suspension_stack[this.current_suspension];
};

Sk.Debugger.prototype.generate_breakpoint_key = function(filename, lineno, colno) {
    var key = filename + "-" + lineno;
    return key;
};

Sk.Debugger.prototype.check_breakpoints = function(filename, lineno, colno, globals, locals) {
    // If Step mode is enabled then ignore breakpoints since we will just break
    // at every line.
    if (this.step_mode === true) {
        return true;
    }
    
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    if (this.dbg_breakpoints.hasOwnProperty(key) &&
        this.dbg_breakpoints[key].enabled === true) {
        var bp = null;
        if (this.tmp_breakpoints.hasOwnProperty(key)) {
            delete this.dbg_breakpoints[key];
            delete this.tmp_breakpoints[key];
            return true;
        }
        
        this.dbg_breakpoints[key].ignore_count -= 1;
        this.dbg_breakpoints[key].ignore_count = Math.max(0, this.dbg_breakpoints[key].ignore_count);
        
        bp = this.dbg_breakpoints[key];
        if (bp.ignore_count === 0) {
            return true;
        } else {
            return false;
        }
    }
    return false;
};

Sk.Debugger.prototype.get_breakpoints_list = function() {
    return this.dbg_breakpoints;
};

Sk.Debugger.prototype.disable_breakpoint = function(filename, lineno, colno) {
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    
    if (this.dbg_breakpoints.hasOwnProperty(key)) {
        this.dbg_breakpoints[key].enabled = false;
    }
};

Sk.Debugger.prototype.enable_breakpoint = function(filename, lineno, colno) {
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    
    if (this.dbg_breakpoints.hasOwnProperty(key)) {
        this.dbg_breakpoints[key].enabled = true;
    }
};

Sk.Debugger.prototype.clear_breakpoint = function(filename, lineno, colno) {
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    if (this.dbg_breakpoints.hasOwnProperty(key)) {
        delete this.dbg_breakpoints[key];
        return null;
    } else {
        return "Invalid breakpoint specified: " + filename + " line: " + lineno;
    }
};

Sk.Debugger.prototype.clear_all_breakpoints = function() {
    this.dbg_breakpoints = {};
    this.tmp_breakpoints = {};
};

Sk.Debugger.prototype.set_ignore_count = function(filename, lineno, colno, count) {
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    if (this.dbg_breakpoints.hasOwnProperty(key)) {
        var bp = this.dbg_breakpoints[key];
        bp.ignore_count = count;
    }
};

Sk.Debugger.prototype.set_condition = function(filename, lineno, colno, lhs, cond, rhs) {
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    var bp;
    if (this.dbg_breakpoints.hasOwnProperty(key)) {
        // Set a new condition
        bp = this.dbg_breakpoints[key];
    } else {
        bp = new Sk.Breakpoint(filename, lineno, colno);
    }
    
    bp.condition = new Sk.Condition(lhs, cond, rhs);
    this.dbg_breakpoints[key] = bp;
};

Sk.Debugger.prototype.print_suspension_info = function(suspension) {
    console.log(suspension)
    var filename = suspension.$filename;
    var lineno = suspension.$lineno;
    var colno = suspension.$colno;
    this.print("Hit Breakpoint at <" + filename + "> at line: " + lineno + " column: " + colno + "\n");
    this.print("----------------------------------------------------------------------------------\n");
    this.print(" ==> " + this.get_source_line(lineno - 1) + "\n");
    this.print("----------------------------------------------------------------------------------\n");
};

Sk.Debugger.prototype.set_suspension = function(suspension) {
    console.log('Set suspension')
    var parent = null;
    if (!suspension.hasOwnProperty("filename") && suspension.child instanceof Sk.misceval.Suspension) {
        console.log('Estamos en 186 primer if de set suspensios')
        suspension = suspension.child;
    }
        
    // Pop the last suspension of the stack if there is more than 0
    if (this.suspension_stack.length > 0) {     
        this.suspension_stack.pop();
        this.current_suspension -= 1;
    }
    
    // Unroll the stack to get each suspension.
    while (suspension instanceof Sk.misceval.Suspension) {
        parent = suspension;
        this.suspension_stack.push(parent);
        this.current_suspension += 1;
        suspension = suspension.child;
    }

    suspension = parent;
    
    this.print_suspension_info(suspension);
    console.log('209')
};

Sk.Debugger.prototype.add_breakpoint = function(filename, lineno, colno, temporary) {
    console.log(filename, lineno, colno, temporary)
    var key = this.generate_breakpoint_key(filename, lineno, colno);
    console.log(key)
    this.dbg_breakpoints[key] = new Sk.Breakpoint(filename, lineno, colno);
    if (temporary) {
        this.tmp_breakpoints[key] = true;
    }
};
// aplicar tecnica de MiscEval en Skilpt aqui
Sk.Debugger.prototype.suspension_handler = function(susp) {
    console.log('221 Suspension handler')
    return new Promise(function(resolve, reject) {
        console.log('223 Suspension handler')
        console.log(susp)
        
        try {
            resolve(susp.resume());
        } catch(e) {
            reject(e);
        }
    });
};

Sk.Debugger.prototype.resume = function() {
    // Reset the suspension stack to the topmost
    this.current_suspension = this.suspension_stack.length - 1;
    if (this.suspension_stack.length === 0) {
        this.print("No running program");
    } else {
        console.log(this.get_active_suspension())
        var promise = this.suspension_handler(this.get_active_suspension());      
        promise.then(this.success.bind(this), this.error.bind(this));
    }
};

Sk.Debugger.prototype.pop_suspension_stack = function() {
    this.suspension_stack.pop();
    this.current_suspension -= 1;
};
/**
 * Necesito saber como hacer que luego de setearle el valor a la suspension que viene de la promesa
 * se ejecute la siguiente suspension
 * tal como pasa en misceval asyncToPromise en Skulpt. Me tengo que vasar en eso
 * para solcionar este problema
 * Otra cosa que me gustaría saber como funciona es como se ejecuta la siguiente suspension y como espera
 * el programa por ella tan solo llaamando a this.set_suspension()
 * @param {*} r 
 * @returns 
 */
Sk.Debugger.prototype.success = function(r) {
    console.log(r)
    if (r instanceof Sk.misceval.Suspension) {        
        if (r.data['type'] == 'Sk.promise') {            
            console.log('Were in a promise')
            var resumeWithData = function resolved(x) {
                try {
                    console.log(r)
                    r.data["result"] = x;
                    var promise = this.suspension_handler(r);      
                    promise.then(this.success.bind(this), this.error.bind(this));
                } catch (e) {
                    this.error(e);
                }
            };
            r.data['promise'].then(resumeWithData, this.error.bind(this));
            return;
        } else {
            this.set_suspension(r);
        }
    } else {
        if (this.suspension_stack.length > 0) {
            console.log('In else')        
            
            // Current suspension needs to be popped of the stack
            this.pop_suspension_stack();
            
            if (this.suspension_stack.length === 0) {                
                return;
            }
            
            var parent_suspension = this.get_active_suspension();
            // The child has completed the execution. So override the child's resume
            // so we can continue the execution.
            parent_suspension.child.resume = function() {
                return r;
            };
            this.resume();
        }
    }
};

Sk.Debugger.prototype.error = function(e) {
    this.print("Traceback (most recent call last):");
    console.log(e)
    for (var idx = 0; idx < e.traceback.length; ++idx) {
        this.print("  File \"" + e.traceback[idx].$filename + "\", line " + e.traceback[idx].$lineno + ", in <module>");
    }
    
    var err_ty = e.constructor.tp$name;
    for (idx = 0; idx < e.args.v.length; ++idx) {
        this.print(err_ty + ": " + e.args.v[idx].v);
    }
};

Sk.Debugger.prototype.asyncToPromise = function(suspendablefn, suspHandlers, debugger_obj) {
    return new Promise(function(resolve, reject) {
        try {
            var r = suspendablefn();
            console.log('Estamos en 290')
            console.log(r);
            console.log(suspendablefn);
            (function handleResponse (r) {
                try {
                    while (r instanceof Sk.misceval.Suspension) {
                        console.log('Estamos en 301')
                        console.log(r);
                        debugger_obj.set_suspension(r);
                        console.log('Estamos en 304')
                        return;
                    }
                    console.log(resolve);
                    resolve(r);
                } catch(e) {
                    reject(e);
                }
            })(r);
            console.log('here? 313')
        } catch (e) {
            console.log('316')
            console.log(e)
            reject(e);
        }
    });
};

Sk.Debugger.prototype.execute = function(suspendablefn, suspHandlers) {
    var r = suspendablefn();
    
    if (r instanceof Sk.misceval.Suspension) {
        this.suspensions.concat(r);
        this.eval_callback(r);
    }
};

Sk.exportSymbol("Sk.Debugger", Sk.Debugger);
