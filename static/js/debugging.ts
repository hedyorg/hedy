import { runit, theGlobalDebugger,theGlobalSourcemap } from "./app";
import { HedyEditor, Breakpoints } from "./editor";
import  TRADUCTION_IMPORT  from '../../highlighting/highlighting-trad.json'
let theGlobalEditor: HedyEditor;
let theLevel: number;
let theLanguage: string;
let TRADUCTION: Map<string,string>;

//Feature flag for variable and values view
let variable_view = true;
let step_debugger = false;
const fullLineCommands = [
  'print',
  'echo',
  'assign',
  'sleep',
  'assign_list',
  'add',
  'remove',
  'ask',
  'play',
  'command', // the turtle and clear commands get put in the source map as 'command'
]

const blockCommands = [
  'ifs',
  'ifelse',
  'if_pressed_else',
  'repeat',
  'if_pressed',
  'elses',
  'if_pressed_elses',
  'for_list',
  'for_loop',
  'while_loop',
  'elifs',
  'if_pressed_elifs',
]

const ifRegex = "((__if__) *[^\n ]+ *((__is__)|(__in__)) *[^\n ]+) *.*";
const repeatRegex = "((__repeat__) *[^\n ]+ *(__times__)) *[^\n ]+ *.+";
const elseRegex = "^(__else__) *[^\n ]+.+$";

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

//this shows just the button, not the list itself
export function hide_if_no_variables(){
  if($('#variables #variable-list li').length == 0){
    $('#variable_button').hide();
    $('#variables').hide();
    $('#variables-expand'). hide();
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
        const variableName = variables[i][0].replace(/^_/, '');
        variableList.append(`<li style=color:${variables[i][2]}>${variableName}: ${variables[i][1]}</li>`);
      }
    }
    show_variables();
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
     result =  "#4299e1";
   }
   if(typeof variable.v == 'string' && isNaN(parsedVariable)){
     result = "#4299e1";
   }
   if(typeof variable.v == 'boolean'){
     result = "#4299e1";
   }
   if (variable.tp$name == 'list'){
    result =  "#4299e1";
   }
   return result;
}
//hiding certain variables from the list unwanted for users
function clean_variables(variables: Record<string, Variable>) {
  const new_variables = [];
  const unwanted_variables = ["random", "time", "int_saver", "int_$rw$", "turtle", "t", "chosen_note"];
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
  readonly keywordLanguage: string;
}

export function initializeDebugger(options: InitializeDebuggerOptions) {
  theGlobalEditor = options.editor;
  theLevel = options.level;
  theLanguage = options.language;
  let TRADUCTIONS = convert(TRADUCTION_IMPORT) as Map<string, Map<string,string>>;
  let lang = options.keywordLanguage;
  if (!TRADUCTIONS.has(lang)) { lang = 'en'; }
  // get the traduction
  TRADUCTION = TRADUCTIONS.get(lang) as Map<string,string> ;

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
    show_variables();
    hide_if_no_variables();
  }
  initializeBreakpoints(options.editor);
}

function initializeBreakpoints(editor: HedyEditor) {
  /**
   * Both of these events listener only are executed for Ace
   * CodeMirror doesn't need them
   */

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
}

function get_shift_key(event: Event | undefined) {
  // @ts-ignore
  if (event.shiftKey) {
    return true;
  } return false;
}

