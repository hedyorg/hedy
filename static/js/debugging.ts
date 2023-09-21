import { runit } from "./app";
import { HedyEditor, Breakpoints } from "./editor";

let theGlobalEditor: HedyEditor;
let theLevel: number;
let theLanguage: string;

//Feature flag for variable and values view
let variable_view = false;
let step_debugger = false;

/**
 * Add types for the gutter event
 */
interface GutterMouseDownEvent {
  readonly domEvent: MouseEvent;
  readonly clientX: number;
  readonly clientY: number;
  readonly editor: AceAjax.Editor;

  getDocumentPosition(): AceAjax.Position;
  stop(): void;
}


function hide_if_no_variables(){
  if($('#variables #variable-list li').length == 0){
    $('#variable_button').hide();
  }
  else{
    $('#variable_button').show();
  }
}

export function show_variables() {
  if (variable_view === true) {
    const variableList = $('#variable-list');
    if (variableList.hasClass('hidden')) {
      variableList.removeClass('hidden');
    }
  }
}

export function load_variables(variables: any) {
  if (variable_view === true) {
    variables = clean_variables(variables);
    const variableList = $('#variable-list');
    variableList.empty();
    for (const i in variables) {
      // Only append if the variable contains any data (and is not undefined)
      if (variables[i][1]) {
        variableList.append(`<li style=color:${variables[i][2]}>${variables[i][0]}: ${variables[i][1]}</li>`);
      }
    }
    hide_if_no_variables();
  }
}

// Color-coding string, numbers, booleans and lists
// This will be cool to use in the future!
// Just change the colors to use it
function special_style_for_variable(variable: Variable) {
  let result = '';
  let parsedVariable = parseInt(variable.v as string);
  if (typeof parsedVariable == 'number' && !isNaN(parsedVariable)){
     result =  "#ffffff";
   }
   if(typeof variable.v == 'string' && isNaN(parsedVariable)){
     result = "#ffffff";
   }
   if(typeof variable.v == 'boolean'){
     result = "#ffffff";
   }
   if (variable.tp$name == 'list'){
    result =  "#ffffff";
   }
   return result;
}

//hiding certain variables from the list unwanted for users
function clean_variables(variables: Record<string, Variable>) {
  const new_variables = [];
  const unwanted_variables = ["random", "time", "int_saver", "int_$rw$", "turtle", "t"];
  for (const variable in variables) {
    if (!variable.includes('__') && !unwanted_variables.includes(variable)) {
      let extraStyle = special_style_for_variable(variables[variable]);
      let name = unfixReserved(variable);
      let newTuple = [name, variables[variable].v, extraStyle];
      new_variables.push(newTuple);
    }
  }
  return new_variables;
}

function unfixReserved(name: string) {
  return name.replace(/_\$rw\$$/, "");
}


/**
 * The 'ace_breakpoint' style has been overridden to show a sleeping emoji in the gutter
 */
const BP_DISABLED_LINE = 'ace_breakpoint';

export interface InitializeDebuggerOptions {
  readonly level: number;
  readonly editor: HedyEditor;
  readonly language: string;
}

export function initializeDebugger(options: InitializeDebuggerOptions) {
  theGlobalEditor = options.editor;
  theLevel = options.level;
  theLanguage = options.language;

  //Hides the HTML DIV for variables if feature flag is false
  if (!variable_view) {
    $('#variables').hide();
    $('#variable_button').hide();
  }

  //Feature flag for step by step debugger. Becomes true automatically for level 7 and below.
  if (options.level > 0) {
    let level = options.level;
    step_debugger = level <= 700;
  }

  //Hides the debug button if feature flag is false
  if (!step_debugger) {
    $('#debug_button').hide();
  }

  if(options.level != 0){
    let level = options.level;
    variable_view = level >= 2;
    hide_if_no_variables();
  }

  initializeBreakpoints(options.editor);
}

