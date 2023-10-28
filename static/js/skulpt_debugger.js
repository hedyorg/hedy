    /**
 * Debugger support for skulpt module
 */

var Sk = Sk || {};

Sk.Breakpoint = function (filename, lineno, colno) {
    this.filename = filename;
    this.lineno = lineno;
    this.colno = colno;
    this.enabled = true;
    this.ignore_count = 0;
};

Sk.Debugger = class {
    constructor(filename, output_callback, stop_callback) {
        this.dbg_breakpoints = {};
        this.tmp_breakpoints = {};
        this.suspensionStack = [];
        this.currentSuspension = -1;
        this.eval_callback = null;
        this.suspension = null;
        this.outputCallback = output_callback;
        this.step_mode = false;
        this.filename = filename;
        this.source_code_lines = [];
        this.program_data = null;
        this.resolveCallback = null;
        this.rejectCallback = null;
        this.stop_callback = stop_callback;
        this.code_starting_line = 0;
    }

    set_code_starting_line(code_starting_line) {
        this.code_starting_line = code_starting_line;
    }

    get_code_starting_line() {
        return this.code_starting_line;
    }

    set_program_data(program_data) {
        this.program_data = program_data;
    }

    get_program_data() {
        return this.program_data;
    }

    set_code_lines(code) {
        this.source_code_lines = code;
    }

    print(txt) {
        console.log(txt);
    }

    get_source_line(lineno) {
        if (this.source_code_lines.length > 0) {
            return this.source_code_lines[lineno];
        }

        return "";
    }

    move_up_the_stack() {
        this.currentSuspension = Math.min(this.currentSuspension + 1, this.suspensionStack.length - 1);
    }

    move_down_the_stack() {
        this.currentSuspension = Math.max(this.currentSuspension - 1, 0);
    }

    enable_step_mode() {
        this.step_mode = true;
    }

    disableStepMode() {
        this.step_mode = false;
    }

    get_suspension_stack() {
        return this.suspensionStack;
    }

    getActiveSuspension() {
        if (this.suspensionStack.length === 0 || 0 > this.currentSuspension) {
            return null;
        }

        return this.suspensionStack[this.currentSuspension];
    }

    generate_breakpoint_key(filename, lineno, colno) {
        var key = filename + "-" + lineno;
        return key;
    }

    check_breakpoints(filename, lineno, colno, globals, locals) {
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
    }

    get_breakpoints_list() {
        return this.dbg_breakpoints;
    }

    disable_breakpoint(filename, lineno, colno) {
        var key = this.generate_breakpoint_key(filename, lineno, colno);

        if (this.dbg_breakpoints.hasOwnProperty(key)) {
            this.dbg_breakpoints[key].enabled = false;
        }
    }

    enable_breakpoint(filename, lineno, colno) {
        var key = this.generate_breakpoint_key(filename, lineno, colno);

        if (this.dbg_breakpoints.hasOwnProperty(key)) {
            this.dbg_breakpoints[key].enabled = true;
        }
    }

    clear_breakpoint(filename, lineno, colno) {
        var key = this.generate_breakpoint_key(filename, lineno, colno);
        if (this.dbg_breakpoints.hasOwnProperty(key)) {
            delete this.dbg_breakpoints[key];
            return null;
        } else {
            return "Invalid breakpoint specified: " + filename + " line: " + lineno;
        }
    }

    clear_all_breakpoints() {
        this.dbg_breakpoints = {};
        this.tmp_breakpoints = {};
    }

    set_ignore_count(filename, lineno, colno, count) {
        var key = this.generate_breakpoint_key(filename, lineno, colno);
        if (this.dbg_breakpoints.hasOwnProperty(key)) {
            var bp = this.dbg_breakpoints[key];
            bp.ignore_count = count;
        }
    }

    set_condition(filename, lineno, colno, lhs, cond, rhs) {
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
    }

    print_suspension_info(suspension) {
        var filename = suspension.$filename;
        var lineno = suspension.$lineno;
        var colno = suspension.$colno;
        this.print("Hit Breakpoint at <" + filename + "> at line: " + lineno + " column: " + colno + "\n");
        this.print("----------------------------------------------------------------------------------\n");
        this.print(" ==> " + this.get_source_line(lineno - 1) + "\n");
        this.print("----------------------------------------------------------------------------------\n");
    }

    set_suspension(suspension) {
        var parent = null;
        if (!suspension.hasOwnProperty("filename") && suspension.child instanceof Sk.misceval.Suspension) {
            suspension = suspension.child;
        }

        // Pop the last suspension of the stack if there is more than 0
        if (this.suspensionStack.length > 0) {
            this.suspensionStack.pop();
            this.currentSuspension -= 1;
        }

        // Unroll the stack to get each suspension.
        while (suspension instanceof Sk.misceval.Suspension) {
            parent = suspension;
            this.suspensionStack.push(parent);
            this.currentSuspension += 1;
            suspension = suspension.child;
        }

        suspension = parent;
        try {
            this.outputCallback();            
        } catch (error) {
            console.error(error)
        }
        // this.print_suspension_info(suspension);
    }

    add_breakpoint(filename, lineno, colno, temporary) {
        var key = this.generate_breakpoint_key(filename, lineno, colno);
        this.dbg_breakpoints[key] = new Sk.Breakpoint(filename, lineno, colno);
        if (temporary) {
            this.tmp_breakpoints[key] = true;
        }
    }

    suspension_handler(susp) {
        return new Promise(function (resolve, reject) {
            try {
                (function handleResponse(r) {
                    try {
                        // jsh*nt insists these be defined outside the loop
                        var resume = function () {
                            try {
                                resolve(r.resume());
                            } catch (e) {
                                reject(e);
                            }
                        };
                        var resumeWithData = function resolved(x) {
                            try {
                                r.data["result"] = x;
                                resume();
                            } catch (e) {
                                reject(e);
                            }
                        };
                        var resumeWithError = function rejected(e) {
                            ;
                            try {
                                r.data["error"] = e;
                                resume();
                            } catch (ex) {
                                reject(ex);
                            }
                        };
                        while (r instanceof Sk.misceval.Suspension) {
                            if (r.data["type"] == "Sk.promise") {
                                r.data["promise"].then(resumeWithData, resumeWithError);
                                return;
                            } else if (r.data["type"] == "Sk.yield") {
                                // Assumes all yields are optional, as Sk.setTimeout might
                                // not be able to yield.
                                //Sk.setTimeout(resume, 0);
                                Sk.global["setImmediate"](resume);
                                return;
                            } else if (r.data["type"] == "Sk.delay") {
                                //Sk.setTimeout(resume, 1);
                                Sk.global["setImmediate"](resume);
                                return;
                            } else if (r.optional) {
                                // Unhandled optional suspensions just get
                                // resumed immediately, and we go around the loop again.
                                return;
                            } else {
                                // Unhandled, non-optional suspension.
                                throw new Sk.builtin.SuspensionError("Unhandled non-optional suspension of type '" + r.data["type"] + "'");
                            }
                        }

                        resolve(r);
                    } catch (e) {
                        reject(e);
                    }
                })(susp);
                resolve(susp.resume());
            } catch (e) {
                reject(e);
            }
        });
    }

    async resume() {
        try {
            await this.handleSuspension(resumeSuspension(this.getActiveSuspension()))
        } catch(e) {
            this.error(e);
        }        
    }

    pop_suspension_stack() {
        this.suspensionStack.pop();
        this.currentSuspension -= 1;
    }


    error(e) {
        this.print("Traceback (most recent call last):");
        for (var idx = 0; idx < e.traceback.length; ++idx) {
            this.print("  File \"" + e.traceback[idx].$filename + "\", line " + e.traceback[idx].$lineno + ", in <module>");
        }

        var err_ty = e.constructor.tp$name;
        for (idx = 0; idx < e.args.v.length; ++idx) {
            this.print(err_ty + ": " + e.args.v[idx].v);
        }
    }

   
    startDebugger(runProgram, debuggerRef) {
        return new Promise(function(resolveCallback, rejectCallback) {
            try {
                var suspension = runProgram();
                try {
                    if (suspension instanceof Sk.misceval.Suspension) {
                        if (suspension.child && suspension.child.$isSuspension) {
                            suspension = suspension.child;
                        }
                        
                        debuggerRef.resolveCallback = resolveCallback;
                        debuggerRef.rejectCallback = rejectCallback;
                        
                        // TODO: remove this field later    
                        debuggerRef.isSingleStep = false;
                        debuggerRef.handleSuspension(suspension);
                    } else {
                        resolveCallback(suspension);
                    }
                } catch (error) {
                    rejectCallback(error)
                }
            } catch (error) {
                rejectCallback(error)
            }
        })
    }

    async continueForward() {       
        if (-1 !== this.currentSuspension) {
            this.disableStepMode()
            await this.resume()
        }        
    };

    onSuspension() {
        this.outputCallback()
    }

    getSuspensionInfo(suspension) {
        let loopSuspension = suspension;
        let lineNumber = loopSuspension.$lineno;
        let columnNumber = loopSuspension.$colno;
        let variables = loopSuspension.hasOwnProperty('$loc') ? loopSuspension.$loc : null;
        while (loopSuspension.child && loopSuspension.child.$isSuspension) {
            lineNumber = loopSuspension.child.$lineno; 
            columnNumber = loopSuspension.child.$colno;
            loopSuspension = loopSuspension.child;
        }        
        variables = loopSuspension.hasOwnProperty('$loc') ? loopSuspension.$loc : null;
        return {
            lineno: lineNumber,
            colno: columnNumber,
            variables: variables
        }
    }

    pushSuspensionStack(suspension) {
        suspension.asyncContext ? this.suspensionStack.splice(this.currentSuspension + 1, 0, suspension) : this.suspensionStack.push(suspension);
        this.currentSuspension += 1;
        this.onSuspension();
    }

    addAsyncSuspension(suspension) {
        let activeSuspension = this.getActiveSuspension();
        this.isSingleStep && this.saveState();
        if (null != activeSuspension)
            if (activeSuspension.asyncContext) {
                let asyncContext = activeSuspension.asyncContext, suspensionIndex = this.currentSuspension;
                while (suspensionIndex < this.suspensionStack.length && asyncContext === this.suspensionStack[suspensionIndex].asyncContext) { 
                    suspensionIndex++; 
                }
                this.suspensionStack.splice(suspensionIndex, 0, suspension)
            } else {
                this.suspensionStack.splice(this.currentSuspension + 1, 0, activeSuspension.clone());
                this.suspensionStack.splice(this.currentSuspension + 1, 0, suspension); 
                this.currentSuspension++; 
                this.onSuspension();
            }
        else  {
            this.suspensionStack.push(suspension); 
            this.currentSuspension = this.suspensionStack.length - 1;
            this.onSuspension();
        }
    }
    async handleSuspension(suspension) {    
        if (!(suspension instanceof Sk.misceval.Suspension)) {
            // The suspension to handle is not a suspension: Either we are done running the program, returning from an asynchronous
            // function or waiting for a callback that the user defined to be called (with asyncContext)
    
            // If the resolve function of the suspension is not null, resolve it. This is needed for asyncContext suspensions
            if (suspension.resolve != null) {
                suspension.resolve(suspension);
            }
    
            // We finished an asynchronous fork, resume with the parent (suspension from where we started)
            if (this.currentSuspension < this.suspensionStack.length - 1) {
                var prevSusp = this.getActiveSuspension();
                this.currentSuspension++;
                var thisSusp = this.getActiveSuspension();
                if (prevSusp.asyncContext !== null && prevSusp.asyncContext !== thisSusp.asyncContext) {
                    //Update the suspensions global variable values
                    thisSusp.updateGlobals(thisSusp);
                }
                this.onSuspension();
            }
            // We finished a fork, but there is no parent if shouldDeferStop() set currentSuspension to -1 and return
            else {
                if (shouldDeferStop()) {
                    this.currentSuspension = -1;
                } else {
                    this.resolveCallback();
                }
    
                //This return is needed, because the babel plugin does some crazy stuff, can be removed if we have await/async natively
                return;
            }
    
    
        } else if (this.currentSuspension < this.suspensionStack.length - 1 && (suspension.asyncContext == null ||
            (this.suspensionStack[this.currentSuspension].asyncContext === this.suspensionStack[this.currentSuspension + 1].asyncContext))) {
            //We are behind the last point the program stopped, just increase the currentSuspension by one. Note that the async context must be the same
            this.currentSuspension++;
            if (suspension instanceof Sk.misceval.Suspension) {
    
                //Get current suspension
                var oldSuspension = this.suspensionStack[this.currentSuspension];
    
                //If a promise, unroll it and possibly wait
                if (suspension.data["type"] === "Sk.promise") {
                    suspension = await unrollPromise(suspension);
                }
    
                // We need to write the changes to the succeeding suspension, else any user changes to the variables is lost
    
                // -- Copy all changes to $loc and $gbl (globals variables) of the next suspension --
                // ----------------------------------------------------------------------------------
                copyVariables.call(this, suspension.$locValues, oldSuspension.$locValues);
                copyVariables.call(this, suspension.$gblValues, oldSuspension.$gblValues);
    
                // -- Copy all changes to $tmps (local variables) of the next suspension --
                // ------------------------------------------------------------------------
                // We need to go to the inner most suspension
                var tmpOldSusp = oldSuspension;
                var tmpSusp = suspension;
                while (tmpOldSusp.child && tmpOldSusp.child.$isSuspension && tmpSusp.child && tmpSusp.child.$isSuspension) {
                    tmpOldSusp = tmpOldSusp.child; //iterate to child to change variables
                    tmpSusp = tmpSusp.child; //iterate to child to change variables
                }
    
                copyVariables.call(this, tmpSusp.$tmps, tmpOldSusp.$tmps);
            }
    
            // Display the current values of the variables of the suspension
            this.onSuspension();
        } else if (suspension instanceof Sk.misceval.Suspension) {
            //If a promise, unroll it and possibly wait and handle the return value
            if (suspension.data["type"] === "Sk.promise") {
                return this.handleSuspension(await unrollPromise(suspension));
            }
            //Push the suspension on the stack
            this.pushSuspensionStack(suspension);
        }
    
    }
}


// I don't know if I need this
function copyVariables(a, b) {
    for (var c in a) {
        if (!a.hasOwnProperty(c) || "undefined" === typeof c || c.toString().startsWith("$") || 
            c.toString().startsWith("__") || "undefined" === typeof a[c]) {
            break;
        }
        var d = a[c].__proto__.tp$name;
        null != b[c] && -1 < this.typesToDeepCopy.indexOf(d) && (b[c] = structuredClone(a[c]))
    }
}

async function unrollPromise(suspension) {
    while (suspension instanceof Sk.misceval.Suspension && suspension.data["type"] === "Sk.promise") {
        if (!suspension.optional) {
            await suspension.data["promise"].then(function (data) {
                suspension.data["result"] = data;
            }, function (e) {
                this.error(e);
            });
        }
        suspension = resumeSuspension(suspension);
    }
    return suspension;
}


// what is this function supposed to do? idk
function shouldDeferStop() {
    return false;
}


function resumeSuspension(suspension) {
    var resumed = suspension.resume();
    resumed.asyncContext = suspension.asyncContext;
    resumed.resolve = null != suspension.resolve ? suspension.resolve : resumed.resolve;
    return resumed
}

Sk.exportSymbol("Sk.Debugger", Sk.Debugger);