function debugRun() {
  if (theLevel && theLanguage) {
    runit(theLevel, theLanguage, false, "", "run", function () {
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

    $('#stopit').hide();
    $('#runit').show()
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
  const active_suspension = theGlobalDebugger.getActiveSuspension();
  const suspension_info = theGlobalDebugger.getSuspensionInfo(active_suspension);
  const lineNumber = suspension_info.lineno;
  load_variables(suspension_info.variables);
  const ifRegexTranslated = ifRegex.replace('__if__', TRADUCTION.get('if')!)
    .replace('__is__', TRADUCTION.get('is')!)
    .replace('__in__', TRADUCTION.get('in')!);

  const repeatRegexTranslated = repeatRegex.replace('__repeat__', TRADUCTION.get('repeat')!)
    .replace('__times__', TRADUCTION.get('times')!);

  const elseRegexTranslated = elseRegex.replace('__else__', TRADUCTION.get('else')!)

  const ifRe = new RegExp(ifRegexTranslated, "gu");
  const repeatRe = new RegExp(repeatRegexTranslated, "gu");
  const elseRe = new RegExp(elseRegexTranslated, "gu");

  if (!lineNumber) return;
  for (const [_, map] of Object.entries(theGlobalSourcemap)) {
    const startingLine = map.python_range.from_line + theGlobalDebugger.get_code_starting_line();
    const finishingLine = map.python_range.to_line + theGlobalDebugger.get_code_starting_line();
    // Maybe we hit the correct mapping for this line
    if (lineNumber >= startingLine && lineNumber <= finishingLine) { 
      // Highlight whole line if it's a full command
      if(fullLineCommands.includes(map.command)){        
        // lines in ace start at 0       
        const lines = theGlobalEditor.contents.split('\n');
        const line = lines[map.hedy_range.from_line - 1];
        const ifMatches = ifRe.exec(line);
        const repeatMatches = repeatRe.exec(line);
        const elseMatches = elseRe.exec(line);
        if (ifMatches || repeatMatches || elseMatches) {
          theGlobalEditor.setDebuggerCurrentLine(map.hedy_range.from_line, 
            map.hedy_range.from_column, map.hedy_range.to_column - 1);
        } else {
          theGlobalEditor.setDebuggerCurrentLine(map.hedy_range.from_line);
        }
        break
      } else if (theLevel <= 7 && blockCommands.includes(map.command)){
        const lines = theGlobalEditor.contents.split('\n');
        let line: string;
        if (map.hedy_range.from_line < map.hedy_range.to_line) {
          line = lines[map.hedy_range.from_line - 1];
        } else {
          const fullLine = lines[map.hedy_range.from_line - 1];
          line = fullLine.substring(map.hedy_range.from_column - 1, map.hedy_range.to_column - 1);
        }       
        const activeLine: string = theGlobalDebugger.get_source_line(lineNumber - 1);

        if (activeLine.match(/ *if/)) {
          const ifMatches = ifRe.exec(line);
          if (ifMatches) {
            const length = ifMatches[1].length;
            theGlobalEditor.setDebuggerCurrentLine(map.hedy_range.from_line, map.hedy_range.from_column, map.hedy_range.from_column + length - 1);            
            break
          }
        } else if (activeLine.match(/ *for/)) {
          const repeatMatches = repeatRe.exec(line);
          if (repeatMatches){            
            const length = repeatMatches[1].length;            
            theGlobalEditor.setDebuggerCurrentLine(map.hedy_range.from_line, map.hedy_range.from_column, map.hedy_range.from_column + length - 1);
            break
          }
        }
      }  else if (theLevel >= 8 && blockCommands.includes(map.command)) { // these commands always come up in the tree so we visit them later
        theGlobalEditor.setDebuggerCurrentLine(map.hedy_range.from_line);
        break;
      }
    }
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

/**
 * The '@types/ace' package has the type of breakpoints incorrect
 *
 * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
 * but can be something you pick yourself.
 */
function getBreakpoints(editor: AceAjax.Editor): Breakpoints {
  return editor.session.getBreakpoints() as unknown as Breakpoints;
}

export function convert(o:(object|undefined)) {
  if (typeof o === 'object') {
    let tmp:Map<string, object> = new Map(Object.entries(o));

    let ret:Map<string, (undefined|object)> = new Map();

    tmp.forEach((value, key) => {
      ret.set(key, convert(value));
    });

    return ret;
  } else {
    return o;
  }
}