function initializeBreakpoints(editor: HedyEditor) {
  
  editor.on("guttermousedown", function (e: GutterMouseDownEvent) {
    const target = e.domEvent.target as HTMLElement;

    // Not actually the gutter
    if (target.className.indexOf("ace_gutter-cell") == -1)
      return;

    if (e.clientX > 25 + target.getBoundingClientRect().left)
      return;

    const breakpoints = getBreakpoints(e.editor);

    let row = e.getDocumentPosition().row;
    if (breakpoints[row] === undefined && row !== e.editor.getLastVisibleRow() + 1) {
      // If the shift key is pressed mark all rows between the current one and the first one above that is a debug line
      if (get_shift_key(event)) {
        let highest_key = row;
        for (const key in breakpoints) {
          const number_key = parseInt(key);
          if (number_key < row) {
            highest_key = number_key;
          }
        }
        for (let i = highest_key; i <= row; i++) {
          e.editor.session.setBreakpoint(i, BP_DISABLED_LINE);
        }
      } else {
        e.editor.session.setBreakpoint(row, BP_DISABLED_LINE);
      }
    } else {
      e.editor.session.clearBreakpoint(row);
    }
    e.stop();
  });

  /**
 * Render markers for all lines that have breakpoints
 * 
 * (Breakpoints mean "disabled lines" in Hedy).
 * */
  editor.on('changeBreakpoint', function() {
    const breakpoints = theGlobalEditor.getBreakpoints();

    const disabledLines = Object.entries(breakpoints)
      .filter(([_, bpClass]) => bpClass === BP_DISABLED_LINE)
      .map(([line, _]) => line)
      .map(x => parseInt(x, 10));

    theGlobalEditor.strikethroughLines(disabledLines);
  });
}

function get_shift_key(event: Event | undefined) {
  // @ts-ignore
  if (event.shiftKey) {
    return true;
  } return false;
}

function debugRun() {
  if (theLevel && theLanguage) {
    runit(theLevel, theLanguage, "", "run", function () {
      $('#output').focus();
    });
  }
}

export function startDebug() {
  if (step_debugger === true) {
    var debugButton = $("#debug_button");
    debugButton.hide();
    var continueButton = $("#debug_continue");
    var stopButton = $("#debug_stop");
    var resetButton = $("#debug_restart");
    var runButtonContainer = $("#runButtonContainer");

    runButtonContainer.hide();
    continueButton.show();
    stopButton.show();
    resetButton.show();

    incrementDebugLine();
  }
}

export function resetDebug() {
  if (step_debugger === true) {
    var storage = window.localStorage;
    var continueButton = $("#debug_continue");
    continueButton.show();

    storage.setItem("debugLine", "0");
    clearDebugVariables();
    markCurrentDebuggerLine();
    debugRun();
  }
}

export function stopDebug() {
  if (step_debugger === true) {
    var debugButton = $("#debug_button");
    debugButton.show();
    var continueButton = $("#debug_continue");
    var stopButton = $("#debug_stop");
    var resetButton = $("#debug_restart");
    var runButtonContainer = $("#runButtonContainer");

    runButtonContainer.show();
    continueButton.hide();
    stopButton.hide();
    resetButton.hide();

    var storage = window.localStorage;
    storage.removeItem("debugLine");

    clearDebugVariables();
    markCurrentDebuggerLine();
  }
}

function clearDebugVariables() {
  var storage = window.localStorage;
  var keysToRemove = {...localStorage};

  for (var key in keysToRemove) {
    if (key.includes("prompt-")) {
      storage.removeItem(key);
    }
  }
}

export function incrementDebugLine() {
  var storage = window.localStorage;
  var debugLine = storage.getItem("debugLine");

  const nextDebugLine = debugLine == null
    ? 0
    : parseInt(debugLine, 10) + 1;

  storage.setItem("debugLine", nextDebugLine.toString());
  markCurrentDebuggerLine();

  var lengthOfEntireEditor = theGlobalEditor.contents.split("\n").filter(e => e).length;
  if (nextDebugLine < lengthOfEntireEditor) {
    debugRun();
  } else {
    stopDebug();
  }
}

function markCurrentDebuggerLine() {
  if (!step_debugger) { return; }

  const storage = window.localStorage;
  var debugLine = storage?.getItem("debugLine");

  if (debugLine != null) {
    var debugLineNumber = parseInt(debugLine, 10);
    theGlobalEditor.setDebuggerCurrentLine(debugLineNumber);
  } else {
    theGlobalEditor.setDebuggerCurrentLine(undefined);
  }
}

export function returnLinesWithoutBreakpoints(editor: HedyEditor) {

  // ignore the lines with a breakpoint in it.
  let code = editor.contents;
  const breakpoints = editor.getBreakpoints();
  const storage = window.localStorage;
  const debugLines = storage.getItem('debugLine');

  if (code) {
    let lines = code.split('\n');
    if(debugLines != null){
      lines = lines.slice(0, parseInt(debugLines) + 1);
    }
    for (let i = 0; i < lines.length; i++) {
      if (breakpoints[i] == BP_DISABLED_LINE) {
        lines[i] = '';
      }
    }
    code = lines.join('\n');
  }

  return code;
}

/**
 * The '@types/ace' package has the type of breakpoints incorrect
 *
 * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
 * but can be something you pick yourself.
 */
function getBreakpoints(editor: AceAjax.Editor): Breakpoints {
  return editor.session.getBreakpoints() as unknown as Breakpoints;
}